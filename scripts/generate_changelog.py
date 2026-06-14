#!/usr/bin/env python3
"""Generate CHANGELOG.md from git log since last tag."""
import subprocess
import sys
from datetime import date
from pathlib import Path


def get_last_tag() -> str | None:
    """Return the most recent git tag, or None if none exist."""
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_commits_since(tag: str | None) -> list[str]:
    """Return one-line commit messages since *tag* (or all commits if no tag)."""
    if tag:
        rev_range = f"{tag}..HEAD"
    else:
        rev_range = "HEAD"

    result = subprocess.run(
        ["git", "log", "--oneline", "--no-merges", rev_range],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines


def categorise(commits: list[str]) -> dict[str, list[str]]:
    """Group commits by conventional-commit prefix."""
    categories: dict[str, list[str]] = {
        "Features": [],
        "Bug Fixes": [],
        "Chores": [],
        "Documentation": [],
        "Other": [],
    }
    prefix_map = {
        "feat": "Features",
        "fix": "Bug Fixes",
        "chore": "Chores",
        "docs": "Documentation",
        "doc": "Documentation",
        "refactor": "Other",
        "test": "Other",
        "ci": "Other",
        "style": "Other",
        "perf": "Other",
        "build": "Other",
    }
    for commit in commits:
        # Strip the short hash (first word)
        parts = commit.split(None, 1)
        message = parts[1] if len(parts) > 1 else commit
        placed = False
        for prefix, category in prefix_map.items():
            if message.lower().startswith(f"{prefix}:") or message.lower().startswith(
                f"{prefix}("
            ):
                categories[category].append(message)
                placed = True
                break
        if not placed:
            categories["Other"].append(message)
    return categories


def format_changelog(
    categories: dict[str, list[str]],
    tag: str | None,
    today: str,
) -> str:
    """Render the changelog section as Markdown."""
    version_header = tag if tag else "Unreleased"
    lines = [
        f"# Changelog\n",
        f"## [{version_header}] — {today}\n",
    ]
    for heading, commits in categories.items():
        if not commits:
            continue
        lines.append(f"### {heading}\n")
        for msg in commits:
            lines.append(f"- {msg}")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    """Entry point: write CHANGELOG.md to the repo root."""
    repo_root = Path(__file__).parent.parent
    changelog_path = repo_root / "CHANGELOG.md"

    last_tag = get_last_tag()
    commits = get_commits_since(last_tag)

    if not commits:
        print("No new commits since last tag — nothing to write.")
        sys.exit(0)

    categories = categorise(commits)
    today = date.today().isoformat()
    content = format_changelog(categories, last_tag, today)

    # Prepend to existing changelog (or create new)
    existing = ""
    if changelog_path.exists():
        existing_text = changelog_path.read_text()
        # Avoid duplicating the header
        if existing_text.startswith("# Changelog"):
            existing = existing_text[len("# Changelog\n"):].lstrip("\n")
        else:
            existing = existing_text

    # Write: new entry on top, old content below
    new_text = content
    if existing:
        new_text = content.rstrip("\n") + "\n\n---\n\n" + existing

    changelog_path.write_text(new_text)
    print(f"Wrote changelog to {changelog_path}")
    print(f"Included {sum(len(v) for v in categories.values())} commits.")


if __name__ == "__main__":
    main()
