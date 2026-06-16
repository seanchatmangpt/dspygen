"""
Inlay hint provider for the dspygen LSP server.

Handles textDocument/inlayHint.

Shows inline hints for:
- After dspy.Predict("sig") / dspy.ChainOfThought("sig") → # inputs: [...] → outputs: [...]
- After module.forward( call → parameter name hints
- After init_dspy( → which model will be configured
- For .output attribute access → show the output field type hint
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_PREDICT_FULL_RE = re.compile(
    r"""\bdspy\.(Predict|ChainOfThought)\(\s*['"](.+?)['"]\s*\)"""
)
_INIT_DSPY_MODEL_RE = re.compile(
    r"""init_dspy\([^)]*model\s*=\s*['"]([^'"]+)['"]"""
)
_FORWARD_CALL_RE = re.compile(r"""\b(\w+)\.forward\(""")
_OUTPUT_ACCESS_RE = re.compile(r"""\b(\w+)\.output\b""")


def _parse_sig_fields(sig_str: str) -> tuple[list[str], list[str]]:
    """Minimal signature parser returning (inputs, outputs)."""
    if "->" not in sig_str:
        return [], []
    parts = sig_str.split("->", 1)
    inputs = [f.strip() for f in parts[0].split(",") if f.strip()]
    outputs = [f.strip() for f in parts[1].split(",") if f.strip()]
    return inputs, outputs


# ---------------------------------------------------------------------------
# Hint builders
# ---------------------------------------------------------------------------


def _hints_for_predict(source: str) -> list[lsp_types.InlayHint]:
    """Show signature field summary after dspy.Predict("...") calls."""
    hints: list[lsp_types.InlayHint] = []
    for line_no, line_text in enumerate(source.splitlines()):
        for m in _PREDICT_FULL_RE.finditer(line_text):
            sig_str = m.group(2)
            inputs, outputs = _parse_sig_fields(sig_str)
            if inputs or outputs:
                label = f"  # inputs: {inputs} → outputs: {outputs}"
                # Place hint at end of the matched call
                col = m.end()
                hints.append(
                    lsp_types.InlayHint(
                        position=lsp_types.Position(line=line_no, character=col),
                        label=label,
                        kind=lsp_types.InlayHintKind.Parameter,
                        padding_left=True,
                    )
                )
    return hints


def _hints_for_init_dspy(source: str) -> list[lsp_types.InlayHint]:
    """Show which model is configured inside init_dspy(model=...)."""
    hints: list[lsp_types.InlayHint] = []
    for line_no, line_text in enumerate(source.splitlines()):
        m = _INIT_DSPY_MODEL_RE.search(line_text)
        if m:
            model = m.group(1)
            label = f"  # configures: {model}"
            col = m.end()
            hints.append(
                lsp_types.InlayHint(
                    position=lsp_types.Position(line=line_no, character=col),
                    label=label,
                    kind=lsp_types.InlayHintKind.Type,
                    padding_left=True,
                )
            )
    return hints


def _hints_for_forward_call(source: str, module_index) -> list[lsp_types.InlayHint]:
    """Show parameter hints for module.forward( calls."""
    hints: list[lsp_types.InlayHint] = []
    for line_no, line_text in enumerate(source.splitlines()):
        for m in _FORWARD_CALL_RE.finditer(line_text):
            var_name = m.group(1)
            # Check if we know input fields for this module
            info = module_index.get_by_name(var_name)
            if info and info.input_fields:
                field_hints = " | ".join(f"{f}: str" for f in info.input_fields)
                label = f"• {field_hints}"
                col = m.end()
                hints.append(
                    lsp_types.InlayHint(
                        position=lsp_types.Position(line=line_no, character=col),
                        label=label,
                        kind=lsp_types.InlayHintKind.Parameter,
                        padding_left=True,
                    )
                )
    return hints


def _hints_for_output_access(source: str, module_index) -> list[lsp_types.InlayHint]:
    """Show output field type hint for .output attribute accesses."""
    hints: list[lsp_types.InlayHint] = []
    for line_no, line_text in enumerate(source.splitlines()):
        for m in _OUTPUT_ACCESS_RE.finditer(line_text):
            var_name = m.group(1)
            info = module_index.get_by_name(var_name)
            if info and info.output_fields:
                fields_str = ", ".join(info.output_fields)
                label = f": ({fields_str})"
                col = m.end()
                hints.append(
                    lsp_types.InlayHint(
                        position=lsp_types.Position(line=line_no, character=col),
                        label=label,
                        kind=lsp_types.InlayHintKind.Type,
                        padding_left=False,
                    )
                )
    return hints


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_inlay_hint(server: LanguageServer) -> None:
    """Register the textDocument/inlayHint handler on *server*."""

    @server.feature(
        lsp_types.TEXT_DOCUMENT_INLAY_HINT,
        lsp_types.InlayHintOptions(resolve_provider=False),
    )
    def on_inlay_hint(
        params: lsp_types.InlayHintParams,
    ) -> list[lsp_types.InlayHint] | None:
        try:
            from .._state import module_index  # noqa: PLC0415

            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source

            hints: list[lsp_types.InlayHint] = []
            hints.extend(_hints_for_predict(source))
            hints.extend(_hints_for_init_dspy(source))
            hints.extend(_hints_for_forward_call(source, module_index))
            hints.extend(_hints_for_output_access(source, module_index))

            return hints
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"inlay_hint handler error: {exc}")
            return None
