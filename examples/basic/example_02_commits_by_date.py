#!/usr/bin/env python3
"""List commit hashes in a given date range.

This example filters commits by a recent window (default: last 30 days) and
prints a table of short commit hashes.
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path



def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the date-range example.

    Returns:
        Parsed arguments containing the repository location and day window.
    """
    # Configure the CLI and return parsed arguments.
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
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    return parser.parse_args()


def main() -> None:
    """Run the date-range example and print a formatted table.

    The date range is computed relative to the current UTC time.
    """
    args = parse_args()

    import pandas as pd
    from pydriller import Repository
    # Compute the lower bound for commit dates.
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    rows: list[dict[str, str]] = []

    # Traverse commits since the calculated date.
    for commit in Repository(str(args.repo), since=since).traverse_commits():
        # Keep a short hash and a formatted commit date for compact output.
        rows.append(
            {
                "hash": commit.hash[:7],
                "date": commit.committer_date.strftime("%Y/%m/%d %H:%M:%S"),
            }
        )

    # Render the collected hashes as a one-column table.
    if rows:
        table = pd.DataFrame(rows, columns=["hash", "date"])
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
