#!/usr/bin/env python3
"""Print commit hash, author, and message for a repository."""

import argparse
from pathlib import Path

import pandas as pd
from pydriller import Repository


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the commit overview example."""
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
    return parser.parse_args()


def main() -> None:
    """Run the commit overview example and print a formatted table."""
    args = parse_args()
    count = 0
    rows: list[dict[str, str]] = []

    for commit in Repository(str(args.repo)).traverse_commits():
        rows.append(
            {
                "hash": commit.hash[:7],
                "author": f"{commit.author.name} <{commit.author.email}>",
                "message": commit.msg.strip(),
            }
        )
        count += 1

        if args.max_count is not None and count >= args.max_count:
            break

    if rows:
        table = pd.DataFrame(rows, columns=["hash", "author", "message"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
