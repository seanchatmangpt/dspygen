#!/usr/bin/env python3
"""Bump dspygen version in pyproject.toml."""
import re
import subprocess
import sys
from pathlib import Path


def bump(part: str = "patch") -> str:
    """Bump the version in pyproject.toml and commit the change.

    Args:
        part: Which version component to bump — 'patch', 'minor', or 'major'.

    Returns:
        The new version string.
    """
    if part not in ("patch", "minor", "major"):
        print(f"Error: part must be one of patch/minor/major, got '{part}'")
        sys.exit(1)

    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    if not pyproject.exists():
        print(f"Error: pyproject.toml not found at {pyproject}")
        sys.exit(1)

    content = pyproject.read_text()

    # Extract current version from [tool.poetry] section
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        print("Error: could not find version in pyproject.toml")
        sys.exit(1)

    current = match.group(1)
    # Support both semver (X.Y.Z) and CalVer-style (YYYY.M.D) formats
    parts = current.split(".")
    if len(parts) < 3:
        print(f"Error: version '{current}' does not have at least 3 components")
        sys.exit(1)

    major, minor, patch_num = int(parts[0]), int(parts[1]), int(parts[2])

    if part == "major":
        major += 1
        minor = 0
        patch_num = 0
    elif part == "minor":
        minor += 1
        patch_num = 0
    else:  # patch
        patch_num += 1

    new_version = f"{major}.{minor}.{patch_num}"

    # Write updated version back to pyproject.toml
    new_content = re.sub(
        r'^(version\s*=\s*)"[^"]+"',
        f'\\1"{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    pyproject.write_text(new_content)
    print(f"Bumped version: {current} -> {new_version}")

    # Re-lock dependencies without updating them
    print("Running poetry lock --no-update ...")
    subprocess.run(["poetry", "lock", "--no-update"], check=True)

    # Stage the changed files
    subprocess.run(
        ["git", "add", "pyproject.toml", "poetry.lock"],
        check=True,
        cwd=pyproject.parent,
    )

    # Commit
    subprocess.run(
        ["git", "commit", "-m", f"chore: bump version to {new_version}"],
        check=True,
        cwd=pyproject.parent,
    )
    print(f"Committed version bump to {new_version}")
    return new_version


if __name__ == "__main__":
    part_arg = sys.argv[1] if len(sys.argv) > 1 else "patch"
    bump(part_arg)
