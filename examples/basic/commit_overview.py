#!/usr/bin/env python3
"""Print commit hash, author, and message for a repository."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydriller import Repository


def parse_args() -> argparse.Namespace:
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
    args = parse_args()
    count = 0

    for commit in Repository(str(args.repo)).traverse_commits():
        print(f"{commit.hash} | {commit.author.name} <{commit.author.email}>")
        print(f"    {commit.msg.strip()}")
        count += 1

        if args.max_count is not None and count >= args.max_count:
            break


if __name__ == "__main__":
    main()
