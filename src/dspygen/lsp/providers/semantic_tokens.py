"""
Semantic tokens provider for the dspygen LSP server.

Handles textDocument/semanticTokens/full.

Token type legend (indices):
  0: class
  1: function
  2: parameter
  3: operator
  4: string
  5: variable

Highlights:
- DSPy signature strings → field names as "parameter", "->" as "operator"
- dspy.Predict / dspy.ChainOfThought → "function"
- dspy.Module base class → "class"
- init_dspy → "function"
- Model name strings in init_dspy(model=...) → "string"

The token list is delta-encoded as per the LSP spec:
  [delta_line, delta_start_char, length, token_type_idx, token_modifier_mask]
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Legend (must match server capabilities advertisement)
# ---------------------------------------------------------------------------

TOKEN_TYPES: list[str] = ["class", "function", "parameter", "operator", "string", "variable"]
TOKEN_MODIFIERS: list[str] = []

_TYPE_CLASS = 0
_TYPE_FUNCTION = 1
_TYPE_PARAMETER = 2
_TYPE_OPERATOR = 3
_TYPE_STRING = 4
_TYPE_VARIABLE = 5

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_DSPY_PREDICT_RE = re.compile(r"\bdspy\.(Predict|ChainOfThought)\b")
_DSPY_MODULE_RE = re.compile(r"\bdspy\.Module\b")
_INIT_DSPY_RE = re.compile(r"\binit_dspy\b")
_SIG_LITERAL_RE = re.compile(r"""(["'])([\w\s,]+->\s*[\w\s,]+)\1""")
_INIT_DSPY_MODEL_RE = re.compile(r"""init_dspy\([^)]*model\s*=\s*(['"])([\w./:-]+)\1""")
_ARROW_RE = re.compile(r"->")
_FIELD_NAME_RE = re.compile(r"\b([a-z_]\w*)\b")


# ---------------------------------------------------------------------------
# Token builder
# ---------------------------------------------------------------------------


class _TokenBuilder:
    """Accumulates raw (line, col, length, type, modifier) tuples."""

    def __init__(self) -> None:
        self._raw: list[tuple[int, int, int, int, int]] = []

    def add(self, line: int, col: int, length: int, token_type: int, modifier: int = 0) -> None:
        if length > 0:
            self._raw.append((line, col, length, token_type, modifier))

    def encode(self) -> list[int]:
        """Delta-encode the tokens and return the flat integer array."""
        # Sort by line then column
        sorted_tokens = sorted(self._raw, key=lambda t: (t[0], t[1]))
        result: list[int] = []
        prev_line = 0
        prev_col = 0
        for line, col, length, t_type, modifier in sorted_tokens:
            delta_line = line - prev_line
            delta_col = col - prev_col if line == prev_line else col
            result.extend([delta_line, delta_col, length, t_type, modifier])
            prev_line = line
            prev_col = col
        return result


def _process_source(source: str) -> list[int]:
    builder = _TokenBuilder()
    lines = source.splitlines()

    for line_no, line_text in enumerate(lines):
        # dspy.Predict / dspy.ChainOfThought
        for m in _DSPY_PREDICT_RE.finditer(line_text):
            # Highlight only the method name part (Predict / ChainOfThought)
            attr_start = m.start() + len("dspy.")
            builder.add(line_no, attr_start, len(m.group(1)), _TYPE_FUNCTION)

        # dspy.Module
        for m in _DSPY_MODULE_RE.finditer(line_text):
            attr_start = m.start() + len("dspy.")
            builder.add(line_no, attr_start, len("Module"), _TYPE_CLASS)

        # init_dspy
        for m in _INIT_DSPY_RE.finditer(line_text):
            builder.add(line_no, m.start(), len("init_dspy"), _TYPE_FUNCTION)

        # init_dspy model string
        for m in _INIT_DSPY_MODEL_RE.finditer(line_text):
            model_name = m.group(2)
            # Find the quoted model value position
            model_start = line_text.find(model_name, m.start())
            if model_start != -1:
                builder.add(line_no, model_start, len(model_name), _TYPE_STRING)

        # DSPy signature string literals
        for m in _SIG_LITERAL_RE.finditer(line_text):
            sig_str = m.group(2)
            sig_col_start = m.start(2)

            # Arrow operator "->"
            for am in _ARROW_RE.finditer(sig_str):
                builder.add(line_no, sig_col_start + am.start(), 2, _TYPE_OPERATOR)

            # Field names (parameter type)
            for fm in _FIELD_NAME_RE.finditer(sig_str):
                field_name = fm.group(1)
                field_start = sig_col_start + fm.start()
                builder.add(line_no, field_start, len(field_name), _TYPE_PARAMETER)

    return builder.encode()


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def get_legend() -> lsp_types.SemanticTokensLegend:
    """Return the SemanticTokensLegend for server capabilities."""
    return lsp_types.SemanticTokensLegend(
        token_types=TOKEN_TYPES,
        token_modifiers=TOKEN_MODIFIERS,
    )


def register_semantic_tokens(server: LanguageServer) -> None:
    """Register the textDocument/semanticTokens/full handler on *server*."""

    @server.feature(
        lsp_types.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
        lsp_types.SemanticTokensOptions(
            legend=get_legend(),
            full=True,
        ),
    )
    def on_semantic_tokens_full(
        params: lsp_types.SemanticTokensParams,
    ) -> lsp_types.SemanticTokens | None:
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            data = _process_source(document.source)
            return lsp_types.SemanticTokens(data=data)
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"semantic_tokens handler error: {exc}")
            return None
