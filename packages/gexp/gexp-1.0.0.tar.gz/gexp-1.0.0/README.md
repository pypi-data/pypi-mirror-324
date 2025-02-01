# gexp

**gexp** is a CLI tool to recursively export text files from a directory, while respecting `.gitignore`, allowing filtering via include/exclude patterns, limiting file size, and displaying the top N largest extracted files.

## Features

-   **Respects `.gitignore`** – Automatically skips files and directories listed in `.gitignore`.
-   **Recursive Export** – Scans all subdirectories and includes files matching criteria.
-   **Include/Exclude Filtering** – Use patterns to specify which files should be included or excluded.
-   **File Size Limit** – Skip files larger than a specified size.
-   **Binary File Detection** – Automatically skips binary files.
-   **Top-N Largest Files Listing** – Always prints the N largest extracted files to the console.
-   **Output to File** – Optionally write the extracted contents to a file.

## Installation

Install `gexp` from PyPI:

```bash
pip install gexp
```

## Usage

### Basic Usage

To export all text files from the current directory:

```bash
gexp
```

### Specify a Directory

To export from a specific directory:

```bash
gexp /path/to/directory
```

### Write Output to a File

To write the extracted files' content to a file instead of printing:

```bash
gexp -o output.txt
```

### Limit File Size

To skip files larger than 500 KB:

```bash
gexp --max-size 500000
```

### Filter by Name

```bash
gexp --include "*.py"
```

### Exclude Specific Directories or Files

To exclude all files in the `docs/` directory:

```bash
gexp --exclude "docs/**"
```

### Combine Include and Exclude

To export only `.py` files while excluding test files:

```bash
gexp --include "*.py" --exclude "test_*.py"
```

### Show Top N Largest Extracted Files

To print the **5 largest** extracted files:

```bash
gexp --top-n 5
```

### Full Example

Export only `.md` and `.txt` files, exclude the `node_modules/` folder, limit file size to 1 MB, and save output to `export.md`:

```bash
gexp --include "*.md" --include "*.txt" --exclude "node_modules/**" --max-size 1000000 -o export.md
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for more details.

## License

This project is licensed under the **MIT License**.

---

Happy exporting! 🚀
