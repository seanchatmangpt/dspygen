commit 9f3f1a604c2de20b8f583613e0445ca336b523c2
Author: Claude <noreply@anthropic.com>
Date:   Sun Jun 14 19:15:44 2026 +0000

    test: add comprehensive LSP server, providers, and analysis test suite
    
    Implements the full DSPygen LSP server at src/dspygen/lsp/ with:
    - signature_parser.py: parse/validate DSPy "inputs -> outputs" strings
    - module_index.py: index all dspygen modules for search and lookup
    - completion.py: dspy.Predict(), module import, init_dspy(model=) completions
    - hover.py: hover docs for Predict, signature strings, module classes
    - diagnostics.py: lint for invalid signatures, missing forward(), field conflicts
    - definition.py: go-to-definition for dspy module classes
    - server.py: LanguageServer assembly with all features registered
    
    Adds 42 passing tests across three test files:
    - tests/test_lsp_analysis.py (18 tests): pure unit tests for analysis utilities
    - tests/test_lsp_providers.py (17 tests): provider function tests without server
    - tests/test_lsp_server.py (7 tests): server assembly and feature registration
    
    Also adds gen_dspy_module_class.py (GenDspyModule) and registers the lsp
    pytest mark in pyproject.toml.
    
    https://claude.ai/code/session_01R6Mp9kxxQ8dTxXZGZLFNvk

diff --git a/tests/test_lsp_analysis.py b/tests/test_lsp_analysis.py
new file mode 100644
index 0000000..0c11e79
--- /dev/null
+++ b/tests/test_lsp_analysis.py
@@ -0,0 +1,204 @@
+"""Unit tests for LSP analysis utilities.
+
+These are pure unit tests that do not require a running LSP server.
+"""
+from __future__ import annotations
+
+import os
+
+import pytest
+
+pygls = pytest.importorskip("pygls")
+lsprotocol = pytest.importorskip("lsprotocol")
+
+from dspygen.lsp.analysis.module_index import ModuleIndex, ModuleInfo
+from dspygen.lsp.analysis.signature_parser import (
+    extract_field_names,
+    parse_signature,
+    validate_signature,
+)
+
+pytestmark = pytest.mark.lsp
+
+# ---------------------------------------------------------------------------
+# signature_parser.py tests
+# ---------------------------------------------------------------------------
+
+
+@pytest.mark.lsp
+def test_parse_simple_signature():
+    """``"text -> summary"`` parses to inputs=["text"], outputs=["summary"]."""
+    parsed = parse_signature("text -> summary")
+    assert parsed.inputs == ["text"]
+    assert parsed.outputs == ["summary"]
+
+
+@pytest.mark.lsp
+def test_parse_multi_input_signature():
+    """``"question, context -> answer"`` yields two inputs."""
+    parsed = parse_signature("question, context -> answer")
+    assert parsed.inputs == ["question", "context"]
+    assert parsed.outputs == ["answer"]
+
+
+@pytest.mark.lsp
+def test_parse_multi_output_signature():
+    """``"text -> title, body"`` yields two outputs."""
+    parsed = parse_signature("text -> title, body")
+    assert parsed.inputs == ["text"]
+    assert parsed.outputs == ["title", "body"]
+
+
+@pytest.mark.lsp
+def test_validate_signature_valid():
+    """A well-formed signature returns no errors."""
+    result = validate_signature("text -> summary")
+    assert result.is_valid
+    assert result.errors == []
+
+
+@pytest.mark.lsp
+def test_validate_signature_empty_output():
+    """``"input -> "`` (empty output side) produces an error about empty output."""
+    result = validate_signature("input -> ")
+    assert not result.is_valid
+    error_text = " ".join(result.errors).lower()
+    assert "output" in error_text or "no output" in error_text or "empty" in error_text or "output" in error_text
+
+
+@pytest.mark.lsp
+def test_validate_signature_no_arrow():
+    """``"input output"`` (missing ``->``) produces an error about the missing arrow."""
+    result = validate_signature("input output")
+    assert not result.is_valid
+    error_text = " ".join(result.errors).lower()
+    assert "->" in error_text or "arrow" in error_text or "missing" in error_text or "separator" in error_text
+
+
+@pytest.mark.lsp
+def test_validate_signature_duplicate_fields():
+    """``"text -> text"`` (same field on both sides) produces an error about conflict."""
+    result = validate_signature("text -> text")
+    assert not result.is_valid
+    error_text = " ".join(result.errors).lower()
+    assert "text" in error_text
+
+
+@pytest.mark.lsp
+def test_validate_signature_non_snake_case():
+    """``"MyField -> output"`` produces a warning about naming conventions."""
+    result = validate_signature("MyField -> output")
+    # Should produce a warning (not necessarily an error) about naming
+    has_warning = any("myfield" in w.lower() or "snake" in w.lower() or "convention" in w.lower()
+                      for w in result.warnings)
+    assert has_warning, f"Expected naming warning, got warnings={result.warnings}"
+
+
+@pytest.mark.lsp
+def test_extract_field_names():
+    """``extract_field_names`` returns all fields from both sides of the signature."""
+    fields = extract_field_names("question, context -> answer, rationale")
+    assert "question" in fields
+    assert "context" in fields
+    assert "answer" in fields
+    assert "rationale" in fields
+    assert len(fields) == 4
+
+
+@pytest.mark.lsp
+def test_parse_signature_with_whitespace():
+    """Extra spaces around field names are stripped gracefully."""
+    parsed = parse_signature("  text  ->  summary  ")
+    assert parsed.inputs == ["text"]
+    assert parsed.outputs == ["summary"]
+
+
+# ---------------------------------------------------------------------------
+# module_index.py tests
+# ---------------------------------------------------------------------------
+
+
+@pytest.fixture(scope="module")
+def module_index():
+    """Shared ModuleIndex instance for module_index tests."""
+    return ModuleIndex()
+
+
+@pytest.mark.lsp
+def test_module_index_builds(module_index):
+    """ModuleIndex() loads without error and has at least 50 modules."""
+    assert len(module_index) >= 50
+
+
+@pytest.mark.lsp
+def test_module_index_search_by_name(module_index):
+    """search("sql") returns results containing the NaturalLanguageToSQLModule."""
+    results = module_index.search("sql")
+    names = [r.name for r in results]
+    assert any("sql" in n.lower() for n in names), (
+        f"Expected a sql-related module, got: {names}"
+    )
+    assert "NaturalLanguageToSQLModule" in names, (
+        f"Expected 'NaturalLanguageToSQLModule' in results, got: {names}"
+    )
+
+
+@pytest.mark.lsp
+def test_module_index_get_by_name_found(module_index):
+    """get_by_name("GenDspyModule") returns a ModuleInfo."""
+    info = module_index.get_by_name("GenDspyModule")
+    assert info is not None
+    assert isinstance(info, ModuleInfo)
+    assert info.name == "GenDspyModule"
+
+
+@pytest.mark.lsp
+def test_module_index_get_by_name_missing(module_index):
+    """get_by_name("NonExistentModule") returns None."""
+    result = module_index.get_by_name("NonExistentModuleXyzzy")
+    assert result is None
+
+
+@pytest.mark.lsp
+def test_module_info_has_fields(module_index):
+    """ModuleInfo objects have name, file_path, docstring, and signature_string fields."""
+    info = module_index.get_by_name("GenDspyModule")
+    assert info is not None
+    assert hasattr(info, "name")
+    assert hasattr(info, "file_path")
+    assert hasattr(info, "docstring")
+    assert hasattr(info, "signature_string")
+    assert info.name == "GenDspyModule"
+    assert info.file_path  # non-empty string
+
+
+@pytest.mark.lsp
+def test_module_index_all_signatures(module_index):
+    """get_all_signatures() returns a dict mapping module names to signature strings."""
+    sigs = module_index.get_all_signatures()
+    assert isinstance(sigs, dict)
+    assert len(sigs) > 0
+    for name, sig in sigs.items():
+        assert isinstance(name, str)
+        assert isinstance(sig, str)
+        assert "->" in sig, f"Signature for {name!r} does not contain '->': {sig!r}"
+
+
+@pytest.mark.lsp
+def test_module_index_search_fuzzy(module_index):
+    """search("chatbot") returns chatbot-related modules."""
+    results = module_index.search("chatbot")
+    names = [r.name for r in results]
+    assert len(results) > 0, "Expected at least one chatbot-related module"
+    assert any("chat" in n.lower() or "bot" in n.lower() for n in names), (
+        f"Unexpected results for chatbot search: {names}"
+    )
+
+
+@pytest.mark.lsp
+def test_module_index_file_paths_exist(module_index):
+    """All file_paths in the index actually exist on disk."""
+    for info in module_index.get_all():
+        assert os.path.isfile(info.file_path), (
+            f"file_path for {info.name!r} does not exist: {info.file_path!r}"
+        )
