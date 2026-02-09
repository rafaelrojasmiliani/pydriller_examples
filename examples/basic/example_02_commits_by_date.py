#!/usr/bin/env python3
"""List commit hashes in a given date range.

This example filters commits by a recent window (default: last 30 days) and
prints a table of short commit hashes.
"""

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
from pydriller import Repository


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the date-range example.

    Returns:
        Parsed arguments containing the repository location and day window.
    """
    parser = argparse.ArgumentParser(
        description="List commit hashes filtered by date range.",
    )
    parser.add_argument(
        "repo",
        type=Path,
        help="Path or URL to the repository to traverse.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Number of days to look back from now.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the date-range example and print a formatted table.

    The date range is computed relative to the current UTC time.
    """
    args = parse_args()
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    rows: list[dict[str, str]] = []

    for commit in Repository(str(args.repo), since=since).traverse_commits():
        rows.append({"hash": commit.hash[:7]})

    if rows:
        table = pd.DataFrame(rows, columns=["hash"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
