# index_builder.py
import os
from typing import Dict, List, Tuple
from .project_types import ParsedProject, FileInfo

def to_module_name(file_path: str, base_dirs: List[str]) -> str:
    ap = os.path.abspath(file_path)
    chosen = ""
    for d in base_dirs:
        dabs = os.path.abspath(d)
        if ap.startswith(dabs) and len(dabs) > len(chosen):
            chosen = dabs
    rel = os.path.relpath(ap, chosen) if chosen else os.path.basename(ap)
    no_ext = os.path.splitext(rel)[0]
    return no_ext.replace(os.sep, ".")

def build_parsed_project(
    files: Dict[str, FileInfo],
    base_dirs: List[str]
) -> ParsedProject:
    sym_idx = {}
    mod_idx = {}
    dj_idx = {}

    # Build symbol_index, module_index
    for fpath, info in files.items():
        mod = to_module_name(fpath, base_dirs)
        mod_idx[mod] = fpath
        for d in info.definitions.values():
            sym_idx.setdefault(d.name, []).append(fpath)

    # Build django_index from apps.get_model calls
    for fpath, info in files.items():
        for (app, model) in info.django_refs:
            guess_mod = f"{app}.models"
            if guess_mod in mod_idx:
                cfile = mod_idx[guess_mod]
                if model in files[cfile].definitions:
                    dj_idx[(app, model)] = (cfile, model)

    return ParsedProject(files, sym_idx, mod_idx, dj_idx)
