import logging
from collections import defaultdict, deque
from typing import Dict, Set, Tuple, Deque
from .project_types import ParsedProject, TargetSpec, FileInfo
from .utils import is_third_party

def gather_definitions(
    proj: ParsedProject,
    targets: Tuple[TargetSpec, ...],
    mode: str = "all",
    max_depth: int = 3
) -> Dict[str, Set[str]]:
    """
    BFS that collects only the classes/methods truly used up to a certain depth.
    Because we now have granular definitions (ClassName.methodName),
    we won't fallback to entire files unless we REALLY want to.

    'needed' = { file_path: set_of_def_names_in_that_file }
    But now def_name can be "MyClass", "MyClass.method_x", or a top-level "some_func".
    """
    needed = defaultdict(set)  # file -> set of definition names
    queue: Deque[Tuple[str, str, int]] = deque()
    visited = set()

    # Keep track if we've processed top-level imports for a file
    processed_imports_for_file = set()

    # 1) Initialize BFS from user targets
    for t in targets:
        if t.file_path not in proj.files:
            continue
        fi = proj.files[t.file_path]
        # If user gave no specific symbols, we BFS everything in that file. But let's remain consistent:
        symbols = t.symbols or list(fi.definitions.keys())
        for s in symbols:
            # Because we might have "MyClass.my_method" or just "MyClass" or "some_func"
            if s in fi.definitions:
                needed[t.file_path].add(s)
                queue.append((t.file_path, s, 0))
            else:
                # If user references a symbol not found, skip or fallback to entire class?
                logging.warning(f"Symbol '{s}' not found in {t.file_path}. Skipping.")
                # We'll skip in this sample – or you could do a bigger fallback if you want.

    # 2) BFS
    while queue:
        curr_file, curr_sym, depth = queue.popleft()
        if (curr_file, curr_sym, depth) in visited:
            continue
        visited.add((curr_file, curr_sym, depth))

        # If the file is third-party or we have no record, skip
        if is_third_party(curr_file) or curr_file not in proj.files:
            continue

        # Only expand further if we haven't exceeded max_depth
        if depth < max_depth:
            fi = proj.files[curr_file]
            defi = fi.definitions.get(curr_sym)
            if not defi:
                # if we can't find the def, skip or fallback to bigger logic
                continue

            # process top-level imports from that file (once)
            if curr_file not in processed_imports_for_file:
                process_top_level_imports(proj, curr_file, needed, queue, mode, depth)
                processed_imports_for_file.add(curr_file)

            # BFS references from that definition
            for ref in defi.local_refs:
                # If "MyClass.my_method", "os.path" or just "Foo"
                handle_local_ref(proj, needed, queue, curr_file, ref, mode, depth)

            # also handle django get_model / url refs if you like
            # (same as original code)
            for (app, model) in fi.django_refs:
                key = (app, model)
                if key in proj.django_index:
                    file_for_model, sym_name = proj.django_index[key]
                    needed[file_for_model].add(sym_name)
                    queue.append((file_for_model, sym_name, depth + 1))

            for rv in fi.url_refs:
                handle_local_ref(proj, needed, queue, curr_file, rv, mode, depth)

    return needed

def process_top_level_imports(
    proj: ParsedProject,
    file_path: str,
    needed: Dict[str, Set[str]],
    queue: Deque[Tuple[str, str, int]],
    mode: str,
    depth: int
):
    fi = proj.files[file_path]

    # import_aliases => e.g. "import myapp.models as mm"
    for alias, real_mod_name in fi.import_aliases.items():
        if real_mod_name in proj.module_index:
            mod_file = proj.module_index[real_mod_name]
            if not is_third_party(mod_file):
                # we push the 'alias' symbol from mod_file or the entire definitions if you want
                # but typically alias is just an import name. We'll skip it unless you want to BFS it
                pass

    # import_symbols => e.g. "from myapp.models import User as U"
    for alias, (base_mod, real_sym) in fi.import_symbols.items():
        if base_mod in proj.module_index:
            mod_file = proj.module_index[base_mod]
            if not is_third_party(mod_file):
                # push the real_sym from mod_file
                push_symbol(proj, needed, queue, mod_file, real_sym, mode, depth)

def handle_local_ref(
    proj: ParsedProject,
    needed: Dict[str, Set[str]],
    queue: Deque[Tuple[str, str, int]],
    curr_file: str,
    ref: str,
    mode: str,
    depth: int
):
    """
    If ref is "MyClass.my_method", "Foo", or "x.y.z" etc., we try to find a matching definition in the same file,
    or in symbol_index, etc. No entire-file fallback now.
    """
    # If it references a local definition within the same file, push it:
    fi = proj.files[curr_file]
    if ref in fi.definitions:
        if ref not in needed[curr_file]:
            needed[curr_file].add(ref)
            queue.append((curr_file, ref, depth + 1))
        return

    # If ref is in the global symbol_index, BFS from there
    if ref in proj.symbol_index:
        all_files = proj.symbol_index[ref]
        if mode == "first":
            pick = all_files[0]
            if not is_third_party(pick):
                if ref not in needed[pick]:
                    needed[pick].add(ref)
                    queue.append((pick, ref, depth + 1))
        else:
            for f in all_files:
                if not is_third_party(f):
                    if ref not in needed[f]:
                        needed[f].add(ref)
                        queue.append((f, ref, depth + 1))
        return

    # If we can't find it, we just skip. Or you can fallback to "MyClass" if ref looks like "MyClass.whatever".
    # For demonstration, I'm skipping. If you want partial fallback:
    # e.g. if "MyClass.method_x" not found, fallback to "MyClass" if it exists, etc.

def push_symbol(
    proj: ParsedProject,
    needed: Dict[str, Set[str]],
    queue: Deque[Tuple[str, str, int]],
    file_path: str,
    symbol: str,
    mode: str,
    depth: int
):
    if is_third_party(file_path):
        return
    if file_path not in proj.files:
        return
    fi = proj.files[file_path]

    if symbol in fi.definitions:
        if symbol not in needed[file_path]:
            needed[file_path].add(symbol)
            queue.append((file_path, symbol, depth + 1))
    else:
        # Symbol not found => skip or fallback
        pass
