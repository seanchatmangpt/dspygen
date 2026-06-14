"""Simple snapshot testing utilities for dspygen.

Snapshot tests capture module output on first run and compare against it on
subsequent runs.  Set the environment variable ``UPDATE_SNAPSHOTS=1`` to
regenerate all snapshots.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest


class SnapshotStore:
    """Store and compare module outputs against persisted snapshots.

    Snapshots are plain text files stored under ``snapshot_dir``.  Each
    snapshot is identified by a unique *name* and stored as
    ``<snapshot_dir>/<name>.txt``.

    Args:
        snapshot_dir: Directory in which snapshot files are stored.  Will be
            created on first use if it does not exist.

    Example::

        store = SnapshotStore(Path("tests/snapshots"))
        store.assert_matches_snapshot("my_module_output", "Hello, world!")
    """

    def __init__(self, snapshot_dir: Path) -> None:
        self.snapshot_dir = Path(snapshot_dir)
        self.update_snapshots: bool = os.environ.get("UPDATE_SNAPSHOTS", "0") == "1"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def assert_matches_snapshot(self, name: str, value: str) -> None:
        """Compare *value* to the stored snapshot named *name*.

        On the **first run** (or when ``UPDATE_SNAPSHOTS=1`` is set in the
        environment), the snapshot is created/updated and the assertion
        trivially passes.

        On subsequent runs the stored value is compared to *value* using a
        plain string equality check; a mismatch raises :class:`AssertionError`
        with a diff-friendly message.

        Args:
            name: Unique identifier for this snapshot (used as the filename
                stem, so avoid characters that are invalid in filenames).
            value: The actual value to store or compare.

        Raises:
            AssertionError: If *value* does not match the stored snapshot.

        Example::

            store.assert_matches_snapshot("summary_output", result.summary)
        """
        snapshot_path = self._snapshot_path(name)

        if self.update_snapshots or not snapshot_path.exists():
            self._write(snapshot_path, value)
            return  # Creating/updating — nothing to compare

        stored = snapshot_path.read_text(encoding="utf-8")
        assert value == stored, (
            f"Snapshot mismatch for {name!r}.\n"
            f"  Snapshot file: {snapshot_path}\n"
            f"  Expected (stored):\n{_indent(stored)}\n"
            f"  Actual:\n{_indent(value)}\n"
            f"  Tip: set UPDATE_SNAPSHOTS=1 to regenerate."
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _snapshot_path(self, name: str) -> Path:
        """Return the Path for a given snapshot *name*."""
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        return self.snapshot_dir / f"{name}.txt"

    def _write(self, path: Path, value: str) -> None:
        """Write *value* to *path*, creating parent directories as needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")


def _indent(text: str, prefix: str = "    ") -> str:
    """Indent every line of *text* with *prefix* for readable diff output."""
    return "\n".join(f"{prefix}{line}" for line in text.splitlines())


# ---------------------------------------------------------------------------
# Pytest fixture
# ---------------------------------------------------------------------------

@pytest.fixture()
def snapshot(tmp_path: Path) -> SnapshotStore:
    """Provide a :class:`SnapshotStore` instance for the current test.

    Snapshots are stored under a ``snapshots/`` sub-directory of the project
    root (next to ``tests/``).  The ``tmp_path`` fixture is accepted so pytest
    can inject it, but snapshot files are *not* stored in ``tmp_path`` — they
    are persisted across runs.

    Set ``UPDATE_SNAPSHOTS=1`` in your environment to regenerate all snapshots.

    Example::

        def test_module_output(snapshot):
            result = my_module(input="hello")
            snapshot.assert_matches_snapshot("my_module_hello", result.output)
    """
    # Persist snapshots alongside the tests directory for version-control
    # friendliness.  Walk up from the tmp_path to find the repo root.
    repo_root = _find_repo_root(tmp_path) or tmp_path
    snapshot_dir = repo_root / "tests" / "snapshots"
    return SnapshotStore(snapshot_dir)


def _find_repo_root(start: Path) -> Path | None:
    """Walk up from *start* looking for a ``pyproject.toml`` or ``.git`` marker."""
    current = start
    for _ in range(20):  # cap the search depth
        if (current / "pyproject.toml").exists() or (current / ".git").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None
