#!/usr/bin/env python3
"""Export commit-level stats (files changed, insertions, deletions) to CSV.

This example traverses commits, captures summary stats, and writes a CSV file
that can be analyzed in pandas or spreadsheets.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from pydriller import Repository


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the commit stats CSV example.

    Returns:
        Parsed arguments containing the repository location and output path.
    """
    # Configure the CLI and return parsed arguments.
    parser = argparse.ArgumentParser(
        description="Export commit-level stats to a CSV file.",
    )
    parser.add_argument(
        "repo",
        type=Path,
        help="Path or URL to the repository to traverse.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("commit_stats.csv"),
        help="CSV output path.",
    )
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit(2)

    return parser.parse_args()


def main() -> None:
    """Run the commit stats example and write a CSV file."""
    args = parse_args()
    rows: list[dict[str, str | int]] = []

    # Traverse commits and capture summary stats for each one.
    for commit in Repository(str(args.repo)).traverse_commits():
        rows.append(
            {
                "hash": commit.hash[:7],
                "author": f"{commit.author.name} <{commit.author.email}>",
                "files_changed": commit.files,
                "insertions": commit.insertions,
                "deletions": commit.deletions,
            }
        )

    # Write the collected stats to CSV for downstream analysis.
    if rows:
        table = pd.DataFrame(
            rows,
            columns=["hash", "author", "files_changed", "insertions", "deletions"],
        )
        table.to_csv(args.output, index=False)
        print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
