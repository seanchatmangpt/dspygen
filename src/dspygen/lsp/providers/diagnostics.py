"""
Diagnostics provider for the dspygen LSP server.

Published on textDocument/didOpen and textDocument/didChange.

Checks:
1. Invalid signature strings (empty output, empty input, etc.)
2. dspy.Module subclass with no forward() method
3. Module instantiation without init_dspy() call in the file
4. Signature field name conflicts (input and output share same name)
5. Non-snake_case field names in signatures
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

_SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")
_SIG_STRING_RE = re.compile(r"""['"]([\w\s,]+->\s*[\w\s,]+)['"]""")


def _make_range(line: int, col_start: int = 0, col_end: int = 100) -> lsp_types.Range:
    return lsp_types.Range(
        start=lsp_types.Position(line=line, character=col_start),
        end=lsp_types.Position(line=line, character=col_end),
    )


def _range_for_node(node: ast.AST) -> lsp_types.Range:
    start_line = getattr(node, "lineno", 1) - 1
    start_col = getattr(node, "col_offset", 0)
    end_line = getattr(node, "end_lineno", start_line + 1) - 1
    end_col = getattr(node, "end_col_offset", start_col + 1)
    return lsp_types.Range(
        start=lsp_types.Position(line=start_line, character=start_col),
        end=lsp_types.Position(line=end_line, character=end_col),
    )


# ---------------------------------------------------------------------------
# AST-based checks
# ---------------------------------------------------------------------------


def _base_names(class_node: ast.ClassDef) -> list[str]:
    names: list[str] = []
    for base in class_node.bases:
        if isinstance(base, ast.Name):
            names.append(base.id)
        elif isinstance(base, ast.Attribute):
            names.append(base.attr)
    return names


def _has_forward_method(class_node: ast.ClassDef) -> bool:
    for item in class_node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "forward":
            return True
    return False


def _find_dspy_module_classes(tree: ast.Module) -> list[ast.ClassDef]:
    classes: list[ast.ClassDef] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if any(b in ("Module", "dspy.Module") for b in _base_names(node)):
                classes.append(node)
    return classes


def _has_init_dspy_call(tree: ast.Module) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "init_dspy":
                return True
            if isinstance(func, ast.Attribute) and func.attr == "init_dspy":
                return True
    return False


def _has_module_instantiation(tree: ast.Module) -> bool:
    """Check whether any known dspygen module class is instantiated in the file."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = ""
            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr
            if name.endswith("Module") and name[0].isupper():
                return True
    return False


def _validate_sig_string(sig: str) -> list[str]:
    """Return error messages for a DSPy signature string."""
    from ..analysis.signature_parser import validate_signature  # noqa: PLC0415

    return validate_signature(sig)


# ---------------------------------------------------------------------------
# Main diagnostic function
# ---------------------------------------------------------------------------


def _compute_diagnostics(source: str) -> list[lsp_types.Diagnostic]:
    diagnostics: list[lsp_types.Diagnostic] = []

    # ---- Parse the source ----
    try:
        tree = ast.parse(source)
    except SyntaxError:
        # Don't add our diagnostics on top of a syntax error — the editor handles those
        return diagnostics

    # ------------------------------------------------------------------
    # Check 1 + 4 + 5: Signature string literals in the source text
    # ------------------------------------------------------------------
    source_lines = source.splitlines()
    for line_no, line_text in enumerate(source_lines):
        for m in _SIG_STRING_RE.finditer(line_text):
            sig = m.group(1).strip()
            col_start = m.start(1)
            col_end = m.end(1)
            range_ = lsp_types.Range(
                start=lsp_types.Position(line=line_no, character=col_start),
                end=lsp_types.Position(line=line_no, character=col_end),
            )
            errors = _validate_sig_string(sig)
            for err in errors:
                # Decide severity
                if "no output" in err.lower() or "no input" in err.lower():
                    severity = lsp_types.DiagnosticSeverity.Error
                elif "conflict" in err.lower() or "both inputs and outputs" in err.lower():
                    severity = lsp_types.DiagnosticSeverity.Error
                elif "snake_case" in err.lower() or "not snake_case" in err.lower():
                    severity = lsp_types.DiagnosticSeverity.Warning
                elif "duplicate" in err.lower():
                    severity = lsp_types.DiagnosticSeverity.Warning
                else:
                    severity = lsp_types.DiagnosticSeverity.Error

                diagnostics.append(
                    lsp_types.Diagnostic(
                        range=range_,
                        message=err,
                        severity=severity,
                        source="dspygen-lsp",
                    )
                )

    # ------------------------------------------------------------------
    # AST-level checks: walk class definitions
    # ------------------------------------------------------------------
    dspy_classes = _find_dspy_module_classes(tree)

    for cls in dspy_classes:
        cls_range = _range_for_node(cls)

        # Check 2: missing forward() method
        if not _has_forward_method(cls):
            diagnostics.append(
                lsp_types.Diagnostic(
                    range=cls_range,
                    message=(
                        f"Class '{cls.name}' inherits from dspy.Module but has no "
                        "forward() method. Define forward() to implement the module logic."
                    ),
                    severity=lsp_types.DiagnosticSeverity.Warning,
                    source="dspygen-lsp",
                )
            )

    # Check 3: module instantiated but init_dspy() not called
    if dspy_classes and _has_module_instantiation(tree) and not _has_init_dspy_call(tree):
        # Point at the first class definition
        first_class_line = dspy_classes[0].lineno - 1
        diagnostics.append(
            lsp_types.Diagnostic(
                range=_make_range(first_class_line),
                message=(
                    "A dspy.Module subclass is instantiated but init_dspy() was not "
                    "called in this file. Make sure to call init_dspy() before running "
                    "any module to configure the language model backend."
                ),
                severity=lsp_types.DiagnosticSeverity.Information,
                source="dspygen-lsp",
            )
        )

    return diagnostics


# ---------------------------------------------------------------------------
# Provider registration
# ---------------------------------------------------------------------------


def register_diagnostics(server: "LanguageServer") -> None:
    """Register didOpen and didChange handlers that publish diagnostics."""

    def _publish(uri: str, source: str) -> None:
        try:
            diags = _compute_diagnostics(source)
            server.publish_diagnostics(uri, diags)
        except Exception as exc:  # noqa: BLE001
            logger.exception(f"diagnostics error for {uri}: {exc}")

    @server.feature(lsp_types.TEXT_DOCUMENT_DID_OPEN)
    def on_did_open(params: lsp_types.DidOpenTextDocumentParams) -> None:
        uri = params.text_document.uri
        source = params.text_document.text
        _publish(uri, source)

    @server.feature(lsp_types.TEXT_DOCUMENT_DID_CHANGE)
    def on_did_change(params: lsp_types.DidChangeTextDocumentParams) -> None:
        uri = params.text_document.uri
        # After incremental sync, the workspace has the latest text
        document = server.workspace.get_text_document(uri)
        _publish(uri, document.source)
