# project_types.py
import ast
from dataclasses import dataclass, field
from typing import List, Set, Dict, Optional, Tuple

@dataclass
class Definition:
    name: str
    start_line: int
    end_line: int
    node: ast.AST
    local_refs: Set[str] = field(default_factory=set)
    parent: Optional[str] = None

@dataclass
class FileInfo:
    """
    Represents a single .py file's extracted data:
      - definitions: top-level classes/functions
      - django_refs: calls to apps.get_model(...)
      - url_refs: calls to path(...) or re_path(...)
      - import_aliases, import_symbols: track how imports map to real modules and symbol names
    """
    path: str
    source_lines: List[str] = field(default_factory=list)
    definitions: Dict[str, Definition] = field(default_factory=dict)
    django_refs: List[Tuple[str, str]] = field(default_factory=list)
    url_refs: List[str] = field(default_factory=list)

    # "import myapp.models as mm" => import_aliases["mm"] = "myapp.models"
    import_aliases: Dict[str, str] = field(default_factory=dict)

    # "from myapp.models import User as U" => import_symbols["U"] = ("myapp.models", "User")
    import_symbols: Dict[str, Tuple[str, str]] = field(default_factory=dict)

@dataclass
class TargetSpec:
    file_path: str
    symbols: List[str]

@dataclass
class ParsedProject:
    files: Dict[str, FileInfo]
    # symbol -> list of file(s) that define it
    symbol_index: Dict[str, List[str]]
    # module -> file path
    module_index: Dict[str, str]
    # For Django dynamic (app, model) => (file, symbol)
    django_index: Dict[Tuple[str, str], Tuple[str, str]]
