"""
Go-to-definition provider for the dspygen LSP server.

Handles:
1. Module class name → jump to src/dspygen/modules/X.py
2. dspy.Predict / dspy.ChainOfThought → return None gracefully
3. Signature string literal → jump to where that signature is first defined in index
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
_SIG_LITERAL_RE = re.compile(r"""['"]([\w\s,]+->\s*[\w\s,]+)['"]""")
_PREDICT_RE = re.compile(r"\bdspy\.(Predict|ChainOfThought)\b")


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


def _line_at(source: str, line_no: int) -> str:
    lines = source.splitlines()
    if line_no >= len(lines):
        return ""
    return lines[line_no]


def _path_to_uri(path: str) -> str:
    """Convert an absolute filesystem path to a ``file://`` URI."""
    return Path(path).resolve().as_uri()


def _zero_range() -> lsp_types.Range:
    """A range pointing at the very start of a file."""
    return lsp_types.Range(
        start=lsp_types.Position(line=0, character=0),
        end=lsp_types.Position(line=0, character=0),
    )


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_definition(server: LanguageServer) -> None:
    """Register the textDocument/definition handler on *server*."""

    @server.feature(lsp_types.TEXT_DOCUMENT_DEFINITION)
    def on_definition(
        params: lsp_types.DefinitionParams,
    ) -> lsp_types.Location | list[lsp_types.Location] | None:
        try:
            from .._state import module_index  # noqa: PLC0415

            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            position = params.position
            line = _line_at(source, position.line)
            col = position.character

            # ------------------------------------------------------------------
            # 1. Check if cursor is on a signature string literal
            # ------------------------------------------------------------------
            for m in _SIG_LITERAL_RE.finditer(line):
                if m.start() <= col <= m.end():
                    sig = m.group(1).strip()
                    # Search index for a module with this exact signature
                    for info in module_index.all_modules():
                        if info.signature_string.strip() == sig:
                            return lsp_types.Location(
                                uri=_path_to_uri(info.file_path),
                                range=_zero_range(),
                            )
                    # Not found — return None gracefully
                    return None

            # ------------------------------------------------------------------
            # 2. Identifier under cursor
            # ------------------------------------------------------------------
            word = _word_at_position(source, position)
            if not word:
                return None

            # 2a. dspy.Predict / dspy.ChainOfThought — cannot jump to source
            if word in ("Predict", "ChainOfThought") and _PREDICT_RE.search(line):
                return None

            # 2b. Known dspygen module class
            info = module_index.get_by_name(word)
            if info:
                file_path = info.file_path
                if Path(file_path).is_file():
                    return lsp_types.Location(
                        uri=_path_to_uri(file_path),
                        range=_zero_range(),
                    )

            # 2c. Fallback: try to find a file named <word_lower>.py in modules dir
            here = Path(__file__).resolve().parent.parent  # lsp/
            modules_dir = here.parent / "modules"
            candidate = modules_dir / f"{word.lower()}.py"
            if candidate.is_file():
                return lsp_types.Location(
                    uri=candidate.resolve().as_uri(),
                    range=_zero_range(),
                )

            return None
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"definition handler error: {exc}")
            return None
