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

diff --git a/tests/test_lsp_providers.py b/tests/test_lsp_providers.py
new file mode 100644
index 0000000..ac2f617
--- /dev/null
+++ b/tests/test_lsp_providers.py
@@ -0,0 +1,251 @@
+"""Tests for LSP providers.
+
+Each provider function is tested in isolation — no real LSP server is started.
+The handler functions are called directly with constructed inputs.
+"""
+from __future__ import annotations
+
+import pytest
+
+pygls = pytest.importorskip("pygls")
+lsprotocol = pytest.importorskip("lsprotocol")
+
+from lsprotocol import types as lsp_types
+
+from dspygen.lsp.providers.completion import get_completions
+from dspygen.lsp.providers.definition import get_definition
+from dspygen.lsp.providers.diagnostics import get_diagnostics
+from dspygen.lsp.providers.hover import get_hover
+
+pytestmark = pytest.mark.lsp
+
+# ---------------------------------------------------------------------------
+# completion.py tests
+# ---------------------------------------------------------------------------
+
+
+@pytest.mark.lsp
+def test_completion_after_dspy_predict():
+    """Typing ``dspy.Predict(`` triggers signature suggestions."""
+    code = 'pred = dspy.Predict('
+    result = get_completions(code, line=0, character=len(code))
+    assert isinstance(result, lsp_types.CompletionList)
+    assert len(result.items) > 0
+    # All items should include a signature string (contain "->")
+    for item in result.items:
+        assert "->" in item.label, f"Expected signature in label, got: {item.label!r}"
+
+
+@pytest.mark.lsp
+def test_completion_after_module_import():
+    """Typing ``from dspygen.modules import `` triggers module name completions."""
+    code = "from dspygen.modules import "
+    result = get_completions(code, line=0, character=len(code))
+    assert isinstance(result, lsp_types.CompletionList)
+    assert len(result.items) > 0
+    labels = [item.label for item in result.items]
+    assert any("Module" in label for label in labels), (
+        f"Expected module names in completions, got first 5: {labels[:5]}"
+    )
+
+
+@pytest.mark.lsp
+def test_completion_init_dspy_model():
+    """Typing ``init_dspy(model=`` triggers model name completions."""
+    code = "init_dspy(model="
+    result = get_completions(code, line=0, character=len(code))
+    assert isinstance(result, lsp_types.CompletionList)
+    assert len(result.items) > 0
+    # All items should be model name strings
+    for item in result.items:
+        assert item.label  # non-empty label
+
+
+@pytest.mark.lsp
+def test_completion_items_have_documentation():
+    """All completion items returned for dspy.Predict( have documentation."""
+    code = "dspy.Predict("
+    result = get_completions(code, line=0, character=len(code))
+    assert len(result.items) > 0
+    for item in result.items:
+        assert item.documentation is not None, (
+            f"Completion item {item.label!r} has no documentation"
+        )
+
+
+@pytest.mark.lsp
+def test_completion_returns_completion_list():
+    """get_completions always returns a CompletionList, even with no matches."""
+    result = get_completions("x = 1 + 2", line=0, character=9)
+    assert isinstance(result, lsp_types.CompletionList)
+    # No completions expected for arithmetic
+    assert isinstance(result.items, list)
+
+
+# ---------------------------------------------------------------------------
+# hover.py tests
+# ---------------------------------------------------------------------------
+
+
+@pytest.mark.lsp
+def test_hover_on_dspy_predict_call():
+    """Hovering over ``Predict`` returns markdown with input/output description."""
+    code = "pred = dspy.Predict('text -> summary')"
+    # Position within "Predict"
+    col = code.index("Predict") + 3  # mid-word
+    result = get_hover(code, line=0, character=col)
+    assert result is not None
+    assert isinstance(result, lsp_types.Hover)
+    content = result.contents
+    assert isinstance(content, lsp_types.MarkupContent)
+    assert content.kind == lsp_types.MarkupKind.Markdown
+    # Should mention inputs/outputs or describe the Predict module
+    assert "Predict" in content.value or "predict" in content.value.lower()
+
+
+@pytest.mark.lsp
+def test_hover_on_signature_string():
+    """Hovering on a signature string ``"text -> summary"`` returns parsed fields."""
+    code = 'pred = dspy.Predict("text -> summary")'
+    # Position inside the signature string
+    col = code.index("text -> summary") + 5
+    result = get_hover(code, line=0, character=col)
+    assert result is not None
+    content = result.contents
+    assert isinstance(content, lsp_types.MarkupContent)
+    # Should show inputs and outputs
+    assert "text" in content.value
+    assert "summary" in content.value
+
+
+@pytest.mark.lsp
+def test_hover_on_unknown_symbol():
+    """Hovering on an unrecognised token returns None gracefully."""
+    code = "x = totally_unknown_symbol_xyz"
+    col = code.index("totally_unknown_symbol_xyz") + 5
+    result = get_hover(code, line=0, character=col)
+    assert result is None
+
+
+@pytest.mark.lsp
+def test_hover_returns_markdown():
+    """Any hover result uses MarkupKind.Markdown."""
+    code = 'pred = dspy.Predict("question, context -> answer")'
+    col = code.index("question") + 2
+    result = get_hover(code, line=0, character=col)
+    assert result is not None
+    content = result.contents
+    assert isinstance(content, lsp_types.MarkupContent)
+    assert content.kind == lsp_types.MarkupKind.Markdown
+
+
+# ---------------------------------------------------------------------------
+# diagnostics.py tests
+# ---------------------------------------------------------------------------
+
+
+@pytest.mark.lsp
+def test_diagnostic_invalid_signature():
+    """``dspy.Predict("input -> ")`` produces an Error diagnostic for the empty output."""
+    code = 'pred = dspy.Predict("input -> ")'
+    diags = get_diagnostics(code)
+    assert len(diags) > 0, "Expected at least one diagnostic for invalid signature"
+    errors = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Error]
+    assert len(errors) > 0, f"Expected Error severity diagnostic, got: {diags}"
+
+
+@pytest.mark.lsp
+def test_diagnostic_missing_forward():
+    """A ``dspy.Module`` subclass without a ``forward`` method produces a Warning."""
+    code = """
+import dspy
+
+class MyModule(dspy.Module):
+    def __init__(self):
+        super().__init__()
+"""
+    diags = get_diagnostics(code)
+    warnings = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Warning]
+    assert len(warnings) > 0, (
+        f"Expected Warning about missing forward method, got diagnostics: {diags}"
+    )
+    assert any("forward" in d.message.lower() for d in warnings), (
+        f"Warning should mention 'forward', got messages: {[d.message for d in warnings]}"
+    )
+
+
+@pytest.mark.lsp
+def test_diagnostic_field_conflict():
+    """Signature ``"text -> text"`` (same field on both sides) produces an Error."""
+    code = 'pred = dspy.Predict("text -> text")'
+    diags = get_diagnostics(code)
+    errors = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Error]
+    assert len(errors) > 0, f"Expected Error for conflicting field 'text', got: {diags}"
+
+
+@pytest.mark.lsp
+def test_diagnostic_clean_code():
+    """A valid DSPy module produces no diagnostics."""
+    code = """
+import dspy
+from dspygen.utils.dspy_tools import init_dspy
+
+
+class SummarizerModule(dspy.Module):
+    \"\"\"Summarizes text.\"\"\"
+
+    def forward(self, text):
+        pred = dspy.Predict("text -> summary")
+        return pred(text=text).summary
+"""
+    diags = get_diagnostics(code)
+    assert diags == [], f"Expected no diagnostics for valid code, got: {diags}"
+
+
+@pytest.mark.lsp
+def test_diagnostic_non_snake_case():
+    """Signature ``"MyField -> output"`` produces a Warning diagnostic."""
+    code = 'pred = dspy.Predict("MyField -> output")'
+    diags = get_diagnostics(code)
+    warnings = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Warning]
+    assert len(warnings) > 0, (
+        f"Expected Warning for non-snake_case field 'MyField', got: {diags}"
+    )
+
+
+# ---------------------------------------------------------------------------
+# definition.py tests
+# ---------------------------------------------------------------------------
+
+
+@pytest.mark.lsp
+def test_definition_dspygen_module():
+    """Cursor on ``GenDspyModule`` resolves to a Location in the modules/ directory."""
+    code = "from dspygen.modules.gen_dspy_module_class import GenDspyModule"
+    col = code.index("GenDspyModule") + 5
+    result = get_definition(code, line=0, character=col)
+    assert result is not None
+    assert isinstance(result, lsp_types.Location)
+    assert "modules" in result.uri or "gen_dspy" in result.uri
+
+
+@pytest.mark.lsp
+def test_definition_unknown_class():
+    """Cursor on an unrecognised class name returns None gracefully."""
+    code = "x = UnknownClassXyzzy123()"
+    col = code.index("UnknownClassXyzzy123") + 5
+    result = get_definition(code, line=0, character=col)
+    assert result is None
+
+
+@pytest.mark.lsp
+def test_definition_returns_location():
+    """The returned object has ``uri`` and ``range`` fields (Location interface)."""
+    code = "from dspygen.modules import NaturalLanguageToSQLModule"
+    col = code.index("NaturalLanguageToSQLModule") + 10
+    result = get_definition(code, line=0, character=col)
+    assert result is not None
+    assert hasattr(result, "uri")
+    assert hasattr(result, "range")
+    assert result.uri.startswith("file://")
+    assert isinstance(result.range, lsp_types.Range)
