"""
Completion provider for the dspygen LSP server.

Triggers:
1. After ``dspy.Predict(`` or ``dspy.ChainOfThought(`` — offer known signature strings
2. After ``from dspygen.modules import`` — list all module names
3. After ``DGModule`` subclass method calls — complete forward(, pipe(, __or__(
4. After ``init_dspy(`` — offer model name completions
5. After field access on a module — complete .output, .forward_args
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MODEL_NAMES: list[dict[str, str]] = [
    {"label": "gpt-4o", "detail": "OpenAI GPT-4o (flagship multimodal)"},
    {"label": "gpt-4o-mini", "detail": "OpenAI GPT-4o Mini (fast, cost-efficient)"},
    {"label": "gpt-4-turbo", "detail": "OpenAI GPT-4 Turbo"},
    {"label": "gpt-3.5-turbo", "detail": "OpenAI GPT-3.5 Turbo (legacy)"},
    {"label": "ollama/llama3", "detail": "Meta Llama 3 via Ollama (local)"},
    {"label": "ollama/llama3:8b", "detail": "Meta Llama 3 8B via Ollama (local)"},
    {"label": "ollama/mistral", "detail": "Mistral 7B via Ollama (local)"},
    {"label": "ollama/codellama", "detail": "Code Llama via Ollama (local)"},
    {"label": "ollama/phi3", "detail": "Microsoft Phi-3 via Ollama (local)"},
    {"label": "anthropic/claude-3-5-sonnet-20241022", "detail": "Anthropic Claude 3.5 Sonnet"},
    {"label": "anthropic/claude-3-haiku-20240307", "detail": "Anthropic Claude 3 Haiku"},
    {"label": "groq/llama3-70b-8192", "detail": "Meta Llama 3 70B via Groq"},
    {"label": "groq/mixtral-8x7b-32768", "detail": "Mixtral 8x7B via Groq"},
]

_MODULE_METHODS: list[dict[str, str]] = [
    {
        "label": "forward",
        "detail": "forward(*args, **kwargs)",
        "doc": "The main inference method for a DSPy module. Override this in your subclass.",
    },
    {
        "label": "pipe",
        "detail": "pipe(input_data)",
        "doc": "Pipe input through the module, returning output for chaining.",
    },
    {
        "label": "__or__",
        "detail": "__or__(other)",
        "doc": "Pipe operator: ``module1 | module2`` chains two modules together.",
    },
]

# Patterns that trigger each completion type
_PREDICT_OPEN = re.compile(r"dspy\.(Predict|ChainOfThought)\(\s*[\"']?$")
_FROM_IMPORT = re.compile(r"from\s+dspygen\.modules\s+import\s+(\w*)$")
_INIT_DSPY = re.compile(r"init_dspy\([^)]*model\s*=\s*[\"']?$")
_FIELD_ACCESS = re.compile(r"\b(\w+)\.\s*$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_line_up_to_cursor(document_text: str, position: lsp_types.Position) -> str:
    """Return the text on *position.line* up to (not including) *position.character*."""
    lines = document_text.splitlines()
    if position.line >= len(lines):
        return ""
    return lines[position.line][: position.character]


def _make_completion_item(
    label: str,
    kind: lsp_types.CompletionItemKind = lsp_types.CompletionItemKind.Text,
    detail: str = "",
    documentation: str = "",
    insert_text: str | None = None,
) -> lsp_types.CompletionItem:
    item = lsp_types.CompletionItem(label=label)
    item.kind = kind
    if detail:
        item.detail = detail
    if documentation:
        item.documentation = lsp_types.MarkupContent(
            kind=lsp_types.MarkupKind.Markdown,
            value=documentation,
        )
    if insert_text is not None:
        item.insert_text = insert_text
    return item


# ---------------------------------------------------------------------------
# Completion logic
# ---------------------------------------------------------------------------


def _completions_for_predict(line: str, module_index) -> list[lsp_types.CompletionItem]:
    """Offer known signature strings when cursor is inside dspy.Predict( or dspy.ChainOfThought(."""
    items: list[lsp_types.CompletionItem] = []
    sigs = module_index.get_all_signatures()
    for mod_name, sig_str in sorted(sigs.items()):
        doc = f"Signature from **{mod_name}**\n\n`{sig_str}`"
        items.append(
            _make_completion_item(
                label=sig_str,
                kind=lsp_types.CompletionItemKind.Value,
                detail=f"from {mod_name}",
                documentation=doc,
            )
        )
    # Also suggest common generic signatures
    for generic in [
        "question -> answer",
        "prompt -> response",
        "context, question -> answer",
        "input -> output",
        "text -> summary",
    ]:
        items.append(
            _make_completion_item(
                label=generic,
                kind=lsp_types.CompletionItemKind.Snippet,
                detail="common DSPy signature",
            )
        )
    return items


def _completions_for_import(prefix: str, module_index) -> list[lsp_types.CompletionItem]:
    """Offer module class names after ``from dspygen.modules import``."""
    items: list[lsp_types.CompletionItem] = []
    for info in module_index.all_modules():
        if not info.name.lower().startswith(prefix.lower()):
            continue
        doc_lines = [f"**{info.name}**"]
        if info.docstring:
            doc_lines.append(f"\n{info.docstring}")
        if info.signature_string:
            doc_lines.append(f"\nSignature: `{info.signature_string}`")
        items.append(
            _make_completion_item(
                label=info.name,
                kind=lsp_types.CompletionItemKind.Class,
                detail=info.file_path.split("/")[-1],
                documentation="\n".join(doc_lines),
            )
        )
    return items


def _completions_for_init_dspy() -> list[lsp_types.CompletionItem]:
    """Offer model name strings when cursor is inside init_dspy(model=...)."""
    items: list[lsp_types.CompletionItem] = []
    for entry in _MODEL_NAMES:
        items.append(
            _make_completion_item(
                label=entry["label"],
                kind=lsp_types.CompletionItemKind.EnumMember,
                detail=entry["detail"],
                documentation=f"**Model:** `{entry['label']}`\n\n{entry['detail']}",
            )
        )
    return items


def _completions_for_module_methods() -> list[lsp_types.CompletionItem]:
    """Offer common dspy.Module method names after a dot."""
    items: list[lsp_types.CompletionItem] = []
    for entry in _MODULE_METHODS:
        items.append(
            _make_completion_item(
                label=entry["label"],
                kind=lsp_types.CompletionItemKind.Method,
                detail=entry.get("detail", ""),
                documentation=entry.get("doc", ""),
            )
        )
    # Also suggest common output attribute names
    for attr in ("output", "forward_args", "predict", "named_predictors"):
        items.append(
            _make_completion_item(
                label=attr,
                kind=lsp_types.CompletionItemKind.Field,
                detail="dspy.Module attribute",
            )
        )
    return items


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_completion(server: "LanguageServer") -> None:
    """Register the textDocument/completion handler on *server*."""

    @server.feature(
        lsp_types.TEXT_DOCUMENT_COMPLETION,
        lsp_types.CompletionOptions(trigger_characters=["(", ".", " ", "'"]),
    )
    def on_completion(
        params: lsp_types.CompletionParams,
    ) -> lsp_types.CompletionList:
        try:
            from .._state import module_index  # noqa: PLC0415

            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            line = _get_line_up_to_cursor(document.source, params.position)

            items: list[lsp_types.CompletionItem] = []

            # 1. dspy.Predict( / dspy.ChainOfThought(
            if _PREDICT_OPEN.search(line):
                items.extend(_completions_for_predict(line, module_index))
                return lsp_types.CompletionList(is_incomplete=False, items=items)

            # 2. from dspygen.modules import <prefix>
            m = _FROM_IMPORT.search(line)
            if m:
                prefix = m.group(1)
                items.extend(_completions_for_import(prefix, module_index))
                return lsp_types.CompletionList(is_incomplete=False, items=items)

            # 3. init_dspy(model=
            if _INIT_DSPY.search(line):
                items.extend(_completions_for_init_dspy())
                return lsp_types.CompletionList(is_incomplete=False, items=items)

            # 4. field / method access after a dot
            if _FIELD_ACCESS.search(line):
                items.extend(_completions_for_module_methods())
                return lsp_types.CompletionList(is_incomplete=False, items=items)

            return lsp_types.CompletionList(is_incomplete=False, items=[])
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"completion handler error: {exc}")
            return lsp_types.CompletionList(is_incomplete=False, items=[])
