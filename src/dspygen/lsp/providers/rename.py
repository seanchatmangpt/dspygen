"""
Rename provider for the dspygen LSP server.

Handles textDocument/rename and textDocument/prepareRename.

Supports renaming:
- DSPy signature field names — renames within the signature string AND all
  .field_name attribute accesses in the current file.
- dspygen module class names — renames the class definition, all usages in
  the current file, and import statements in the current file.

Returns WorkspaceEdit with all TextEdits needed.
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
_SIG_LITERAL_RE = re.compile(r"""(["'])([\w\s,]+->\s*[\w\s,]+)\1""")


def _word_at_position(source: str, position: lsp_types.Position) -> str:
    lines = source.splitlines()
    if position.line >= len(lines):
        return ""
    line = lines[position.line]
    col = position.character
    for match in _IDENT_RE.finditer(line):
        if match.start() <= col <= match.end():
            return match.group(1)
    return ""


def _range_at(line_no: int, col_start: int, col_end: int) -> lsp_types.Range:
    return lsp_types.Range(
        start=lsp_types.Position(line=line_no, character=col_start),
        end=lsp_types.Position(line=line_no, character=col_end),
    )


def _is_field_name_in_sig(source: str, position: lsp_types.Position) -> tuple[str, str] | None:
    """
    If the cursor is on a field name inside a signature string literal,
    return (field_name, sig_string).  Otherwise return None.
    """
    lines = source.splitlines()
    if position.line >= len(lines):
        return None
    line = lines[position.line]
    for m in _SIG_LITERAL_RE.finditer(line):
        sig_str = m.group(2)
        sig_start = m.start(2)
        sig_end = m.end(2)
        if not (sig_start <= position.character <= sig_end):
            continue
        # Find which field name the cursor is on within sig_str
        rel_col = position.character - sig_start
        for fm in re.finditer(r"\b([a-z_]\w*)\b", sig_str):
            if fm.start() <= rel_col <= fm.end():
                return fm.group(1), sig_str
    return None


def _rename_in_sig_strings(
    source: str,
    old_name: str,
    new_name: str,
) -> list[lsp_types.TextEdit]:
    """Return TextEdits that rename *old_name* inside all signature string literals."""
    edits: list[lsp_types.TextEdit] = []
    lines = source.splitlines()
    for line_no, line_text in enumerate(lines):
        for m in _SIG_LITERAL_RE.finditer(line_text):
            sig_str = m.group(2)
            sig_col_start = m.start(2)
            # Find all occurrences of old_name as a whole word inside sig_str
            for fm in re.finditer(r"\b" + re.escape(old_name) + r"\b", sig_str):
                abs_start = sig_col_start + fm.start()
                abs_end = sig_col_start + fm.end()
                edits.append(
                    lsp_types.TextEdit(
                        range=_range_at(line_no, abs_start, abs_end),
                        new_text=new_name,
                    )
                )
    return edits


def _rename_field_accesses(
    source: str,
    old_name: str,
    new_name: str,
) -> list[lsp_types.TextEdit]:
    """Return TextEdits for .old_name attribute accesses in source."""
    edits: list[lsp_types.TextEdit] = []
    pattern = re.compile(r"\." + re.escape(old_name) + r"\b")
    lines = source.splitlines()
    for line_no, line_text in enumerate(lines):
        for m in pattern.finditer(line_text):
            # m.start() is the '.', we want to replace just the name part
            name_start = m.start() + 1
            name_end = name_start + len(old_name)
            edits.append(
                lsp_types.TextEdit(
                    range=_range_at(line_no, name_start, name_end),
                    new_text=new_name,
                )
            )
    return edits


def _rename_class_in_file(
    source: str,
    old_name: str,
    new_name: str,
) -> list[lsp_types.TextEdit]:
    """
    Return TextEdits to rename all occurrences of *old_name* as a class/identifier
    (definition + usages + imports) in *source*.
    """
    edits: list[lsp_types.TextEdit] = []
    pattern = re.compile(r"\b" + re.escape(old_name) + r"\b")
    lines = source.splitlines()
    for line_no, line_text in enumerate(lines):
        for m in pattern.finditer(line_text):
            edits.append(
                lsp_types.TextEdit(
                    range=_range_at(line_no, m.start(), m.end()),
                    new_text=new_name,
                )
            )
    return edits


def _is_dspy_module_class(source: str, name: str) -> bool:
    """Return True if *name* is a dspy.Module subclass defined in *source*."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id in ("Module",):
                    return True
                if isinstance(base, ast.Attribute) and base.attr in ("Module",):
                    return True
    return False


def _uri_to_path(uri: str) -> Path:
    if uri.startswith("file://"):
        return Path(uri[len("file://"):])
    return Path(uri)


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_rename(server: "LanguageServer") -> None:
    """Register textDocument/rename and textDocument/prepareRename handlers."""

    @server.feature(lsp_types.TEXT_DOCUMENT_PREPARE_RENAME)
    def on_prepare_rename(
        params: lsp_types.PrepareRenameParams,
    ) -> lsp_types.Range | None:
        """Return the range of the symbol that would be renamed, or None."""
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            position = params.position
            lines = source.splitlines()
            if position.line >= len(lines):
                return None
            line = lines[position.line]
            col = position.character
            # Check if cursor is on an identifier
            for m in _IDENT_RE.finditer(line):
                if m.start() <= col <= m.end():
                    return _range_at(position.line, m.start(), m.end())
            return None
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"prepare_rename handler error: {exc}")
            return None

    @server.feature(lsp_types.TEXT_DOCUMENT_RENAME)
    def on_rename(
        params: lsp_types.RenameParams,
    ) -> lsp_types.WorkspaceEdit | None:
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            position = params.position
            new_name = params.new_name

            edits: list[lsp_types.TextEdit] = []

            # 1. Check if cursor is on a field name inside a signature literal
            sig_result = _is_field_name_in_sig(source, position)
            if sig_result:
                old_field, _sig_str = sig_result
                # Rename inside all signature strings in this file
                edits.extend(_rename_in_sig_strings(source, old_field, new_name))
                # Rename all .old_field attribute accesses
                edits.extend(_rename_field_accesses(source, old_field, new_name))
            else:
                # 2. Rename a class / identifier
                word = _word_at_position(source, position)
                if not word:
                    return None
                edits.extend(_rename_class_in_file(source, word, new_name))

            if not edits:
                return None

            return lsp_types.WorkspaceEdit(
                changes={uri: edits},
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"rename handler error: {exc}")
            return None
