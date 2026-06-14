"""
References provider for the dspygen LSP server.

Handles textDocument/references.

Finds all references to:
- dspygen module class names — all usages (import, instantiation) in the
  current file, and all files in the ModuleIndex that reference the module.
- DSPy signature field names — all .field_name attribute accesses in the
  current file.
- Any identifier — all occurrences in the current file as a baseline.
"""

from __future__ import annotations

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


def _is_field_in_sig(source: str, position: lsp_types.Position) -> str | None:
    """
    If the cursor is on a field name inside a signature literal, return the
    field name; otherwise return None.
    """
    lines = source.splitlines()
    if position.line >= len(lines):
        return None
    line = lines[position.line]
    for m in _SIG_LITERAL_RE.finditer(line):
        sig_str = m.group(2)
        sig_start = m.start(2)
        if not (sig_start <= position.character <= m.end(2)):
            continue
        rel_col = position.character - sig_start
        for fm in re.finditer(r"\b([a-z_]\w*)\b", sig_str):
            if fm.start() <= rel_col <= fm.end():
                return fm.group(1)
    return None


def _find_all_occurrences(source: str, name: str, uri: str) -> list[lsp_types.Location]:
    """Find all whole-word occurrences of *name* in *source*."""
    locations: list[lsp_types.Location] = []
    pattern = re.compile(r"\b" + re.escape(name) + r"\b")
    for line_no, line_text in enumerate(source.splitlines()):
        for m in pattern.finditer(line_text):
            locations.append(
                lsp_types.Location(
                    uri=uri,
                    range=lsp_types.Range(
                        start=lsp_types.Position(line=line_no, character=m.start()),
                        end=lsp_types.Position(line=line_no, character=m.end()),
                    ),
                )
            )
    return locations


def _find_field_accesses(source: str, field_name: str, uri: str) -> list[lsp_types.Location]:
    """Find all .field_name accesses in source."""
    locations: list[lsp_types.Location] = []
    pattern = re.compile(r"\." + re.escape(field_name) + r"\b")
    for line_no, line_text in enumerate(source.splitlines()):
        for m in pattern.finditer(line_text):
            name_start = m.start() + 1  # skip the dot
            locations.append(
                lsp_types.Location(
                    uri=uri,
                    range=lsp_types.Range(
                        start=lsp_types.Position(line=line_no, character=name_start),
                        end=lsp_types.Position(
                            line=line_no, character=name_start + len(field_name)
                        ),
                    ),
                )
            )
    return locations


def _find_in_sig_literals(source: str, field_name: str, uri: str) -> list[lsp_types.Location]:
    """Find all uses of *field_name* inside signature string literals."""
    locations: list[lsp_types.Location] = []
    for line_no, line_text in enumerate(source.splitlines()):
        for m in _SIG_LITERAL_RE.finditer(line_text):
            sig_str = m.group(2)
            sig_start = m.start(2)
            for fm in re.finditer(r"\b" + re.escape(field_name) + r"\b", sig_str):
                abs_start = sig_start + fm.start()
                locations.append(
                    lsp_types.Location(
                        uri=uri,
                        range=lsp_types.Range(
                            start=lsp_types.Position(line=line_no, character=abs_start),
                            end=lsp_types.Position(
                                line=line_no, character=abs_start + len(field_name)
                            ),
                        ),
                    )
                )
    return locations


def _cross_file_references(class_name: str, module_index) -> list[lsp_types.Location]:
    """Search all indexed module files for references to *class_name*."""
    locations: list[lsp_types.Location] = []
    seen_files: set[str] = set()

    for module_info in module_index.all_modules():
        file_path = module_info.file_path
        if file_path in seen_files:
            continue
        seen_files.add(file_path)
        try:
            source = Path(file_path).read_text(encoding="utf-8", errors="replace")
            file_uri = Path(file_path).as_uri()
            locations.extend(_find_all_occurrences(source, class_name, file_uri))
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"references: could not read {file_path}: {exc}")

    return locations


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_references(server: "LanguageServer") -> None:
    """Register the textDocument/references handler on *server*."""

    @server.feature(lsp_types.TEXT_DOCUMENT_REFERENCES)
    def on_references(
        params: lsp_types.ReferenceParams,
    ) -> list[lsp_types.Location] | None:
        try:
            from .._state import module_index  # noqa: PLC0415

            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            position = params.position
            include_declaration = (params.context and params.context.include_declaration)

            locations: list[lsp_types.Location] = []

            # 1. Check if cursor is on a field name inside a signature literal
            field_name = _is_field_in_sig(source, position)
            if field_name:
                locations.extend(_find_in_sig_literals(source, field_name, uri))
                locations.extend(_find_field_accesses(source, field_name, uri))
                return locations

            # 2. Identifier (class name or other)
            word = _word_at_position(source, position)
            if not word:
                return []

            # Check if it's a known module class
            info = module_index.get_by_name(word)
            if info:
                # Current file
                locations.extend(_find_all_occurrences(source, word, uri))
                # Cross-file references via module index
                cross = _cross_file_references(word, module_index)
                # Deduplicate with current file results
                current_uri_locs = {(l.range.start.line, l.range.start.character) for l in locations}
                for loc in cross:
                    if loc.uri == uri:
                        key = (loc.range.start.line, loc.range.start.character)
                        if key in current_uri_locs:
                            continue
                    locations.append(loc)
            else:
                # Generic identifier — search current file only
                locations.extend(_find_all_occurrences(source, word, uri))

            return locations
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"references handler error: {exc}")
            return None
