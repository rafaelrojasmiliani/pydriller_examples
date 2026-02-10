#!/usr/bin/env python3
"""Print commit hash, author, and message for a repository.

This example traverses a repository's commits and renders a compact table
with a short hash, the author identity, and the commit message.
"""

import argparse
import sys
from pathlib import Path



def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the commit overview example.

    Returns:
        Parsed arguments containing the repository location and optional
        max-count limit.
    """
    # Configure the CLI and return parsed arguments.
    parser = argparse.ArgumentParser(
        description="Traverse commits and print hash, author, and message.",
    )
    parser.add_argument(
        "repo",
        type=Path,
        help="Path or URL to the repository to traverse.",
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

    return parser.parse_args()


def main() -> None:
    """Run the commit overview example and print a formatted table.

    The output is rendered with pandas to make the commit data easy to scan.
    """
    args = parse_args()

    import pandas as pd
    from pydriller import Repository
    count = 0
    rows: list[dict[str, str]] = []

    # Walk all commits in the repository and collect summary fields.
    for commit in Repository(str(args.repo)).traverse_commits():
        # Store a short hash to keep the table compact.
        rows.append(
            {
                "hash": commit.hash[:7],
                "author": f"{commit.author.name} <{commit.author.email}>",
                "message": commit.msg.strip(),
            }
        )
        count += 1

        # Optional early-exit for fast exploration.
        if args.max_count is not None and count >= args.max_count:
            break

    # Render the collected rows as a table for readable output.
    if rows:
        table = pd.DataFrame(rows, columns=["hash", "author", "message"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
