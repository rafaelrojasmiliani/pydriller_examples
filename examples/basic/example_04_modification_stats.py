#!/usr/bin/env python3
"""List per-file modification stats for each commit.

This example traverses commits and prints a table of file paths with
added/removed line counts for each commit.
"""

import argparse
import sys
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
    """Parse command-line arguments for the modification stats example.

    Returns:
        Parsed arguments containing the repository location and optional
        max-count limit.
    """
    # Configure the CLI and return parsed arguments.
    parser = argparse.ArgumentParser(
        description="Show per-file added/removed line counts per commit.",
    )
    parser.add_argument(
        "repo",
        type=Path,
        help="Path to the local Git repository to traverse.",
    )
    parser.add_argument(
        "--max-count",
        type=int,
        default=None,
        help="Limit the number of commits processed.",
    )
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    validate_repo_path(args.repo, parser)
    return args


def main() -> None:
    """Run the modification stats example and print a formatted table."""
    args = parse_args()

    import pandas as pd
    from pydriller import Repository
    rows: list[dict[str, str | int]] = []
    count = 0

    # Traverse commits and collect per-file modification stats.
    for commit in Repository(str(args.repo)).traverse_commits():
        for modification in commit.modified_files:
            file_path = modification.new_path or modification.old_path or "<deleted>"
            rows.append(
                {
                    "hash": commit.hash[:7],
                    "file": file_path,
                    "added": modification.added_lines,
                    "removed": modification.deleted_lines,
                }
            )

        count += 1
        # Optional early-exit for faster exploration.
        if args.max_count is not None and count >= args.max_count:
            break

    # Render the collected rows as a table for readable output.
    if rows:
        table = pd.DataFrame(rows, columns=["hash", "file", "added", "removed"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
