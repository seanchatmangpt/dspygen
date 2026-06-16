"""
Document symbol provider for the dspygen LSP server.

Handles textDocument/documentSymbol.

Extracts:
- dspy.Module subclasses  → SymbolKind.Class (with method children)
- dspy.Signature subclasses → SymbolKind.Class
- All top-level class definitions → SymbolKind.Class
- All top-level function definitions → SymbolKind.Function
- forward() methods → SymbolKind.Method
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


def _range_for_node(node: ast.AST) -> lsp_types.Range:
    start_line = getattr(node, "lineno", 1) - 1
    start_col = getattr(node, "col_offset", 0)
    end_line = getattr(node, "end_lineno", start_line + 1) - 1
    end_col = getattr(node, "end_col_offset", start_col + 1)
    return lsp_types.Range(
        start=lsp_types.Position(line=start_line, character=start_col),
        end=lsp_types.Position(line=end_line, character=end_col),
    )


def _name_range_for_node(
    node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
) -> lsp_types.Range:
    """Range covering just the name identifier."""
    start_line = getattr(node, "lineno", 1) - 1
    start_col = getattr(node, "col_offset", 0)
    if isinstance(node, ast.ClassDef):
        keyword_len = len("class ")
    elif isinstance(node, ast.AsyncFunctionDef):
        keyword_len = len("async def ")
    else:
        keyword_len = len("def ")
    name_start = start_col + keyword_len
    name_end = name_start + len(node.name)
    return lsp_types.Range(
        start=lsp_types.Position(line=start_line, character=name_start),
        end=lsp_types.Position(line=start_line, character=name_end),
    )


def _make_function_symbol(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    is_method: bool = False,
) -> lsp_types.DocumentSymbol:
    kind = lsp_types.SymbolKind.Method if is_method else lsp_types.SymbolKind.Function
    return lsp_types.DocumentSymbol(
        name=node.name,
        kind=kind,
        range=_range_for_node(node),
        selection_range=_name_range_for_node(node),
    )


def _make_class_symbol(class_node: ast.ClassDef) -> lsp_types.DocumentSymbol:
    """Build a DocumentSymbol for a class with method/nested-class children."""
    children: list[lsp_types.DocumentSymbol] = []

    for item in class_node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            children.append(_make_function_symbol(item, is_method=True))
        elif isinstance(item, ast.ClassDef):
            children.append(_make_class_symbol(item))

    return lsp_types.DocumentSymbol(
        name=class_node.name,
        kind=lsp_types.SymbolKind.Class,
        range=_range_for_node(class_node),
        selection_range=_name_range_for_node(class_node),
        children=children if children else None,
    )


def _extract_symbols(source: str) -> list[lsp_types.DocumentSymbol]:
    """Parse *source* and return a top-level DocumentSymbol list."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    symbols: list[lsp_types.DocumentSymbol] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            symbols.append(_make_class_symbol(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(_make_function_symbol(node, is_method=False))

    return symbols


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_document_symbol(server: LanguageServer) -> None:
    """Register the textDocument/documentSymbol handler on *server*."""

    @server.feature(
        lsp_types.TEXT_DOCUMENT_DOCUMENT_SYMBOL,
        lsp_types.DocumentSymbolOptions(),
    )
    def on_document_symbol(
        params: lsp_types.DocumentSymbolParams,
    ) -> list[lsp_types.DocumentSymbol] | None:
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            return _extract_symbols(document.source)
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"document_symbol handler error: {exc}")
            return None
