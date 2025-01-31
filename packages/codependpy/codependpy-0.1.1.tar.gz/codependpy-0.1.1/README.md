# codependpy
> **A Python CLI tool for partial code extraction with dependency resolution.**  

[![PyPI](https://img.shields.io/pypi/v/codependpy.svg)](https://pypi.org/project/codependpy)
[![Python Version](https://img.shields.io/pypi/pyversions/codependpy.svg)](https://pypi.org/project/codependpy)
[![License](https://img.shields.io/pypi/l/codependpy.svg)](LICENSE)

---

## Overview

**codependpy** is a command-line tool that analyzes Python projects, traverses their **abstract syntax trees** (AST), and extracts *only* the classes and functions you need—along with their transitive dependencies. It supports **partial-file extraction** while still preventing you from missing dependencies. Whenever a reference can’t be resolved to a specific class/function, codependpy gracefully **falls back** to including the entire file, ensuring no key logic is left behind. 

This is perfect for:
- **Preparing minimal code contexts** for Large Language Models (LLMs) without shipping entire repositories.
- **Refactoring or debugging** large codebases, where you only need a few critical classes/functions (plus their dependencies).
- **Exploring** how code in a project is interconnected, focusing on usage-driven references.

---

## Key Features

1. **Selective AST-Based Extraction**  
   - Gathers references to classes/functions via `Name` and `Attribute` nodes.  
   - Navigates Django-specific calls like `apps.get_model("app_label","ModelName")`.  

2. **Intelligent Fallback**  
   - If code references a function name **not** found as a top-level `def` (e.g., it’s hidden behind a tricky import), codependpy pulls **the entire file** to guarantee coverage.  

3. **Support for Import Aliases**  
   - Recognizes `import mymodule as mm` or `from mymodule import Foo as Bar`, capturing partial references like `mm.Foo` or `Bar` within the code.  

4. **Recursive BFS**  
   - Every discovered reference triggers further scanning, so all transitively needed code is collected.  

5. **Django-Aware**  
   - Picks up dynamic model references from `apps.get_model(...)`.  
   - Handles typical `path(...)` and `re_path(...)` usage in Django’s `urls.py`.  

6. **Partial vs. Entire Files**  
   - By default, codependpy tries to export only the snippet for each class/function you actually reference.  
   - If it fails to find the function name in the AST, it imports the entire file.  

7. **Small, Modular Codebase**  
   - Each part of the logic (scanning, parsing, BFS, reconstruction) is in a separate file, making it easy to extend or debug.  

---

## Installation

```bash
pip install codependpy
```

> **Requirements**: Python 3.7+ (for `dataclasses` and up-to-date `ast` features).

---

## Usage

Once installed, you can run:

```bash
codependpy --search-dir <DIR> --target <FILE:SYMBOL1,SYMBOL2> [options...]
```

### Required Arguments

- `--target FILE:Symbol1,Symbol2`  
  The starting point(s) for BFS. If you omit `:SymbolList`, codependpy uses all top-level definitions in that file.  
  - Use multiple `--target` flags to specify multiple files or symbols.

### Optional Arguments

- `--search-dir DIR`  
  One or more directories in which to **search** for `.py` files. Defaults to `.` if not provided.  
- `--exclude "REGEX"`  
  Excludes any file/directory matching this pattern (e.g., `--exclude "migrations"`).  
- `--output PATH`  
  Where codependpy writes the final **partial extraction**. Defaults to `collected.py`.  

### Example Command

```bash
codependpy \
  --search-dir ./my_project \
  --exclude "tests|migrations" \
  --target "./my_project/app/models.py:UserModel,PostModel" \
  --target "./my_project/app/utils.py:helper_fn" \
  --output "./collected_snippets.py"
```

1. Recursively scans `./my_project` for `.py` files, ignoring paths that match `tests` or `migrations`.  
2. Reads definitions for `UserModel` and `PostModel` from `models.py` plus `helper_fn` from `utils.py`.  
3. Builds a BFS dependency graph, pulling in references from local modules, Django’s `apps.get_model`, etc.  
4. Outputs only the classes/functions you need into **`collected_snippets.py`**, plus essential top-level imports for each file.  
5. If a reference can’t be matched to a specific top-level function/class, the entire relevant file is included as a fallback.

---

## How It Works

1. **Scanning**  
   All `.py` files from your `search-dir` are discovered (skipping `site-packages` and `dist-packages`).  
2. **Parsing**  
   Each file is parsed into an AST using Python’s built-in `ast` module. codependpy collects:  
   - Top-level classes/functions (name, start line, end line).  
   - Import statements and their aliases.  
   - Django dynamic references (e.g., `apps.get_model`).  
   - URL references (e.g., `path('some-url', view)`).  
3. **Index Building**  
   A global “symbol index” is created, mapping symbol names → file(s) that define them.  
   A “module index” is created, mapping module import paths → file.  
4. **BFS**  
   Starting from each target class/function, codependpy recursively visits references discovered in that class/function’s body.  
   - For alias references (`import x as y`), it resolves `y.Thing` → symbol `Thing` in module `x`.  
   - For partial references that can’t be resolved, it pulls the entire file.  
5. **Reconstruction**  
   Each file is partially reconstructed. Only needed definitions (plus top-level imports) are included—**unless** we used the entire-file fallback.  

---

## Advanced Topics

- **Django Integration**  
  codependpy intercepts `apps.get_model("app_label","ModelName")`, linking it to local `app_label.models.py` so you can get that class.  
- **URL Patterns**  
  `path(...)` or `re_path(...)` references are also recognized, ensuring views are included if they’re local.  
- **Collision Mode**  
  If the same symbol is defined in multiple files, codependpy can either pick the *first* or *all* matching files. By default, it picks *all*.  
- **Fallback Full File**  
  Guarantee you never lose critical logic: if references can’t match an AST definition, codependpy includes the entire file.  

---

## Limitations

1. **No External Libraries**  
   codependpy doesn’t fetch code from actual `site-packages`. If references are from external libraries like `requests`, they’re excluded.  
2. **Complex Relative Imports**  
   Some tricky multi-level relative imports might need adjustments if your project’s structure is unusual.  
3. **Runtime Generators**  
   Dynamic code (`exec`, `eval`, metaclasses, etc.) can’t be fully tracked by static AST analysis.  
4. **Syntax Issues**  
   If your code has parse errors or incomplete imports, codependpy won’t see your definitions.  

---

## Contributing

Contributions, bug reports, and feature requests are welcome!  
1. **Fork** this repository.  
2. Create a new branch: `git checkout -b my-feature`  
3. Commit changes: `git commit -m 'Add some feature'`  
4. Open a **Pull Request**.

---

## Publishing to PyPI

1. Update `setup.py` or `pyproject.toml` with the correct metadata (name, version, author, etc.).  
2. Build the distribution:
   ```bash
   python -m build
   ```
3. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```
4. Once published, others can install via:
   ```bash
   pip install codependpy
   ```

---

## License

This project is licensed under the [MIT License](LICENSE).  
Feel free to modify and share—just give credit where it’s due!

---

**Happy partial extraction!**  

If you have any feedback or issues, open an [issue on GitHub](https://github.com/your-repo/codependpy/issues) or submit a pull request.  
