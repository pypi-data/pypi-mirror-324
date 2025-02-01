#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import argparse

# Make sure we have pathspec installed:
#   pip install pathspec
try:
    import pathspec
except ImportError:
    print("Please install pathspec: pip install pathspec")
    sys.exit(1)


def load_gitignore(gitignore_path: Path):
    """Load the .gitignore file and return a pathspec object. If the file doesn't exist, return None."""
    if not gitignore_path.is_file():
        return None

    with gitignore_path.open("r", encoding="utf-8") as f:
        gitignore_content = f.read()

    return pathspec.PathSpec.from_lines("gitwildmatch", gitignore_content.splitlines())


def is_text_file(file_path: Path, chunk_size=1024) -> bool:
    """
    Check if the file appears to be text by trying to decode its first chunk as UTF-8.
    If this fails, assume it's binary and skip it.
    """
    try:
        with file_path.open("rb") as f:
            chunk = f.read(chunk_size)
        chunk.decode("utf-8")  # Raises UnicodeDecodeError if not text
        return True
    except (UnicodeDecodeError, PermissionError, OSError):
        # Binary or unreadable; treat as non-text
        return False


def build_pathspec(patterns):
    """
    Given a list of patterns (strings), build a pathspec object using 'gitwildmatch'.
    Returns None if the list is empty.
    """
    if not patterns:
        return None
    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)


def main():
    parser = argparse.ArgumentParser(
        description="Recursively export text files from a directory, "
        "respecting .gitignore, includes/excludes, etc. "
        "Binary files are always skipped."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to export. Defaults to current directory.",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1_000_000,  # 1 MB default
        help="Maximum file size (in bytes) to include. Default: 1,000,000 bytes = 1 MB.",
    )

    # Include/exclude patterns (multiple allowed via 'append')
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help=(
            "Pathspec pattern(s) to explicitly include. "
            "If provided, only files matching at least one pattern are kept. "
            "(Multiple can be specified, e.g. --include '*.py' --include 'dir1/**')"
        ),
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help=(
            "Pathspec pattern(s) to explicitly exclude. "
            "Files matching these patterns are removed from final results. "
            "(Multiple can be specified, e.g. --exclude 'docs/**')."
        ),
    )

    # Argument to write output to a file
    parser.add_argument(
        "-o",
        "--out-file",
        help="Write the extracted file contents to the specified file instead of stdout.",
    )

    # Argument to always print top N extracted files (by size) to the console
    parser.add_argument(
        "--top-n",
        type=int,
        default=None,
        help=(
            "List the top N extracted files by size (descending) to stdout at the end. "
            "This summary is always printed to console, even if --out-file is used."
        ),
    )

    args = parser.parse_args()

    # Resolve the target directory
    directory = Path(args.directory).resolve()

    # 1) Load .gitignore if present
    gitignore_path = directory / ".gitignore"
    gitignore_spec = load_gitignore(gitignore_path)

    # 2) Build pathspec objects for includes/excludes
    include_spec = build_pathspec(args.include)
    exclude_spec = build_pathspec(args.exclude)

    # We'll store a list of files that pass all checks
    extracted_files = []

    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        rel_root = root_path.relative_to(directory)

        # Prune subdirectories that match the exclude spec
        new_dirs = []
        for d in dirs:
            candidate = root_path / d
            rel_candidate = candidate.relative_to(directory)

            if exclude_spec and exclude_spec.match_file(str(rel_candidate)):
                continue
            new_dirs.append(d)
        dirs[:] = new_dirs

        # Now handle files in this directory
        for fname in files:
            file_path = root_path / fname
            rel_path_str = str(file_path.relative_to(directory))

            # 1) Check .gitignore
            if gitignore_spec and gitignore_spec.match_file(rel_path_str):
                continue

            # 2) If include patterns exist, skip file if it doesn't match any
            if include_spec and not include_spec.match_file(rel_path_str):
                continue

            # 3) Check exclude spec
            if exclude_spec and exclude_spec.match_file(rel_path_str):
                continue

            # 4) Check file size
            file_size = file_path.stat().st_size
            if file_size > args.max_size:
                continue

            # 5) Always skip binary files
            if not is_text_file(file_path):
                continue

            # Read file content
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                # Could not read file (permissions, etc.), skip
                continue

            # Store data for final output
            extracted_files.append(
                {"rel_path": rel_path_str, "size": file_size, "content": content}
            )

    # Build the text that represents all extracted files
    output_lines = []
    for item in extracted_files:
        output_lines.append(f"{item['rel_path']}\n```\n{item['content']}\n```\n\n")
    final_output = "".join(output_lines)

    # Write or print file contents
    if args.out_file:
        # Write to the specified file
        try:
            with open(args.out_file, "w", encoding="utf-8") as out_f:
                out_f.write(final_output)
        except Exception as e:
            print(f"Error writing to {args.out_file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to stdout
        print(final_output, end="")

    # Regardless of out-file usage, if --top-n was requested, print summary to console
    if args.top_n and args.top_n > 0 and extracted_files:
        # Sort extracted files by size descending
        sorted_files = sorted(extracted_files, key=lambda x: x["size"], reverse=True)
        top_files = sorted_files[: args.top_n]

        # Print summary to console (stdout)
        print(f"\nTop {args.top_n} extracted files by size (descending):")
        for fdata in top_files:
            print(f"{fdata['rel_path']} - {fdata['size']} bytes")
        print()  # extra newline


if __name__ == "__main__":
    main()
