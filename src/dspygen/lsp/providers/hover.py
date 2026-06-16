"""
Hover provider for the dspygen LSP server.

Shows:
1. Module class name → docstring + signature + example usage
2. dspy.Predict / dspy.ChainOfThought / dspy.ReAct / dspy.ProgramOfThought call → parsed signature (inputs → outputs)
3. init_dspy → available models and descriptions
4. Signature string literal → parsed inputs / outputs
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

_INIT_DSPY_RE = re.compile(r"\binit_dspy\b")
_PREDICT_RE = re.compile(r"\bdspy\.(Predict|ChainOfThought|ReAct|ProgramOfThought)\b")
# Matches a string literal that contains "->"
_SIG_LITERAL_RE = re.compile(r"""['"]([\w\s,]+\s*->\s*[\w\s,]+)['"]""")
# Identifier under cursor
_IDENT_RE = re.compile(r"\b([A-Za-z_]\w*)\b")

_KNOWN_MODELS_MD = """\
| Model | Description |
|---|---|
| `gpt-4o` | OpenAI GPT-4o — flagship multimodal model |
| `gpt-4o-mini` | OpenAI GPT-4o Mini — fast and cost-efficient |
| `gpt-4-turbo` | OpenAI GPT-4 Turbo |
| `gpt-3.5-turbo` | OpenAI GPT-3.5 Turbo (legacy) |
| `ollama/llama3` | Meta Llama 3 via Ollama (local) |
| `ollama/mistral` | Mistral 7B via Ollama (local) |
| `ollama/codellama` | Code Llama via Ollama (local) |
| `anthropic/claude-3-5-sonnet-20241022` | Anthropic Claude 3.5 Sonnet |
| `groq/llama3-70b-8192` | Meta Llama 3 70B via Groq |
"""

# Static hover documentation for DSPy predictor classes that don't parse a signature.
_STATIC_HOVER: dict[str, str] = {
    "ChainOfThought": (
        "## `dspy.ChainOfThought`\n\n"
        "Chain of Thought — adds reasoning steps before producing the output. "
        "Inputs and outputs same as Predict.\n\n"
        "```python\n"
        "cot = dspy.ChainOfThought('context, question -> answer')\n"
        "result = cot(context='...', question='...')\n"
        "```"
    ),
    "ReAct": (
        "## `dspy.ReAct`\n\n"
        "ReAct — iterative reasoning+acting agent. Requires `tools` argument.\n\n"
        "```python\n"
        "react = dspy.ReAct('question -> answer', tools=[search, calc])\n"
        "result = react(question='...')\n"
        "```"
    ),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _word_at_position(source: str, position: lsp_types.Position) -> str:
    """Return the identifier-like word that the cursor sits on."""
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


def _make_hover(md: str) -> lsp_types.Hover:
    return lsp_types.Hover(
        contents=lsp_types.MarkupContent(
            kind=lsp_types.MarkupKind.Markdown,
            value=md,
        )
    )


def _format_signature(sig_str: str) -> str:
    """Format a signature string as Markdown."""
    from ..analysis.signature_parser import parse_signature  # noqa: PLC0415

    parsed = parse_signature(sig_str)
    inputs = ", ".join(f"`{f}`" for f in parsed["inputs"]) or "_none_"
    outputs = ", ".join(f"`{f}`" for f in parsed["outputs"]) or "_none_"
    return (
        f"**Inputs:** {inputs}\n\n"
        f"**Outputs:** {outputs}\n\n"
        f"```\n{sig_str}\n```"
    )


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_hover(server: LanguageServer) -> None:
    """Register the textDocument/hover handler on *server*."""

    @server.feature(lsp_types.TEXT_DOCUMENT_HOVER)
    def on_hover(params: lsp_types.HoverParams) -> lsp_types.Hover | None:
        try:
            from .._state import module_index  # noqa: PLC0415

            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            position = params.position
            line = _line_at(source, position.line)

            # ------------------------------------------------------------------
            # 1. init_dspy keyword
            # ------------------------------------------------------------------
            word = _word_at_position(source, position)
            if word == "init_dspy" or _INIT_DSPY_RE.search(line):
                md = (
                    "## `init_dspy()`\n\n"
                    "Initialise the DSPy language model backend.\n\n"
                    "```python\n"
                    "init_dspy(model='gpt-4o-mini', max_tokens=800)\n"
                    "```\n\n"
                    "### Available models\n\n"
                    + _KNOWN_MODELS_MD
                )
                return _make_hover(md)

            # ------------------------------------------------------------------
            # 2. dspy.Predict / dspy.ChainOfThought / dspy.ReAct / dspy.ProgramOfThought
            # ------------------------------------------------------------------
            if word in ("Predict", "ChainOfThought", "ReAct", "ProgramOfThought") and _PREDICT_RE.search(line):
                # ChainOfThought and ReAct have static descriptions; show them when no
                # signature literal is present on the line.
                m = _SIG_LITERAL_RE.search(line)
                sig_str = m.group(1).strip() if m else None
                if sig_str:
                    md = (
                        f"## `dspy.{word}`\n\n"
                        f"**Parsed signature:**\n\n"
                        + _format_signature(sig_str)
                    )
                elif word in _STATIC_HOVER:
                    md = _STATIC_HOVER[word]
                else:
                    md = (
                        f"## `dspy.{word}`\n\n"
                        f"A DSPy predictor. Pass a signature string or a `dspy.Signature` subclass.\n\n"
                        f"```python\n"
                        f"pred = dspy.{word}('input -> output')\n"
                        f"result = pred(input='...')\n"
                        f"```"
                    )
                return _make_hover(md)

            # ------------------------------------------------------------------
            # 3. Signature string literal under cursor
            # ------------------------------------------------------------------
            for m in _SIG_LITERAL_RE.finditer(line):
                start_col, end_col = m.start(), m.end()
                if start_col <= position.character <= end_col:
                    sig_str = m.group(1).strip()
                    md = "## DSPy Signature\n\n" + _format_signature(sig_str)
                    return _make_hover(md)

            # ------------------------------------------------------------------
            # 4. Module class name
            # ------------------------------------------------------------------
            if word:
                info = module_index.get_by_name(word)
                if info:
                    parts = [f"## `{info.name}`"]
                    if info.docstring:
                        parts.append(f"\n{info.docstring}")
                    if info.signature_string:
                        parts.append(
                            f"\n**Signature:** `{info.signature_string}`\n\n"
                            + _format_signature(info.signature_string)
                        )
                    # Example usage
                    example_args = ", ".join(
                        f"{f}=..." for f in info.input_fields
                    ) or "..."
                    parts.append(
                        f"\n**Example:**\n```python\nmod = {info.name}()\n"
                        f"result = mod.forward({example_args})\n```"
                    )
                    return _make_hover("\n\n".join(parts))

            return None
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"hover handler error: {exc}")
            return None
