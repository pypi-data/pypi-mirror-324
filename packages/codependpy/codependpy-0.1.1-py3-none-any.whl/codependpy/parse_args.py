# parse_args.py
import argparse
import os
from typing import List
from .project_types import TargetSpec

def parse_arguments() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="codependpy", description="Partial Py Dep Collector")

    # 1) Positional for the 'file.py:Sym1,Sym2' specs
    p.add_argument(
        "targets", 
        nargs="+",
        help="One or more paths in the form 'file.py:Symbol1,Symbol2'"
    )

    # 2) Optional flags for BFS depth, search-dir, etc.
    p.add_argument(
        "-d", "--depth",
        type=int,
        default=3,
        help="How deep the BFS goes (default=3)"
    )
    p.add_argument(
        "-s", "--search-dir",
        action="append",
        default=["."],
        help="Dirs to search for .py files (can be used multiple times)"
    )
    p.add_argument(
        "-e", "--exclude",
        default="",
        help="Regex to exclude certain paths"
    )
    p.add_argument(
        "-o", "--output",
        default="collected.py",
        help="Output file for extracted code"
    )

    return p.parse_args()


def build_targets(target_args: List[str]) -> List[TargetSpec]:
    """
    Convert each 'file.py:Symbol1,Symbol2' positional argument
    into a TargetSpec(file_path='absolute/path/to/file.py', symbols=[Symbol1, Symbol2]).
    """
    results = []
    for t in target_args:
        if ":" in t:
            path_part, syms = t.split(":", 1)
            symbols = [s.strip() for s in syms.split(",") if s.strip()]
        else:
            path_part, symbols = t, []
        results.append(
            TargetSpec(
                file_path=os.path.abspath(path_part), 
                symbols=symbols
            )
        )
    return results
