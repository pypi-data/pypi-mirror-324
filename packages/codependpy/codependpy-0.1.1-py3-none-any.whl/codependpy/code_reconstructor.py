from typing import Dict, Set
from collections import defaultdict
from .project_types import FileInfo

def reconstruct_code(
    needed: Dict[str, Set[str]],
    files: Dict[str, FileInfo]
) -> Dict[str, str]:
    """
    For each file -> set of needed definitions:
      - We gather the lines for each method/func definition individually.
      - If a definition is "MyClass", we add the class declaration line + any base classes lines,
        but not all methods automatically, only the ones specifically needed.

    We'll group methods that share the same parent class under that class block.
    """
    results = {}
    for fpath, required_syms in needed.items():
        if not required_syms:
            continue
        info = files[fpath]
        # We group needed definitions by their parent class
        # e.g. "MyClass" or None for top-level
        grouped = defaultdict(list)
        for sym in required_syms:
            defi = info.definitions[sym]
            grouped[defi.parent].append(defi)

        # Now build the output lines
        lines_out = []
        # Step 1: gather top-level imports if you want them at the top
        # We'll do so by scanning lines until the first definition starts
        earliest_line = min(d.start_line for d in info.definitions.values()) if info.definitions else 999999
        for i, line in enumerate(info.source_lines, start=1):
            if i >= earliest_line:
                break
            ls = line.strip()
            if ls.startswith("import ") or ls.startswith("from "):
                lines_out.append(line)

        # Step 2: for each parent group, we either:
        #  - if parent is None => it's a top-level function
        #  - if parent is a class => we reconstruct the class line, then only the needed methods
        for parent, definitions in grouped.items():
            if parent is None:
                # these are top-level defs
                for d in sorted(definitions, key=lambda x: x.start_line):
                    snippet = info.source_lines[d.start_line - 1: d.end_line]
                    lines_out.extend(snippet)
                    if not snippet[-1].endswith("\n"):
                        lines_out.append("\n")
                lines_out.append("\n")
            else:
                # we have methods for a specific class
                # first we need the class definition snippet (just the class line + maybe bases)
                # we can slice from the class's start_line up to the line right before its first method
                class_def = info.definitions[parent]
                # We'll output "class MyClass(...):" line(s)
                class_header_lines = info.source_lines[class_def.start_line - 1: class_def.start_line]
                lines_out.extend(class_header_lines)
                if not class_header_lines or not class_header_lines[-1].endswith("\n"):
                    lines_out.append("\n")

                # We need to indent methods properly. Let's gather them in ascending order:
                definitions.sort(key=lambda x: x.start_line)
                for d in definitions:
                    snippet = info.source_lines[d.start_line - 1: d.end_line]
                    lines_out.extend(snippet)
                    if not snippet[-1].endswith("\n"):
                        lines_out.append("\n")
                lines_out.append("\n")  # spacing after the class block

        results[fpath] = "".join(lines_out)

    return results
