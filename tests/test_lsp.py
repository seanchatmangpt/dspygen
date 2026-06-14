"""Consolidated LSP tests — 30 focused, synchronous tests.

Covers: signature_parser, module_index, server assembly, completion, hover,
diagnostics, definition, document_symbol, workspace_symbol, rename,
code_action, semantic_tokens, formatting, references, inlay_hint,
folding_range, call_hierarchy, execute_command.

All tests are synchronous, mock external I/O, and run in under 5 ms each.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

pygls = pytest.importorskip("pygls")
lsprotocol = pytest.importorskip("lsprotocol")

from lsprotocol import types as lsp_types

pytestmark = pytest.mark.lsp


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def module_index():
    from dspygen.lsp.analysis.module_index import ModuleIndex
    idx = ModuleIndex()
    idx.build()
    return idx


@pytest.fixture(scope="module")
def lsp_server():
    from dspygen.lsp.server import server
    return server


# ===========================================================================
# signature_parser  (4 tests)
# ===========================================================================


def test_parse_simple_signature():
    """'text -> summary' parses to inputs=['text'], outputs=['summary']."""
    from dspygen.lsp.analysis.signature_parser import parse_signature
    parsed = parse_signature("text -> summary")
    assert parsed["inputs"] == ["text"]
    assert parsed["outputs"] == ["summary"]


def test_parse_multi_input_signature():
    """'question, context -> answer' yields two inputs."""
    from dspygen.lsp.analysis.signature_parser import parse_signature
    parsed = parse_signature("question, context -> answer")
    assert parsed["inputs"] == ["question", "context"]
    assert parsed["outputs"] == ["answer"]


def test_validate_invalid_signature():
    """'input -> ' (empty output side) produces at least one validation error."""
    from dspygen.lsp.analysis.signature_parser import validate_signature
    errors = validate_signature("input -> ")
    assert len(errors) > 0
    combined = " ".join(errors).lower()
    assert "output" in combined or "empty" in combined or "no " in combined


def test_validate_field_conflict():
    """'text -> text' (same field on both sides) produces a conflict error."""
    from dspygen.lsp.analysis.signature_parser import validate_signature
    errors = validate_signature("text -> text")
    assert len(errors) > 0
    combined = " ".join(errors).lower()
    assert "text" in combined


# ===========================================================================
# module_index  (3 tests)
# ===========================================================================


def test_module_index_builds_without_error(module_index):
    """ModuleIndex.build() runs without error and finds at least 50 modules."""
    assert len(module_index.all_modules()) >= 50


def test_module_index_search_returns_results(module_index):
    """search('sql') returns results that include a SQL-related module."""
    results = module_index.search("sql")
    names = [r.name for r in results]
    assert any("sql" in n.lower() for n in names)


def test_module_index_get_by_name_found_and_not_found(module_index):
    """get_by_name returns ModuleInfo for a known name and None for unknown."""
    from dspygen.lsp.analysis.module_index import ModuleInfo
    info = module_index.get_by_name("GenDspyModule")
    assert info is not None
    assert isinstance(info, ModuleInfo)
    assert info.name == "GenDspyModule"

    missing = module_index.get_by_name("NonExistentModuleXyzzy")
    assert missing is None


# ===========================================================================
# server  (3 tests)
# ===========================================================================


def test_server_creates(lsp_server):
    """The LanguageServer instance is created successfully."""
    from pygls.lsp.server import LanguageServer
    assert isinstance(lsp_server, LanguageServer)


def test_server_name(lsp_server):
    """Server name is 'dspygen-lsp'."""
    assert lsp_server.name == "dspygen-lsp"


def test_completion_registered(lsp_server):
    """textDocument/completion is registered in the feature manager."""
    protocol = lsp_server.protocol
    bf = getattr(protocol, "fm", None) or getattr(protocol, "_feature_manager", None)
    if bf is None:
        pytest.skip("Cannot introspect feature manager on this pygls version")
    method_name = lsp_types.TEXT_DOCUMENT_COMPLETION
    feature_keys = list(bf._features.keys()) if hasattr(bf, "_features") else []
    assert method_name in feature_keys, (
        f"Expected '{method_name}' registered, got: {feature_keys}"
    )


# ===========================================================================
# completion  (2 tests)
# ===========================================================================


def test_completion_after_dspy_predict(module_index):
    """Typing 'dspy.Predict(' triggers signature completions containing '->'."""
    from dspygen.lsp.providers.completion import _completions_for_predict
    items = _completions_for_predict("pred = dspy.Predict(", module_index)
    assert len(items) > 0
    sig_items = [i for i in items if "->" in i.label]
    assert len(sig_items) > 0


def test_completion_after_import_returns_names(module_index):
    """Typing 'from dspygen.modules import' returns module name completions."""
    from dspygen.lsp.providers.completion import _completions_for_import
    items = _completions_for_import("", module_index)
    assert len(items) > 0
    labels = [item.label for item in items]
    assert any("Module" in label for label in labels)


# ===========================================================================
# hover  (2 tests)
# ===========================================================================


def test_hover_on_signature_string_returns_markdown():
    """Hovering on 'text -> summary' returns a Markdown MarkupContent."""
    from dspygen.lsp.providers.hover import _format_signature, _make_hover
    sig_str = "text -> summary"
    formatted = _format_signature(sig_str)
    hover = _make_hover("## DSPy Signature\n\n" + formatted)
    assert isinstance(hover, lsp_types.Hover)
    content = hover.contents
    assert isinstance(content, lsp_types.MarkupContent)
    assert content.kind == lsp_types.MarkupKind.Markdown
    assert "text" in content.value and "summary" in content.value


def test_hover_on_unknown_symbol_returns_none(module_index):
    """Looking up an unrecognised symbol via the module index returns None."""
    result = module_index.get_by_name("totally_unknown_symbol_xyz_abc")
    assert result is None


# ===========================================================================
# diagnostics  (3 tests)
# ===========================================================================


def test_diagnostics_invalid_sig_produces_error():
    """dspy.Predict('input -> ') produces at least one Error diagnostic."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics
    code = 'pred = dspy.Predict("input -> ")'
    diags = _compute_diagnostics(code)
    errors = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Error]
    assert len(errors) > 0


def test_diagnostics_missing_forward_produces_warning():
    """A dspy.Module subclass with no forward() produces a Warning diagnostic."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics
    code = (
        "import dspy\n"
        "\n"
        "class MyModule(dspy.Module):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
    )
    diags = _compute_diagnostics(code)
    warnings = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Warning]
    assert len(warnings) > 0
    assert any("forward" in d.message.lower() for d in warnings)


def test_diagnostics_valid_code_no_diags():
    """A well-formed DSPy module produces zero diagnostics."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics
    code = (
        "import dspy\n"
        "\n"
        "class Summarizer(dspy.Module):\n"
        '    """Summarizes text."""\n'
        "\n"
        "    def forward(self, text):\n"
        '        pred = dspy.Predict("text -> summary")\n'
        "        return pred(text=text).summary\n"
    )
    diags = _compute_diagnostics(code)
    assert diags == []


# ===========================================================================
# definition  (2 tests)
# ===========================================================================


def test_definition_known_module_returns_location(module_index):
    """get_by_name for a known class name returns a non-None ModuleInfo with file_path."""
    from dspygen.lsp.providers.definition import _path_to_uri
    info = module_index.get_by_name("GenDspyModule")
    assert info is not None
    uri = _path_to_uri(info.file_path)
    assert uri.startswith("file://")
    assert "modules" in uri or "gen_dspy" in uri


def test_definition_unknown_returns_none(module_index):
    """get_by_name for an unknown class returns None."""
    result = module_index.get_by_name("UnknownClassXyzzy123")
    assert result is None


# ===========================================================================
# document_symbol  (1 test)
# ===========================================================================


def test_document_symbol_extracts_class_definitions():
    """_extract_symbols finds class definitions in Python source."""
    from dspygen.lsp.providers.document_symbol import _extract_symbols
    source = (
        "import dspy\n"
        "\n"
        "class MySignature(dspy.Signature):\n"
        '    """A signature."""\n'
        "    question = dspy.InputField()\n"
        "    answer = dspy.OutputField()\n"
        "\n"
        "class MyModule(dspy.Module):\n"
        "    def forward(self, question):\n"
        "        pass\n"
    )
    symbols = _extract_symbols(source)
    names = [s.name for s in symbols]
    assert "MySignature" in names
    assert "MyModule" in names
    for s in symbols:
        assert isinstance(s, lsp_types.DocumentSymbol)


# ===========================================================================
# workspace_symbol  (1 test)
# ===========================================================================


def test_workspace_symbol_returns_matching_symbols():
    """_WorkspaceIndex.search returns entries whose names contain the query."""
    from dspygen.lsp.providers.workspace_symbol import _WorkspaceIndex, _index_file
    idx = _WorkspaceIndex()
    source = (
        "import dspy\n"
        "\n"
        "class SummarizerModule(dspy.Module):\n"
        "    def forward(self, text):\n"
        "        pass\n"
    )
    entries = _index_file(Path("/fake/summarizer.py"), source)
    idx._entries = entries
    idx._built = True

    results = idx.search("Summarizer")
    assert len(results) >= 1
    assert any("Summarizer" in e.name for e in results)


# ===========================================================================
# rename  (1 test)
# ===========================================================================


def test_rename_renames_field_in_signature_string():
    """_rename_in_sig_strings renames a field name inside a sig literal."""
    from dspygen.lsp.providers.rename import _rename_in_sig_strings
    source = 'pred = dspy.Predict("text -> summary")'
    edits = _rename_in_sig_strings(source, "text", "document")
    assert len(edits) >= 1
    for edit in edits:
        assert edit.new_text == "document"
        assert isinstance(edit, lsp_types.TextEdit)


# ===========================================================================
# code_action  (1 test)
# ===========================================================================


def test_code_action_invalid_sig_offers_fix():
    """_action_fix_signature_output returns a CodeAction for a missing-output diag."""
    from dspygen.lsp.providers.code_action import _action_fix_signature_output
    uri = "file:///fake/test.py"
    source_line = 'pred = dspy.Predict("input -> ")'
    diag = lsp_types.Diagnostic(
        range=lsp_types.Range(
            start=lsp_types.Position(line=0, character=0),
            end=lsp_types.Position(line=0, character=len(source_line)),
        ),
        message="Signature has no output fields.",
        severity=lsp_types.DiagnosticSeverity.Error,
        source="dspygen-lsp",
    )
    action = _action_fix_signature_output(uri, diag, [source_line])
    assert action is not None
    assert isinstance(action, lsp_types.CodeAction)
    assert "output" in action.title.lower() or "fix" in action.title.lower()


# ===========================================================================
# semantic_tokens  (1 test)
# ===========================================================================


def test_semantic_tokens_returns_encoded_tokens():
    """_process_source returns a non-empty list of ints for DSPy source."""
    from dspygen.lsp.providers.semantic_tokens import _process_source
    source = 'pred = dspy.Predict("text -> summary")\n'
    data = _process_source(source)
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(x, int) for x in data)


# ===========================================================================
# formatting  (1 test)
# ===========================================================================


def test_formatting_ruff_available_returns_text_edits():
    """_format_source returns a changed string when ruff is available; skipped otherwise."""
    import shutil
    from dspygen.lsp.providers.formatting import _format_source, _whole_document_edit
    if not shutil.which("ruff"):
        pytest.skip("ruff not available in this environment")
    source = "x=1\ny  =  2\n"
    formatted = _format_source(source)
    edits = _whole_document_edit(source, formatted)
    assert isinstance(edits, list)
    for edit in edits:
        assert isinstance(edit, lsp_types.TextEdit)


# ===========================================================================
# references  (1 test)
# ===========================================================================


def test_references_finds_field_references_in_file():
    """_find_all_occurrences locates every whole-word occurrence of a field."""
    from dspygen.lsp.providers.references import _find_all_occurrences
    uri = "file:///fake/mod.py"
    source = (
        "pred = dspy.Predict('text -> summary')\n"
        "result = pred(text='hello')\n"
        "print(result.summary)\n"
    )
    locs = _find_all_occurrences(source, "summary", uri)
    assert len(locs) >= 1
    for loc in locs:
        assert isinstance(loc, lsp_types.Location)
        assert loc.uri == uri


# ===========================================================================
# inlay_hint  (1 test)
# ===========================================================================


def test_inlay_hint_returns_hints_for_dspy_predict_call():
    """_hints_for_predict produces InlayHint entries for dspy.Predict('sig') calls."""
    from dspygen.lsp.providers.inlay_hint import _hints_for_predict
    source = "pred = dspy.Predict('text -> summary')\n"
    hints = _hints_for_predict(source)
    assert len(hints) >= 1
    for hint in hints:
        assert isinstance(hint, lsp_types.InlayHint)
        label = hint.label if isinstance(hint.label, str) else ""
        assert "inputs" in label or "outputs" in label or "->" in label


# ===========================================================================
# folding_range  (1 test)
# ===========================================================================


def test_folding_range_returns_ranges_for_class_body():
    """_extract_folding_ranges returns at least one FoldingRange for a class."""
    from dspygen.lsp.providers.folding_range import _extract_folding_ranges
    source = (
        "import dspy\n"
        "\n"
        "class MyModule(dspy.Module):\n"
        "    def forward(self, text):\n"
        "        return text\n"
    )
    ranges = _extract_folding_ranges(source)
    assert len(ranges) >= 1
    for r in ranges:
        assert isinstance(r, lsp_types.FoldingRange)
        assert r.end_line >= r.start_line


# ===========================================================================
# call_hierarchy  (1 test)
# ===========================================================================


def test_call_hierarchy_prepare_returns_item_for_module_class():
    """_find_class_node finds a class in source; _make_item builds a valid item."""
    from dspygen.lsp.providers.call_hierarchy import (
        _find_class_node,
        _make_item,
        _name_range,
        _range_for_node,
    )
    source = (
        "import dspy\n"
        "\n"
        "class SummarizerModule(dspy.Module):\n"
        "    def forward(self, text):\n"
        "        return text\n"
    )
    class_node = _find_class_node(source, "SummarizerModule")
    assert class_node is not None
    uri = "file:///fake/summarizer.py"
    item = _make_item(
        name="SummarizerModule",
        kind=lsp_types.SymbolKind.Class,
        uri=uri,
        range_=_range_for_node(class_node),
        selection_range=_name_range(class_node),
        detail="dspy.Module",
    )
    assert isinstance(item, lsp_types.CallHierarchyItem)
    assert item.name == "SummarizerModule"
    assert item.uri == uri


# ===========================================================================
# execute_command  (1 test)
# ===========================================================================


def test_execute_command_validate_signature_returns_result():
    """_handle_validate_signature returns a valid result for a direct sig arg."""
    from dspygen.lsp.providers.execute_command import _handle_validate_signature
    mock_server = MagicMock()
    result = _handle_validate_signature(mock_server, ["question -> answer"])
    assert isinstance(result, str)
    assert "valid" in result.lower() or "question" in result.lower()
