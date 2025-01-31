# utils.py
import os
import ast

def is_third_party(path: str) -> bool:
    """
    If path is in site-packages or dist-packages, treat it as external.
    """
    return ("site-packages" in path) or ("dist-packages" in path)

def resolve_relative_import(base_file: str, level: int, module: str) -> str:
    """
    Convert from .models => 'myproj.models'
    """
    base_dir = os.path.dirname(base_file)
    parts = base_dir.split(os.sep)
    new_parts = parts[:-level] if level <= len(parts) else []
    if module:
        new_parts.append(module.replace(".", os.sep))
    resolved = os.path.join(*new_parts)
    return resolved.replace(os.sep, ".") if resolved else module

def attr_chain(node: ast.AST) -> str:
    """
    For node = myapp.models.User => "myapp.models.User"
    """
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    parts.reverse()
    return ".".join(parts)
