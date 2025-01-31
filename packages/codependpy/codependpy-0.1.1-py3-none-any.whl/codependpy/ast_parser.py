import ast
from .project_types import FileInfo, Definition
from .utils import resolve_relative_import, attr_chain

class Parser(ast.NodeVisitor):
    def __init__(self, info: FileInfo):
        super().__init__()
        self.info = info
        self.current_class_stack = []  # We'll track class name(s) up the stack

    def visit_Import(self, node: ast.Import):
        """
        e.g. "import myapp.models as mm" => import_aliases["mm"] = "myapp.models"
        """
        for alias in node.names:
            alias_name = alias.asname if alias.asname else alias.name
            self.info.import_aliases[alias_name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """
        e.g. "from myapp.models import User as U" => import_symbols["U"] = ("myapp.models", "User")
        with relative import => level>0
        """
        if node.module is not None:
            if node.level > 0:
                base_mod = resolve_relative_import(self.info.path, node.level, node.module)
            else:
                base_mod = node.module
            for alias in node.names:
                real_name = alias.name
                alias_name = alias.asname if alias.asname else real_name
                self.info.import_symbols[alias_name] = (base_mod, real_name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        func_str = attr_chain(node.func)
        # Django dynamic: apps.get_model(...)
        if func_str.endswith("get_model"):
            if len(node.args) >= 2:
                a, b = node.args[:2]
                if all(isinstance(x, ast.Constant) for x in [a, b]):
                    self.info.django_refs.append((a.value, b.value))

        # Django URL patterns: path(...) / re_path(...)
        if func_str in ("path", "re_path"):
            # we do a quick look for direct references as in original code
            if node.args:
                self._maybe_add_url_ref(node.args[0])
            for kw in node.keywords:
                if kw.arg == "view":
                    self._maybe_add_url_ref(kw.value)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        We'll create a definition for the class itself (e.g., "MyClass") and then
        create sub-definitions for each method "MyClass.methodName".
        """
        class_name = node.name
        class_def = Definition(
            name=class_name,
            start_line=node.lineno,
            end_line=self._end_line(node),
            node=node,
            parent=None
        )
        self.info.definitions[class_name] = class_def

        self.current_class_stack.append(class_name)

        # We also want to see if base classes are local references
        for base in node.bases:
            if isinstance(base, ast.Name):
                class_def.local_refs.add(base.id)
            elif isinstance(base, ast.Attribute):
                class_def.local_refs.add(attr_chain(base))

        # Now visit the body. We'll catch function defs as separate definitions.
        self.generic_visit(node)

        self.current_class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Functions might be top-level or inside a class. We'll do a 'qualified name' for class methods.
        E.g., if we are inside class Foo, then the method is "Foo.my_method".
        """
        qualified_name = node.name
        parent_class = self._get_current_class()
        if parent_class:
            qualified_name = f"{parent_class}.{node.name}"

        def_def = Definition(
            name=qualified_name,
            start_line=node.lineno,
            end_line=self._end_line(node),
            node=node,
            parent=parent_class
        )
        self.info.definitions[qualified_name] = def_def

        # We'll gather references by traversing the method body
        self._process_function_body(node, def_def)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        # We can treat it the same as a normal function def
        self.visit_FunctionDef(node)

    def _process_function_body(self, node: ast.FunctionDef, def_obj: Definition):
        """
        We'll do a second visitor to gather local references from inside the function.
        """
        FunctionBodyVisitor(def_obj, self._get_current_class()).visit(node)

    def visit_Name(self, node: ast.Name):
        """
        If we see a Name at top-level (not inside a function/class?), let's assume
        it's a reference in a global scope. We'll put it in a special top-level definition if you wish.
        But typically top-level references that are not in a def or class are less common.
        For simplicity, do nothing special here.
        """
        self.generic_visit(node)

    def _maybe_add_url_ref(self, val):
        if isinstance(val, ast.Name):
            self.info.url_refs.append(val.id)
        elif isinstance(val, ast.Attribute):
            chain = attr_chain(val)
            self.info.url_refs.append(chain)

    def _get_current_class(self):
        return self.current_class_stack[-1] if self.current_class_stack else None

    def _end_line(self, node: ast.AST) -> int:
        if hasattr(node, "end_lineno") and node.end_lineno:
            return node.end_lineno
        return max(
            [getattr(node, "lineno", 0)] +
            [self._end_line(ch) for ch in ast.iter_child_nodes(node)]
        )

class FunctionBodyVisitor(ast.NodeVisitor):
    """
    A specialized visitor that collects references inside a function body.
    We'll handle `self.x` or `cls.y`.
    """
    def __init__(self, definition_obj: Definition, current_class: str):
        self.def_obj = definition_obj
        self.current_class = current_class
        super().__init__()

    def visit_Name(self, node: ast.Name):
        # If it's a direct name reference, add it
        self.def_obj.local_refs.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        """
        E.g. "self.foo" => if we are inside class Bar, that references "Bar.foo".
        We do the same for "cls.foo" if you use classmethods.
        """
        full_chain = attr_chain(node)
        # If the base is "self" or "cls" and we have a current_class,
        # treat it as referencing "current_class.attr"
        if isinstance(node.value, ast.Name):
            base_name = node.value.id
            if base_name in ("self", "cls") and self.current_class:
                # e.g. "MyClass.foo"
                qualified = f"{self.current_class}.{node.attr}"
                self.def_obj.local_refs.add(qualified)
            else:
                # normal "module.attr"
                self.def_obj.local_refs.add(full_chain)
        else:
            # normal "something.something"
            self.def_obj.local_refs.add(full_chain)

        self.generic_visit(node)

def parse_file(filepath: str) -> FileInfo:
    fi = FileInfo(path=filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()
    fi.source_lines = src.splitlines(True)
    root = ast.parse(src, filepath)
    Parser(fi).visit(root)
    return fi
