<<<<<<< HEAD
#!/usr/bin/env python3
"""Print commit hash, author, and message for a repository.

This minimal example shows how to traverse commits in a repository and
print key metadata for each one.
"""

import argparse
import sys
from pathlib import Path



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
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    return parser.parse_args()


def main() -> None:
    """Run the commit overview example and print commit metadata."""
    args = parse_args()

    from pydriller import Repository
    count = 0

    # Traverse commits in the repository and print the main fields.
    for commit in Repository(str(args.repo)).traverse_commits():
        # Use the full hash for clarity in this minimal example.
        print(f"{commit.hash} | {commit.author.name} <{commit.author.email}>")
        print(f"    {commit.msg.strip()}")
        count += 1

        # Stop early if a max count was provided.
        if args.max_count is not None and count >= args.max_count:
            break


if __name__ == "__main__":
    main()
||||||| 252cc15
=======
#!/usr/bin/env python3
"""Print commit hash, author, and message for a repository.

This minimal example shows how to traverse commits in a repository and
print key metadata for each one.
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
    """Parse command-line arguments for the commit overview example."""
    parser = argparse.ArgumentParser(
        description="Traverse commits and print hash, author, and message.",
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
    """Run the commit overview example and print commit metadata."""
    args = parse_args()

    from pydriller import Repository
    count = 0

    # Traverse commits in the repository and print the main fields.
    for commit in Repository(str(args.repo)).traverse_commits():
        # Use the full hash for clarity in this minimal example.
        print(f"{commit.hash} | {commit.author.name} <{commit.author.email}>")
        print(f"    {commit.msg.strip()}")
        count += 1

        # Stop early if a max count was provided.
        if args.max_count is not None and count >= args.max_count:
            break


if __name__ == "__main__":
    main()
>>>>>>> codex/provide-basic-pydrill-usage-examples-l99v8w
