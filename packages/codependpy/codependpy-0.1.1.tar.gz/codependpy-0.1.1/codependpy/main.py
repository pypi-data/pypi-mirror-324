# main.py
import sys
import logging
import time
import itertools

from .parse_args import parse_arguments, build_targets
from .file_scanner import scan_python_files
from .ast_parser import parse_file
from .index_builder import build_parsed_project
from .dependency_bfs import gather_definitions
from .code_reconstructor import reconstruct_code

logging.basicConfig(level=logging.INFO, format="%(message)s")


def main() -> None:
    args = parse_arguments()
    targets = build_targets(args.targets)

    logging.info("🔍 Searching for .py files...")
    pyfiles = scan_python_files(args.search_dir, args.exclude)
    logging.info(f"   Found {len(pyfiles)} files.")

    if not pyfiles:
        logging.error("No .py files found. Exiting.")
        sys.exit(1)

    # We'll do a little spinner while parsing files, just for fun:
    spinner = itertools.cycle(["⣷", "⣯", "⣟", "⡿", "⢿", "⣻"])
    logging.info("🗂 Parsing files... press Ctrl+C to cancel\n")
    file_map = {}
    for i, f in enumerate(pyfiles, start=1):
        # Print spinner
        sys.stdout.write(f"\r {next(spinner)}  Parsing {i}/{len(pyfiles)}")
        sys.stdout.flush()
        try:
            file_map[f] = parse_file(f)
        except Exception as e:
            logging.warning(f"\n⚠️  Skipping {f}, parse error => {e}")

    # Move to new line after spinner
    sys.stdout.write("\n\n")
    sys.stdout.flush()

    parsed = build_parsed_project(file_map, args.search_dir)

    logging.info(f"💡 Running BFS with depth={args.depth} for {len(targets)} target(s)...\n")
    needed = gather_definitions(parsed, tuple(targets), mode="all", max_depth=args.depth)

    logging.info("⚙️  Reconstructing code snippets...")
    final_snippets = reconstruct_code(needed, parsed.files)

    # Gather some summary stats:
    num_extracted_files = len(final_snippets)
    total_lines = 0
    for snippet in final_snippets.values():
        total_lines += snippet.count("\n")

    with open(args.output, "w", encoding="utf-8") as out:
        for fpath in sorted(final_snippets.keys()):
            out.write(f"# === Extracted from: {fpath}\n")
            out.write(final_snippets[fpath])
            out.write("\n\n")

    logging.info("✅ Done!")
    logging.info("🔎 Summary:")
    logging.info(f"   • Targets:      {len(targets)}")
    logging.info(f"   • BFS Depth:    {args.depth}")
    logging.info(f"   • Files Saved:  {num_extracted_files}")
    logging.info(f"   • Total Lines:  {total_lines}")
    logging.info(f"   • Output Path:  {args.output}")
    logging.info("🎉 Extraction finished successfully!\n")


if __name__ == "__main__":
    main()
