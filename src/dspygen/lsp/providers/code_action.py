"""
Code action provider for the dspygen LSP server.

Handles textDocument/codeAction.

Provides quick fixes and refactors:
1. Invalid signature diagnostic → "Fix signature: add output field"
2. Missing forward() → "Add forward() method stub"
3. Non-snake_case field → "Convert to snake_case"
4. Module instantiation without init_dspy() → "Add init_dspy() call"
5. dspy.Predict → "Convert to ChainOfThought"
"""

from __future__ import annotations

import ast
import re
from typing import TYPE_CHECKING

from loguru import logger
from lsprotocol import types as lsp_types

if TYPE_CHECKING:
    from pygls.lsp.server import LanguageServer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SIG_LITERAL_RE = re.compile(r"""(["'])([\w\s,]+->\s*[\w\s,]+)\1""")
_PREDICT_RE = re.compile(r"\bdspy\.Predict\b")


def _range_at(line_no: int, col_start: int, col_end: int) -> lsp_types.Range:
    return lsp_types.Range(
        start=lsp_types.Position(line=line_no, character=col_start),
        end=lsp_types.Position(line=line_no, character=col_end),
    )


def _to_snake_case(name: str) -> str:
    """Convert a camelCase or PascalCase string to snake_case."""
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def _find_class_end_for_forward(source: str) -> int | None:
    """
    Find the best insertion line for a forward() stub.
    Returns the line number (0-based) after the last line of the first
    dspy.Module subclass body.  Returns None if not found.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            is_module = (
                (isinstance(base, ast.Name) and base.id == "Module")
                or (isinstance(base, ast.Attribute) and base.attr == "Module")
            )
            if is_module:
                # Insert at end of class body
                end_line = getattr(node, "end_lineno", None)
                if end_line is not None:
                    return end_line - 1  # 0-based, insert before closing
    return None


def _insert_init_dspy_edit(source: str) -> lsp_types.TextEdit | None:
    """Return a TextEdit inserting init_dspy() after the last import line."""
    lines = source.splitlines()
    last_import_line = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            last_import_line = i

    insert_line = last_import_line + 1
    insert_pos = lsp_types.Position(line=insert_line, character=0)
    return lsp_types.TextEdit(
        range=lsp_types.Range(start=insert_pos, end=insert_pos),
        new_text="\ninit_dspy()\n",
    )


# ---------------------------------------------------------------------------
# Action builders
# ---------------------------------------------------------------------------


def _action_fix_signature_output(
    uri: str,
    diag: lsp_types.Diagnostic,
    source_lines: list[str],
) -> lsp_types.CodeAction | None:
    """Offer to append an output field to a signature missing one."""
    if "no output" not in diag.message.lower():
        return None
    line_no = diag.range.start.line
    if line_no >= len(source_lines):
        return None
    line_text = source_lines[line_no]
    for m in _SIG_LITERAL_RE.finditer(line_text):
        sig_str = m.group(2)
        if "->" in sig_str and not sig_str.split("->", 1)[1].strip():
            # Append 'output' to the signature
            col_end = m.end(2)
            new_sig = sig_str.rstrip() + " output"
            edit = lsp_types.TextEdit(
                range=_range_at(line_no, m.start(2), m.end(2)),
                new_text=new_sig,
            )
            return lsp_types.CodeAction(
                title="Fix signature: add output field",
                kind=lsp_types.CodeActionKind.QuickFix,
                diagnostics=[diag],
                edit=lsp_types.WorkspaceEdit(changes={uri: [edit]}),
            )
    return None


def _action_add_forward_stub(
    uri: str,
    diag: lsp_types.Diagnostic,
    source: str,
) -> lsp_types.CodeAction | None:
    """Offer to add a forward() stub to a dspy.Module class missing one."""
    if "forward()" not in diag.message:
        return None
    insert_line = _find_class_end_for_forward(source)
    if insert_line is None:
        return None
    stub = "\n    def forward(self, *args, **kwargs):\n        raise NotImplementedError\n"
    insert_pos = lsp_types.Position(line=insert_line, character=0)
    edit = lsp_types.TextEdit(
        range=lsp_types.Range(start=insert_pos, end=insert_pos),
        new_text=stub,
    )
    return lsp_types.CodeAction(
        title="Add forward() method stub",
        kind=lsp_types.CodeActionKind.QuickFix,
        diagnostics=[diag],
        edit=lsp_types.WorkspaceEdit(changes={uri: [edit]}),
    )


def _action_snake_case_field(
    uri: str,
    diag: lsp_types.Diagnostic,
    source_lines: list[str],
) -> lsp_types.CodeAction | None:
    """Convert a non-snake_case field name to snake_case."""
    if "snake_case" not in diag.message.lower():
        return None
    # Extract the field name from the diagnostic message
    m = re.search(r"Field name '(\w+)'", diag.message)
    if not m:
        return None
    bad_name = m.group(1)
    snake = _to_snake_case(bad_name)
    if snake == bad_name:
        return None
    line_no = diag.range.start.line
    if line_no >= len(source_lines):
        return None
    line_text = source_lines[line_no]
    pattern = re.compile(r"\b" + re.escape(bad_name) + r"\b")
    edits: list[lsp_types.TextEdit] = []
    for fm in pattern.finditer(line_text):
        edits.append(
            lsp_types.TextEdit(
                range=_range_at(line_no, fm.start(), fm.end()),
                new_text=snake,
            )
        )
    if not edits:
        return None
    return lsp_types.CodeAction(
        title=f"Convert '{bad_name}' to snake_case: '{snake}'",
        kind=lsp_types.CodeActionKind.QuickFix,
        diagnostics=[diag],
        edit=lsp_types.WorkspaceEdit(changes={uri: edits}),
    )


def _action_add_init_dspy(
    uri: str,
    diag: lsp_types.Diagnostic,
    source: str,
) -> lsp_types.CodeAction | None:
    """Add init_dspy() call for modules that need it."""
    if "init_dspy" not in diag.message:
        return None
    edit = _insert_init_dspy_edit(source)
    if edit is None:
        return None
    return lsp_types.CodeAction(
        title="Add init_dspy() call",
        kind=lsp_types.CodeActionKind.QuickFix,
        diagnostics=[diag],
        edit=lsp_types.WorkspaceEdit(changes={uri: [edit]}),
    )


def _actions_for_range(
    uri: str,
    source: str,
    range_: lsp_types.Range,
) -> list[lsp_types.CodeAction]:
    """Context-dependent actions not tied to a specific diagnostic."""
    actions: list[lsp_types.CodeAction] = []
    source_lines = source.splitlines()
    start_line = range_.start.line
    end_line = range_.end.line

    for line_no in range(start_line, min(end_line + 1, len(source_lines))):
        line_text = source_lines[line_no]

        # dspy.Predict → Convert to ChainOfThought
        for m in _PREDICT_RE.finditer(line_text):
            edit = lsp_types.TextEdit(
                range=_range_at(line_no, m.start(), m.end()),
                new_text="dspy.ChainOfThought",
            )
            actions.append(
                lsp_types.CodeAction(
                    title="Convert dspy.Predict to dspy.ChainOfThought",
                    kind=lsp_types.CodeActionKind.RefactorRewrite,
                    edit=lsp_types.WorkspaceEdit(changes={uri: [edit]}),
                )
            )

    return actions


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_code_action(server: "LanguageServer") -> None:
    """Register the textDocument/codeAction handler on *server*."""

    @server.feature(
        lsp_types.TEXT_DOCUMENT_CODE_ACTION,
        lsp_types.CodeActionOptions(
            code_action_kinds=[
                lsp_types.CodeActionKind.QuickFix,
                lsp_types.CodeActionKind.RefactorRewrite,
            ]
        ),
    )
    def on_code_action(
        params: lsp_types.CodeActionParams,
    ) -> list[lsp_types.CodeAction] | None:
        try:
            uri = params.text_document.uri
            document = server.workspace.get_text_document(uri)
            source = document.source
            source_lines = source.splitlines()
            diagnostics = params.context.diagnostics or []

            actions: list[lsp_types.CodeAction] = []

            # Actions tied to diagnostics
            for diag in diagnostics:
                if diag.source != "dspygen-lsp":
                    continue
                a = _action_fix_signature_output(uri, diag, source_lines)
                if a:
                    actions.append(a)

                a = _action_add_forward_stub(uri, diag, source)
                if a:
                    actions.append(a)

                a = _action_snake_case_field(uri, diag, source_lines)
                if a:
                    actions.append(a)

                a = _action_add_init_dspy(uri, diag, source)
                if a:
                    actions.append(a)

            # Context-dependent refactors
            actions.extend(_actions_for_range(uri, source, params.range))

            return actions
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"code_action handler error: {exc}")
            return None
