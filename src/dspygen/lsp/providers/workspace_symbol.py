"""
Workspace symbol provider for the dspygen LSP server.

Handles workspace/symbol.

Builds a workspace-level symbol index by scanning all Python files, then
returns matches for a client query string.  Prioritises dspygen module
classes and dspy.Signature subclasses.
"""

from __future__ import annotations

import ast
import threading
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Workspace index (built lazily on first query)
# ---------------------------------------------------------------------------


class _SymbolEntry:
    __slots__ = ("name", "kind", "file_path", "line", "col", "priority")

    def __init__(
        self,
        name: str,
        kind: lsp_types.SymbolKind,
        file_path: str,
        line: int,
        col: int,
        priority: int = 0,
    ) -> None:
        self.name = name
        self.kind = kind
        self.file_path = file_path
        self.line = line
        self.col = col
        self.priority = priority  # higher = ranked first


class _WorkspaceIndex:
    def __init__(self) -> None:
        self._entries: list[_SymbolEntry] = []
        self._lock = threading.Lock()
        self._built = False

    def build(self, root_paths: list[str]) -> None:
        entries: list[_SymbolEntry] = []
        for root_path in root_paths:
            root = Path(root_path)
            if not root.is_dir():
                continue
            for py_file in sorted(root.rglob("*.py")):
                try:
                    source = py_file.read_text(encoding="utf-8", errors="replace")
                    entries.extend(_index_file(py_file, source))
                except Exception as exc:  # noqa: BLE001
                    logger.debug(f"workspace_symbol: could not index {py_file}: {exc}")

        with self._lock:
            self._entries = entries
            self._built = True

        logger.info(f"workspace_symbol: indexed {len(entries)} symbols")

    def search(self, query: str, limit: int = 100) -> list[_SymbolEntry]:
        q = query.lower()
        with self._lock:
            matched = [e for e in self._entries if q in e.name.lower()]
        # Sort by priority descending, then alphabetically
        matched.sort(key=lambda e: (-e.priority, e.name.lower()))
        return matched[:limit]


_INDEX = _WorkspaceIndex()
_INDEX_LOCK = threading.Lock()


def _base_names(class_node: ast.ClassDef) -> list[str]:
    names: list[str] = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(f"{ast.unparse(base.value)}.{base.attr}")
    return names


def _index_file(path: Path, source: str) -> list[_SymbolEntry]:
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []

    entries: list[_SymbolEntry] = []
    file_str = str(path.resolve())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = _base_names(node)
            is_dspy_module = any(b in ("Module", "dspy.Module") for b in bases)
            is_dspy_sig = any(b in ("Signature", "dspy.Signature") for b in bases)
            priority = 2 if is_dspy_module else (1 if is_dspy_sig else 0)
            entries.append(
                _SymbolEntry(
                    name=node.name,
                    kind=lsp_types.SymbolKind.Class,
                    file_path=file_str,
                    line=node.lineno - 1,
                    col=node.col_offset,
                    priority=priority,
                )
            )
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            entries.append(
                _SymbolEntry(
                    name=node.name,
                    kind=lsp_types.SymbolKind.Function,
                    file_path=file_str,
                    line=node.lineno - 1,
                    col=node.col_offset,
                )
            )

    return entries


def _ensure_index(server: LanguageServer) -> None:
    """Build the index if it hasn't been built yet."""
    with _INDEX_LOCK:
        if _INDEX._built:
            return
        # Collect workspace root folders
        roots: list[str] = []
        try:
            for folder in (server.workspace.folders or {}).values():
                uri = folder.uri if hasattr(folder, "uri") else str(folder)
                if uri.startswith("file://"):
                    roots.append(uri[len("file://"):])
        except Exception:  # noqa: BLE001
            pass
        if not roots:
            # Fall back to dspygen package root
            here = Path(__file__).resolve().parent.parent.parent  # src/dspygen
            roots = [str(here)]
        _INDEX.build(roots)


def _to_workspace_symbol(entry: _SymbolEntry) -> lsp_types.WorkspaceSymbol:
    location = lsp_types.Location(
        uri=Path(entry.file_path).as_uri(),
        range=lsp_types.Range(
            start=lsp_types.Position(line=entry.line, character=entry.col),
            end=lsp_types.Position(line=entry.line, character=entry.col + len(entry.name)),
        ),
    )
    return lsp_types.WorkspaceSymbol(
        name=entry.name,
        kind=entry.kind,
        location=location,
    )


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_workspace_symbol(server: LanguageServer) -> None:
    """Register the workspace/symbol handler on *server*."""

    @server.feature(
        lsp_types.WORKSPACE_SYMBOL,
        lsp_types.WorkspaceSymbolOptions(),
    )
    def on_workspace_symbol(
        params: lsp_types.WorkspaceSymbolParams,
    ) -> list[lsp_types.WorkspaceSymbol] | None:
        try:
            _ensure_index(server)
            query = params.query or ""
            entries = _INDEX.search(query)
            return [_to_workspace_symbol(e) for e in entries]
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"workspace_symbol handler error: {exc}")
            return None
