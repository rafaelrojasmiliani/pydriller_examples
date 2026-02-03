#!/usr/bin/env python3
"""List commit hashes in a given date range."""

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pydriller import Repository


def parse_args() -> argparse.Namespace:
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
    args = parse_args()
    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    for commit in Repository(str(args.repo), since=since).traverse_commits():
        print(commit.hash)


if __name__ == "__main__":
    main()
