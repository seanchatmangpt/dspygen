"""
Folding range provider for the dspygen LSP server.

Handles textDocument/foldingRange.

Defines foldable regions for:
- dspy.Module subclasses → class body
- forward() methods → method body
- dspy.Signature subclasses → signature definition
- Multi-line string literals (docstrings, signature strings)
"""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _base_names(class_node: ast.ClassDef) -> list[str]:
    names: list[str] = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
    return names


def _is_dspy_module(class_node: ast.ClassDef) -> bool:
    return any(b in ("Module", "dspy.Module") for b in _base_names(class_node))


def _is_dspy_signature(class_node: ast.ClassDef) -> bool:
    return any(b in ("Signature", "dspy.Signature") for b in _base_names(class_node))


def _fold_node(node: ast.AST) -> lsp_types.FoldingRange | None:
    """Return a FoldingRange for a multi-line AST node."""
    start = getattr(node, "lineno", None)
    end = getattr(node, "end_lineno", None)
    if start is None or end is None:
        return None
    start_line = start - 1  # 0-based
    end_line = end - 1
    if end_line <= start_line:
        return None
    return lsp_types.FoldingRange(
        start_line=start_line,
        end_line=end_line,
        kind=lsp_types.FoldingRangeKind.Region,
    )


def _collect_multiline_strings(tree: ast.Module) -> list[lsp_types.FoldingRange]:
    """Return folding ranges for multi-line string constant nodes."""
    ranges: list[lsp_types.FoldingRange] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                fr = _fold_node(node)
                if fr:
                    ranges.append(fr)
    return ranges


def _extract_folding_ranges(source: str) -> list[lsp_types.FoldingRange]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    ranges: list[lsp_types.FoldingRange] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Fold the class itself
            fr = _fold_node(node)
            if fr:
                ranges.append(fr)

            # Fold forward() method bodies
            for item in node.body:
                if (
                    isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and item.name == "forward"
                ):
                    fr = _fold_node(item)
                    if fr:
                        ranges.append(fr)

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Top-level functions
            fr = _fold_node(node)
            if fr:
                ranges.append(fr)

    # Multi-line string literals
    ranges.extend(_collect_multiline_strings(tree))

    return ranges


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_folding_range(server: LanguageServer) -> None:
    """Register the textDocument/foldingRange handler on *server*."""

    @server.feature(lsp_types.TEXT_DOCUMENT_FOLDING_RANGE)
    def on_folding_range(
        params: lsp_types.FoldingRangeParams,
    ) -> list[lsp_types.FoldingRange] | None:
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            return _extract_folding_ranges(document.source)
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"folding_range handler error: {exc}")
            return None
