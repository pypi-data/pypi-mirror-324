# file_scanner.py
import os
import re
from typing import List

def scan_python_files(dirs: List[str], exclude: str) -> List[str]:
    """
    Recursively find all .py files, skipping site-packages & dist-packages or
    any path matching the exclude regex.
    """
    all_files = []
    pat = re.compile(exclude) if exclude else None
    for d in dirs:
        for root, _subdirs, files in os.walk(d):
            if "site-packages" in root or "dist-packages" in root:
                continue
            if pat and pat.search(root):
                continue
            for f in files:
                if f.endswith(".py"):
                    fp = os.path.join(root, f)
                    if pat and pat.search(fp):
                        continue
                    all_files.append(os.path.abspath(fp))
    return all_files
