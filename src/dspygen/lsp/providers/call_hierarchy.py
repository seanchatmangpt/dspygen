"""
Call hierarchy provider for the dspygen LSP server.

Handles:
- textDocument/prepareCallHierarchy
- callHierarchy/incomingCalls
- callHierarchy/outgoingCalls

For dspygen module classes:
- Incoming: all places the class is instantiated (within the workspace)
- Outgoing: dspy.Predict, dspy.ChainOfThought, other module calls inside forward()
- Pipeline: | operator chains are represented as outgoing calls
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_IDENT_RE = re.compile(r"\b([A-Za-z_]\w*)\b")


def _range_for_node(node: ast.AST) -> lsp_types.Range:
    start_line = getattr(node, "lineno", 1) - 1
    start_col = getattr(node, "col_offset", 0)
    end_line = getattr(node, "end_lineno", start_line + 1) - 1
    end_col = getattr(node, "end_col_offset", start_col + 1)
    return lsp_types.Range(
        start=lsp_types.Position(line=start_line, character=start_col),
        end=lsp_types.Position(line=end_line, character=end_col),
    )


def _name_range(node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef) -> lsp_types.Range:
    start_line = getattr(node, "lineno", 1) - 1
    start_col = getattr(node, "col_offset", 0)
    if isinstance(node, ast.ClassDef):
        kw_len = len("class ")
    elif isinstance(node, ast.AsyncFunctionDef):
        kw_len = len("async def ")
    else:
        kw_len = len("def ")
    name_start = start_col + kw_len
    return lsp_types.Range(
        start=lsp_types.Position(line=start_line, character=name_start),
        end=lsp_types.Position(line=start_line, character=name_start + len(node.name)),
    )


def _zero_range() -> lsp_types.Range:
    return lsp_types.Range(
        start=lsp_types.Position(line=0, character=0),
        end=lsp_types.Position(line=0, character=0),
    )


def _word_at(source: str, position: lsp_types.Position) -> str:
    lines = source.splitlines()
    if position.line >= len(lines):
        return ""
    line = lines[position.line]
    col = position.character
    for m in _IDENT_RE.finditer(line):
        if m.start() <= col <= m.end():
            return m.group(1)
    return ""


def _base_names(class_node: ast.ClassDef) -> list[str]:
    names: list[str] = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
    return names


def _find_class_node(source: str, name: str) -> ast.ClassDef | None:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _find_forward_node(
    class_node: ast.ClassDef,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for item in class_node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "forward":
            return item
    return None


# ---------------------------------------------------------------------------
# Build CallHierarchyItem
# ---------------------------------------------------------------------------


def _make_item(
    name: str,
    kind: lsp_types.SymbolKind,
    uri: str,
    range_: lsp_types.Range,
    selection_range: lsp_types.Range,
    detail: str = "",
) -> lsp_types.CallHierarchyItem:
    return lsp_types.CallHierarchyItem(
        name=name,
        kind=kind,
        uri=uri,
        range=range_,
        selection_range=selection_range,
        detail=detail if detail else None,
    )


# ---------------------------------------------------------------------------
# Incoming calls: who instantiates this class
# ---------------------------------------------------------------------------


def _find_instantiations(class_name: str, source: str, uri: str) -> list[lsp_types.Range]:
    """Return ranges of all Call nodes that look like ClassName(...)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    ranges: list[lsp_types.Range] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = ""
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name == class_name:
                ranges.append(_range_for_node(node))
    return ranges


# ---------------------------------------------------------------------------
# Outgoing calls from forward()
# ---------------------------------------------------------------------------


def _calls_in_forward(
    forward_node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[tuple[str, ast.AST]]:
    """Return (callee_name, call_node) tuples from within a forward() body."""
    results: list[tuple[str, ast.AST]] = []
    for node in ast.walk(forward_node):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                # dspy.Predict, dspy.ChainOfThought, obj.forward, etc.
                name = f"{ast.unparse(func.value)}.{func.attr}"
                results.append((name, node))
            elif isinstance(func, ast.Name):
                results.append((func.id, node))
    # Also detect | operator (pipeline)
    for node in ast.walk(forward_node):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            results.append(("__or__ (pipeline)", node))
    return results


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_call_hierarchy(server: LanguageServer) -> None:
    """Register call hierarchy handlers on *server*."""

    @server.feature(lsp_types.TEXT_DOCUMENT_PREPARE_CALL_HIERARCHY)
    def on_prepare_call_hierarchy(
        params: lsp_types.CallHierarchyPrepareParams,
    ) -> list[lsp_types.CallHierarchyItem] | None:
        try:
            from .._state import module_index  # noqa: PLC0415

            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            position = params.position
            word = _word_at(source, position)
            if not word:
                return None

            # Check if it's a known dspy.Module class
            info = module_index.get_by_name(word)
            if info:
                class_node = _find_class_node(source, word)
                if class_node:
                    item = _make_item(
                        name=word,
                        kind=lsp_types.SymbolKind.Class,
                        uri=uri,
                        range_=_range_for_node(class_node),
                        selection_range=_name_range(class_node),
                        detail="dspy.Module",
                    )
                    return [item]

            # Check if it's a forward() method
            try:
                tree = ast.parse(source)
            except SyntaxError:
                return None
            for node in ast.walk(tree):
                if (
                    isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name == word
                ):
                    item = _make_item(
                        name=word,
                        kind=lsp_types.SymbolKind.Method,
                        uri=uri,
                        range_=_range_for_node(node),
                        selection_range=_name_range(node),
                    )
                    return [item]

            return None
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"prepare_call_hierarchy handler error: {exc}")
            return None

    @server.feature(lsp_types.CALL_HIERARCHY_INCOMING_CALLS)
    def on_incoming_calls(
        params: lsp_types.CallHierarchyIncomingCallsParams,
    ) -> list[lsp_types.CallHierarchyIncomingCall] | None:
        try:
            from .._state import module_index  # noqa: PLC0415

            item = params.item
            class_name = item.name
            incoming: list[lsp_types.CallHierarchyIncomingCall] = []

            # Search all indexed module files for instantiations
            seen: set[str] = set()
            for mod_info in module_index.all_modules():
                fp = mod_info.file_path
                if fp in seen:
                    continue
                seen.add(fp)
                try:
                    source = Path(fp).read_text(encoding="utf-8", errors="replace")
                    file_uri = Path(fp).as_uri()
                    ranges = _find_instantiations(class_name, source, file_uri)
                    if ranges:
                        caller_item = _make_item(
                            name=mod_info.name,
                            kind=lsp_types.SymbolKind.Module,
                            uri=file_uri,
                            range_=_zero_range(),
                            selection_range=_zero_range(),
                            detail=fp,
                        )
                        incoming.append(
                            lsp_types.CallHierarchyIncomingCall(
                                from_=caller_item,
                                from_ranges=ranges,
                            )
                        )
                except Exception:  # noqa: BLE001
                    pass

            return incoming
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"incoming_calls handler error: {exc}")
            return None

    @server.feature(lsp_types.CALL_HIERARCHY_OUTGOING_CALLS)
    def on_outgoing_calls(
        params: lsp_types.CallHierarchyOutgoingCallsParams,
    ) -> list[lsp_types.CallHierarchyOutgoingCall] | None:
        try:
            item = params.item
            uri = item.uri
            doc = server.workspace.get_text_document(uri)
            source = doc.source

            class_name = item.name
            class_node = _find_class_node(source, class_name)
            if not class_node:
                return []

            forward_node = _find_forward_node(class_node)
            if not forward_node:
                return []

            calls = _calls_in_forward(forward_node)
            outgoing: list[lsp_types.CallHierarchyOutgoingCall] = []
            for callee_name, call_node in calls:
                call_range = _range_for_node(call_node)
                callee_item = _make_item(
                    name=callee_name,
                    kind=lsp_types.SymbolKind.Function,
                    uri=uri,
                    range_=call_range,
                    selection_range=call_range,
                )
                outgoing.append(
                    lsp_types.CallHierarchyOutgoingCall(
                        to=callee_item,
                        from_ranges=[call_range],
                    )
                )

            return outgoing
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"outgoing_calls handler error: {exc}")
            return None
