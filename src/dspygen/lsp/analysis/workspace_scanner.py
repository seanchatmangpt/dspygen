"""
Workspace scanner for the dspygen LSP server.

Walks a workspace root and extracts class / function symbols from all Python
files using the standard ``ast`` module.  Results are cached by file mtime so
repeated calls are cheap.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path
from typing import TypedDict


class SymbolInfo(TypedDict):
    """Lightweight description of a single symbol extracted from a Python file."""

    name: str
    kind: str  # "class" | "function"
    line: int  # 1-based line number (matches ast node lineno)
    col: int   # 0-based column offset
    docstring: str


class WorkspaceScanner:
    """Scan a workspace root and extract symbols from Python source files.

    The scanner keeps an internal cache keyed by absolute file path.  Each
    cache entry stores the file's mtime at the time of the last scan and the
    extracted symbols.  Entries are invalidated automatically when the file is
    modified on disk.

    Example::

        scanner = WorkspaceScanner()
        symbols = scanner.scan(Path("/path/to/workspace"))
        for file_path, file_symbols in symbols.items():
            for sym in file_symbols:
                print(sym["name"], sym["kind"], sym["line"])
    """

    def __init__(self) -> None:
        # _cache: {abs_path_str -> (mtime_ns, list[SymbolInfo])}
        self._cache: dict[str, tuple[int, list[SymbolInfo]]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan(self, root: Path) -> dict[str, list[SymbolInfo]]:
        """Return a mapping of file path → list of symbols for all ``.py`` files under *root*.

        The mapping key is the **absolute** POSIX path string.  Results are
        cached by file mtime; only files that have changed since the last call
        are re-parsed.

        Parameters
        ----------
        root:
            Workspace root directory to scan.  Non-existent or non-directory
            paths are silently skipped.
        """
        root = root.resolve()
        if not root.is_dir():
            return {}

        result: dict[str, list[SymbolInfo]] = {}

        for py_file in self._iter_python_files(root):
            key = str(py_file)
            try:
                mtime_ns = py_file.stat().st_mtime_ns
            except OSError:
                continue

            cached_mtime, cached_symbols = self._cache.get(key, (-1, []))
            if mtime_ns == cached_mtime:
                result[key] = cached_symbols
            else:
                symbols = self._extract_symbols(py_file)
                self._cache[key] = (mtime_ns, symbols)
                result[key] = symbols

        return result

    def invalidate(self, path: Path) -> None:
        """Remove the cached entry for *path*, forcing a re-parse on next ``scan``."""
        self._cache.pop(str(path.resolve()), None)

    def clear(self) -> None:
        """Wipe the entire in-memory cache."""
        self._cache.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _iter_python_files(root: Path):
        """Yield all ``.py`` files under *root*, skipping hidden dirs and ``__pycache__``."""
        for dirpath, dirnames, filenames in os.walk(root):
            # Prune hidden directories and __pycache__ in-place so os.walk skips them
            dirnames[:] = [
                d for d in dirnames
                if not d.startswith(".") and d != "__pycache__"
            ]
            for fname in filenames:
                if fname.endswith(".py"):
                    yield Path(dirpath) / fname

    @staticmethod
    def _extract_symbols(path: Path) -> list[SymbolInfo]:
        """Parse *path* and return a list of :class:`SymbolInfo` dicts."""
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(path))
        except (SyntaxError, OSError):
            return []

        symbols: list[SymbolInfo] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                kind: str
                if isinstance(node, ast.ClassDef):
                    kind = "class"
                else:
                    kind = "function"

                docstring = ast.get_docstring(node) or ""

                symbols.append(
                    SymbolInfo(
                        name=node.name,
                        kind=kind,
                        line=node.lineno,
                        col=node.col_offset,
                        docstring=docstring,
                    )
                )

        return symbols
