#!/usr/bin/env python3
"""Build a map of files to the commits that modified them.

This example groups commit hashes by file path to show change history per file.
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path


def validate_repo_path(repo: Path, parser: argparse.ArgumentParser) -> None:
    """Validate that repo exists, is a directory, and is a Git repository."""
    if not repo.exists():
        parser.error(f"Repository path does not exist: {repo}")

    if not repo.is_dir():
        parser.error(f"Repository path is not a directory: {repo}")

    import subprocess

    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or result.stdout.strip() != "true":
        parser.error(f"Repository path is not a valid Git repository: {repo}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the file commit map example.

    Returns:
        Parsed arguments containing the repository location.
    """
    # Configure the CLI and return parsed arguments.
    parser = argparse.ArgumentParser(
        description="Map files to the commits that modified them.",
    )
    parser.add_argument(
        "repo",
        type=Path,
        help="Path or URL to the repository to traverse.",
    )
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    validate_repo_path(args.repo, parser)
    return args


def main() -> None:
    """Run the file commit map example and print a formatted table."""
    args = parse_args()

    import pandas as pd
    from pydriller import Repository
    file_to_commits: dict[str, list[str]] = defaultdict(list)

    # Traverse commits and add each short hash to the file's history.
    for commit in Repository(str(args.repo)).traverse_commits():
        short_hash = commit.hash[:7]
        for modification in commit.modified_files:
            file_path = modification.new_path or modification.old_path or "<deleted>"
            file_to_commits[file_path].append(short_hash)

    # Convert the mapping into rows for a readable table output.
    rows: list[dict[str, str]] = []
    for file_path, hashes in sorted(file_to_commits.items()):
        rows.append({"file": file_path, "commits": ", ".join(hashes)})

    # Render the file/commit mapping using pandas for aligned output.
    if rows:
        table = pd.DataFrame(rows, columns=["file", "commits"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
