# Basic examples

Minimal scripts that show how to clone and traverse a repository with PyDriller.

## Example scripts

### Example 01: Commit overview

**Script:** `example_01_commit_overview.py`

Traverse commits in a repository and print a table with the hash, author, and message.

**Usage**

```bash
python examples/basic/example_01_commit_overview.py /path/to/repo --max-count 10
```

### Example 02: Commits in a date range

**Script:** `example_02_commits_by_date.py`

Filter commits by date range (e.g., last 30 days) and list commit hashes in a table.

**Usage**

```bash
python examples/basic/example_02_commits_by_date.py /path/to/repo --days 30
```

## Example ideas

1. Traverse commits in a single repository and print the commit hash, author, and message.
2. Filter commits by date range (e.g., last 30 days) and list the commit hashes.
3. Filter commits by author email and summarize each commit’s changed files.
4. Iterate over file modifications in each commit and print file paths with added/removed line counts.
5. Clone a remote repository to a temporary directory and run a basic commit traversal.
6. Extract commit-level stats (files changed, insertions, deletions) and export to CSV.
7. Build a map keyed by file path where each value is the list of commits that modified that file.
