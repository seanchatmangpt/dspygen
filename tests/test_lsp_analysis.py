"""Unit tests for LSP analysis utilities.

These are pure unit tests that do not require a running LSP server.
"""
from __future__ import annotations

import os

import pytest

pygls = pytest.importorskip("pygls")
lsprotocol = pytest.importorskip("lsprotocol")

from dspygen.lsp.analysis.module_index import ModuleIndex, ModuleInfo
from dspygen.lsp.analysis.signature_parser import (
    extract_field_names,
    parse_signature,
    validate_signature,
)

pytestmark = pytest.mark.lsp

# ---------------------------------------------------------------------------
# signature_parser.py tests
# ---------------------------------------------------------------------------


@pytest.mark.lsp
def test_parse_simple_signature():
    """``"text -> summary"`` parses to inputs=["text"], outputs=["summary"]."""
    parsed = parse_signature("text -> summary")
    assert parsed["inputs"] == ["text"]
    assert parsed["outputs"] == ["summary"]


@pytest.mark.lsp
def test_parse_multi_input_signature():
    """``"question, context -> answer"`` yields two inputs."""
    parsed = parse_signature("question, context -> answer")
    assert parsed["inputs"] == ["question", "context"]
    assert parsed["outputs"] == ["answer"]


@pytest.mark.lsp
def test_parse_multi_output_signature():
    """``"text -> title, body"`` yields two outputs."""
    parsed = parse_signature("text -> title, body")
    assert parsed["inputs"] == ["text"]
    assert parsed["outputs"] == ["title", "body"]


@pytest.mark.lsp
def test_validate_signature_valid():
    """A well-formed signature returns no errors."""
    errors = validate_signature("text -> summary")
    assert errors == []


@pytest.mark.lsp
def test_validate_signature_empty_output():
    """``"input -> "`` (empty output side) produces an error about empty output."""
    errors = validate_signature("input -> ")
    assert len(errors) > 0
    error_text = " ".join(errors).lower()
    assert "output" in error_text or "no output" in error_text


@pytest.mark.lsp
def test_validate_signature_no_arrow():
    """``"input output"`` (missing ``->``) produces an error about the missing arrow."""
    errors = validate_signature("input output")
    assert len(errors) > 0
    error_text = " ".join(errors).lower()
    assert "->" in error_text or "arrow" in error_text or "missing" in error_text or "separator" in error_text


@pytest.mark.lsp
def test_validate_signature_duplicate_fields():
    """``"text -> text"`` (same field on both sides) produces an error about conflict."""
    errors = validate_signature("text -> text")
    assert len(errors) > 0
    error_text = " ".join(errors).lower()
    assert "text" in error_text


@pytest.mark.lsp
def test_validate_signature_non_snake_case():
    """``"MyField -> output"`` produces an error/warning about naming conventions."""
    errors = validate_signature("MyField -> output")
    assert len(errors) > 0, f"Expected naming error/warning, got: {errors}"
    error_text = " ".join(errors).lower()
    assert "myfield" in error_text or "snake" in error_text or "snake_case" in error_text.lower()


@pytest.mark.lsp
def test_extract_field_names():
    """``extract_field_names`` returns all fields from both sides of the signature."""
    fields = extract_field_names("question, context -> answer, rationale")
    assert "question" in fields
    assert "context" in fields
    assert "answer" in fields
    assert "rationale" in fields
    assert len(fields) == 4


@pytest.mark.lsp
def test_parse_signature_with_whitespace():
    """Extra spaces around field names are stripped gracefully."""
    parsed = parse_signature("  text  ->  summary  ")
    assert parsed["inputs"] == ["text"]
    assert parsed["outputs"] == ["summary"]


# ---------------------------------------------------------------------------
# module_index.py tests
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def module_index():
    """Shared ModuleIndex instance for module_index tests."""
    idx = ModuleIndex()
    idx.build()
    return idx


@pytest.mark.lsp
def test_module_index_builds(module_index):
    """ModuleIndex() builds without error and has at least 50 modules."""
    assert len(module_index.all_modules()) >= 50


@pytest.mark.lsp
def test_module_index_search_by_name(module_index):
    """search("sql") returns results containing the NaturalLanguageToSQLModule."""
    results = module_index.search("sql")
    names = [r.name for r in results]
    assert any("sql" in n.lower() for n in names), (
        f"Expected a sql-related module, got: {names}"
    )
    assert "NaturalLanguageToSQLModule" in names, (
        f"Expected 'NaturalLanguageToSQLModule' in results, got: {names}"
    )


@pytest.mark.lsp
def test_module_index_get_by_name_found(module_index):
    """get_by_name("GenDspyModule") returns a ModuleInfo."""
    info = module_index.get_by_name("GenDspyModule")
    assert info is not None
    assert isinstance(info, ModuleInfo)
    assert info.name == "GenDspyModule"


@pytest.mark.lsp
def test_module_index_get_by_name_missing(module_index):
    """get_by_name("NonExistentModuleXyzzy") returns None."""
    result = module_index.get_by_name("NonExistentModuleXyzzy")
    assert result is None


@pytest.mark.lsp
def test_module_info_has_fields(module_index):
    """ModuleInfo objects have name, file_path, docstring, and signature_string fields."""
    info = module_index.get_by_name("GenDspyModule")
    assert info is not None
    assert hasattr(info, "name")
    assert hasattr(info, "file_path")
    assert hasattr(info, "docstring")
    assert hasattr(info, "signature_string")
    assert info.name == "GenDspyModule"
    assert info.file_path  # non-empty string


@pytest.mark.lsp
def test_module_index_all_signatures(module_index):
    """get_all_signatures() returns a dict mapping module names to signature strings."""
    sigs = module_index.get_all_signatures()
    assert isinstance(sigs, dict)
    assert len(sigs) > 0
    for name, sig in sigs.items():
        assert isinstance(name, str)
        assert isinstance(sig, str)
        assert "->" in sig, f"Signature for {name!r} does not contain '->': {sig!r}"


@pytest.mark.lsp
def test_module_index_search_fuzzy(module_index):
    """search("chatbot") returns chatbot-related modules."""
    results = module_index.search("chatbot")
    names = [r.name for r in results]
    assert len(results) > 0, "Expected at least one chatbot-related module"
    assert any("chat" in n.lower() or "bot" in n.lower() for n in names), (
        f"Unexpected results for chatbot search: {names}"
    )


@pytest.mark.lsp
def test_module_index_file_paths_exist(module_index):
    """All file_paths in the index actually exist on disk."""
    for info in module_index.all_modules():
        assert os.path.isfile(info.file_path), (
            f"file_path for {info.name!r} does not exist: {info.file_path!r}"
        )
