#!/usr/bin/env python3
"""Summarize commits by author email.

This example filters commits by a specific author email and prints a table
showing the short hash, author identity, and modified file paths.
"""

import argparse
import sys
from pathlib import Path



def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the author filter example.

    Returns:
        Parsed arguments containing the repository location and author email.
    """
    # Configure the CLI and return parsed arguments.
    parser = argparse.ArgumentParser(
        description="Filter commits by author email and summarize changes.",
    )
    parser.add_argument(
        "repo",
        type=Path,
        help="Path or URL to the repository to traverse.",
    )
    parser.add_argument(
        "--author-email",
        help="Author email address to filter commits by.",
    )
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    return parser.parse_args()


def main() -> None:
    """Run the author filter example and print a formatted table."""
    args = parse_args()

    import pandas as pd
    from pydriller import Repository

    # If no author filter is provided, list all discovered authors.
    if not args.author_email:
        authors: set[str] = set()
        for commit in Repository(str(args.repo)).traverse_commits():
            authors.add(f"{commit.author.name} <{commit.author.email}>")

        rows = [{"author": author} for author in sorted(authors)]
        if rows:
            table = pd.DataFrame(rows, columns=["author"])
            print(table.to_string(index=False))
        return

    rows: list[dict[str, str]] = []

    # Traverse the repository and collect commits for the selected author.
    for commit in Repository(
        str(args.repo),
        only_authors=[args.author_email],
    ).traverse_commits():
        # Capture a short hash and a compact list of modified files.
        file_names = [mod.new_path or mod.old_path or "<deleted>" for mod in commit.modified_files]
        rows.append(
            {
                "hash": commit.hash[:7],
                "author": f"{commit.author.name} <{commit.author.email}>",
                "files": ", ".join(file_names),
            }
        )

    # Render the results with pandas for a readable, aligned table.
    if rows:
        table = pd.DataFrame(rows, columns=["hash", "author", "files"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
