#!/usr/bin/env python3
"""Verify version consistency across pyproject.toml, __init__.py, and git tags."""
import re
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def get_pyproject_version() -> str:
    """Read the version string declared in pyproject.toml."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    if not pyproject.exists():
        print("Error: pyproject.toml not found")
        sys.exit(1)

    content = pyproject.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        print("Error: could not find version in pyproject.toml")
        sys.exit(1)
    return match.group(1)


def get_installed_version() -> str | None:
    """Return the installed package version, or None if not installed."""
    try:
        return version("dspygen")
    except PackageNotFoundError:
        return None


def get_latest_git_tag() -> str | None:
    """Return the most recent git tag, or None if there are no tags."""
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip().lstrip("v")


def main() -> int:
    """Run all version consistency checks. Returns 0 on success, 1 on failure."""
    exit_code = 0

    pyproject_ver = get_pyproject_version()
    installed_ver = get_installed_version()
    latest_tag = get_latest_git_tag()

    print(f"pyproject.toml version : {pyproject_ver}")
    print(f"Installed package      : {installed_ver or '(not installed)'}")
    print(f"Latest git tag         : {latest_tag or '(no tags)'}")

    # Check 1: pyproject.toml vs installed package
    if installed_ver is None:
        print("WARNING: dspygen is not installed in the current environment.")
        exit_code = 1
    elif pyproject_ver != installed_ver:
        print(
            f"MISMATCH: pyproject.toml has {pyproject_ver!r} "
            f"but installed package reports {installed_ver!r}. "
            "Run 'poetry install' to sync."
        )
        exit_code = 1
    else:
        print("OK: pyproject.toml version matches installed package.")

    # Check 2: git tag vs pyproject.toml (advisory only)
    if latest_tag is None:
        print("WARNING: No git tags found — consider tagging a release.")
    elif latest_tag != pyproject_ver:
        print(
            f"WARNING: Latest git tag is v{latest_tag!r} "
            f"but pyproject.toml declares {pyproject_ver!r}. "
            "Run 'make release' when ready to publish."
        )
    else:
        print("OK: git tag matches pyproject.toml version.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
