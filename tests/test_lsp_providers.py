"""Tests for LSP providers.

Each provider's internal logic is tested directly — no real LSP server is
started. For providers that wrap their logic in a ``register_X(server)``
closure, we test the underlying helper functions directly.
"""
from __future__ import annotations

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
    """Build and return the module index used by providers."""
    from dspygen.lsp.analysis.module_index import ModuleIndex
    idx = ModuleIndex()
    idx.build()
    return idx


# ---------------------------------------------------------------------------
# completion.py tests
# ---------------------------------------------------------------------------


@pytest.mark.lsp
def test_completion_after_dspy_predict(module_index):
    """Typing ``dspy.Predict(`` triggers signature suggestions."""
    from dspygen.lsp.providers.completion import _completions_for_predict

    line = "pred = dspy.Predict("
    items = _completions_for_predict(line, module_index)
    assert len(items) > 0
    # All items should include a signature string (contain "->")
    sig_items = [i for i in items if "->" in i.label]
    assert len(sig_items) > 0, f"Expected signature labels with '->', got: {[i.label for i in items[:5]]}"


@pytest.mark.lsp
def test_completion_after_module_import(module_index):
    """Typing ``from dspygen.modules import `` triggers module name completions."""
    from dspygen.lsp.providers.completion import _completions_for_import

    items = _completions_for_import("", module_index)
    assert len(items) > 0
    labels = [item.label for item in items]
    assert any("Module" in label for label in labels), (
        f"Expected module names in completions, got first 5: {labels[:5]}"
    )


@pytest.mark.lsp
def test_completion_init_dspy_model():
    """Typing ``init_dspy(model=`` triggers model name completions."""
    from dspygen.lsp.providers.completion import _completions_for_init_dspy

    items = _completions_for_init_dspy()
    assert len(items) > 0
    # All items should be model name strings (non-empty labels)
    for item in items:
        assert item.label, f"Completion item has empty label"


@pytest.mark.lsp
def test_completion_items_have_documentation(module_index):
    """Completions from dspy.Predict( that reference a module have documentation."""
    from dspygen.lsp.providers.completion import _completions_for_predict

    items = _completions_for_predict("dspy.Predict(", module_index)
    assert len(items) > 0
    # The module-derived completions (with "from <Module>" detail) should have docs
    module_items = [i for i in items if i.detail and "from " in i.detail]
    assert len(module_items) > 0, "Expected module-derived completion items"
    for item in module_items:
        assert item.documentation is not None, (
            f"Module completion item {item.label!r} has no documentation"
        )


@pytest.mark.lsp
def test_completion_returns_completion_list(module_index):
    """Provider returns a list of CompletionItems (not a CompletionList object)."""
    from dspygen.lsp.providers.completion import _completions_for_predict

    items = _completions_for_predict("dspy.Predict(", module_index)
    assert isinstance(items, list)
    for item in items:
        assert isinstance(item, lsp_types.CompletionItem)


# ---------------------------------------------------------------------------
# hover.py tests
# ---------------------------------------------------------------------------


@pytest.mark.lsp
def test_hover_on_dspy_predict_call():
    """Hovering over ``Predict`` returns markdown with input/output description."""
    from dspygen.lsp.providers.hover import _word_at_position, _make_hover, _PREDICT_RE, _SIG_LITERAL_RE, _format_signature

    code = "pred = dspy.Predict('text -> summary')"
    col = code.index("Predict") + 3  # mid-word
    pos = lsp_types.Position(line=0, character=col)
    word = _word_at_position(code, pos)
    assert word == "Predict"
    assert _PREDICT_RE.search(code)
    # Compose the hover as the provider would
    m = _SIG_LITERAL_RE.search(code)
    assert m is not None
    sig_str = m.group(1).strip()
    md = f"## `dspy.{word}`\n\n**Parsed signature:**\n\n" + _format_signature(sig_str)
    hover = _make_hover(md)
    assert isinstance(hover, lsp_types.Hover)
    assert "Predict" in hover.contents.value


@pytest.mark.lsp
def test_hover_on_signature_string():
    """Hovering on a signature string ``"text -> summary"`` returns parsed fields."""
    from dspygen.lsp.providers.hover import _format_signature, _make_hover

    sig_str = "text -> summary"
    formatted = _format_signature(sig_str)
    assert "text" in formatted
    assert "summary" in formatted
    hover = _make_hover("## DSPy Signature\n\n" + formatted)
    assert isinstance(hover, lsp_types.Hover)
    content = hover.contents
    assert isinstance(content, lsp_types.MarkupContent)
    assert "text" in content.value
    assert "summary" in content.value


@pytest.mark.lsp
def test_hover_on_unknown_symbol(module_index):
    """Hovering on an unrecognised token should return None (module not in index)."""
    from dspygen.lsp.providers.hover import _word_at_position

    code = "x = totally_unknown_symbol_xyz"
    col = code.index("totally_unknown_symbol_xyz") + 5
    pos = lsp_types.Position(line=0, character=col)
    word = _word_at_position(code, pos)
    # The word should not be in the module index
    result = module_index.get_by_name(word)
    assert result is None, f"Expected None for unknown symbol, got: {result}"


@pytest.mark.lsp
def test_hover_returns_markdown():
    """Any hover result uses MarkupKind.Markdown."""
    from dspygen.lsp.providers.hover import _make_hover, _format_signature

    sig_str = "question, context -> answer"
    md = "## DSPy Signature\n\n" + _format_signature(sig_str)
    hover = _make_hover(md)
    assert isinstance(hover, lsp_types.Hover)
    content = hover.contents
    assert isinstance(content, lsp_types.MarkupContent)
    assert content.kind == lsp_types.MarkupKind.Markdown


# ---------------------------------------------------------------------------
# diagnostics.py tests
# ---------------------------------------------------------------------------


@pytest.mark.lsp
def test_diagnostic_invalid_signature():
    """``dspy.Predict("input -> ")`` produces an Error diagnostic for the empty output."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics

    code = 'pred = dspy.Predict("input -> ")'
    diags = _compute_diagnostics(code)
    assert len(diags) > 0, "Expected at least one diagnostic for invalid signature"
    errors = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Error]
    assert len(errors) > 0, f"Expected Error severity diagnostic, got: {diags}"


@pytest.mark.lsp
def test_diagnostic_missing_forward():
    """A ``dspy.Module`` subclass without a ``forward`` method produces a Warning."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics

    code = """
import dspy

class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()
"""
    diags = _compute_diagnostics(code)
    warnings = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Warning]
    assert len(warnings) > 0, (
        f"Expected Warning about missing forward method, got diagnostics: {diags}"
    )
    assert any("forward" in d.message.lower() for d in warnings), (
        f"Warning should mention 'forward', got messages: {[d.message for d in warnings]}"
    )


@pytest.mark.lsp
def test_diagnostic_field_conflict():
    """Signature ``"text -> text"`` (same field on both sides) produces an Error."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics

    code = 'pred = dspy.Predict("text -> text")'
    diags = _compute_diagnostics(code)
    errors = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Error]
    assert len(errors) > 0, f"Expected Error for conflicting field 'text', got: {diags}"


@pytest.mark.lsp
def test_diagnostic_clean_code():
    """A valid DSPy module produces no diagnostics."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics

    code = """
import dspy
from dspygen.utils.dspy_tools import init_dspy


class SummarizerModule(dspy.Module):
    \"\"\"Summarizes text.\"\"\"

    def forward(self, text):
        pred = dspy.Predict("text -> summary")
        return pred(text=text).summary
"""
    diags = _compute_diagnostics(code)
    assert diags == [], f"Expected no diagnostics for valid code, got: {diags}"


@pytest.mark.lsp
def test_diagnostic_non_snake_case():
    """Signature ``"MyField -> output"`` produces a Warning diagnostic."""
    from dspygen.lsp.providers.diagnostics import _compute_diagnostics

    code = 'pred = dspy.Predict("MyField -> output")'
    diags = _compute_diagnostics(code)
    warnings = [d for d in diags if d.severity == lsp_types.DiagnosticSeverity.Warning]
    assert len(warnings) > 0, (
        f"Expected Warning for non-snake_case field 'MyField', got: {diags}"
    )


# ---------------------------------------------------------------------------
# definition.py tests
# ---------------------------------------------------------------------------


@pytest.mark.lsp
def test_definition_dspygen_module(module_index):
    """The definition helper for GenDspyModule resolves to a file in modules/ dir."""
    from dspygen.lsp.providers.definition import _word_at_position, _path_to_uri
    from lsprotocol import types as lsp_types

    code = "from dspygen.modules.gen_dspy_module_class import GenDspyModule"
    col = code.index("GenDspyModule") + 5
    pos = lsp_types.Position(line=0, character=col)
    word = _word_at_position(code, pos)
    assert word == "GenDspyModule"
    info = module_index.get_by_name(word)
    assert info is not None, "GenDspyModule should be in the index"
    uri = _path_to_uri(info.file_path)
    assert "modules" in uri or "gen_dspy" in uri


@pytest.mark.lsp
def test_definition_unknown_class(module_index):
    """Looking up an unrecognised class name returns None."""
    from dspygen.lsp.providers.definition import _word_at_position
    from lsprotocol import types as lsp_types

    code = "x = UnknownClassXyzzy123()"
    col = code.index("UnknownClassXyzzy123") + 5
    pos = lsp_types.Position(line=0, character=col)
    word = _word_at_position(code, pos)
    result = module_index.get_by_name(word)
    assert result is None


@pytest.mark.lsp
def test_definition_returns_location(module_index):
    """The Location for NaturalLanguageToSQLModule has ``uri`` and ``range`` fields."""
    from dspygen.lsp.providers.definition import _word_at_position, _path_to_uri, _zero_range
    from lsprotocol import types as lsp_types

    code = "from dspygen.modules import NaturalLanguageToSQLModule"
    col = code.index("NaturalLanguageToSQLModule") + 10
    pos = lsp_types.Position(line=0, character=col)
    word = _word_at_position(code, pos)
    info = module_index.get_by_name(word)
    assert info is not None
    uri = _path_to_uri(info.file_path)
    location = lsp_types.Location(uri=uri, range=_zero_range())
    assert hasattr(location, "uri")
    assert hasattr(location, "range")
    assert location.uri.startswith("file://")
    assert isinstance(location.range, lsp_types.Range)
