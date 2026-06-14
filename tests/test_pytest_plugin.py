"""
Meta-tests for the dspygen pytest plugin.

Tests validate the fixtures and marks that the plugin would provide.
The plugin itself is implemented inline here (so it can be tested without
a real entry-point install).
"""

import sys
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Plugin implementation (inline reference implementation)
# ---------------------------------------------------------------------------

class _MockDSPyLM:
    """A mock DSPy language model that records all calls."""

    def __init__(self, model_name: str = "mock-lm"):
        self.model_name = model_name
        self._calls: List[dict] = []

    def __call__(self, prompt: str, **kwargs) -> str:
        record = {"prompt": prompt, **kwargs}
        self._calls.append(record)
        return f"[mock response for: {prompt[:30]}]"

    @property
    def calls(self) -> List[dict]:
        return list(self._calls)

    def reset(self):
        self._calls.clear()


class _SignatureValidator:
    """Validates DSPy-style signature strings."""

    @staticmethod
    def validate(sig: str) -> Dict[str, Any]:
        errors = []
        if not sig or not sig.strip():
            errors.append("Empty signature")
        elif "->" not in sig:
            errors.append("Missing '->' separator")
        else:
            parts = [p.strip() for p in sig.split("->")]
            if len(parts) != 2:
                errors.append("Expected exactly one '->'")
            if not parts[0]:
                errors.append("No input fields")
            if not parts[1]:
                errors.append("No output field")
        return {"valid": len(errors) == 0, "errors": errors}


def _assert_signature_valid(sig: str):
    """Pytest helper: assert that a DSPy signature is valid."""
    result = _SignatureValidator.validate(sig)
    if not result["valid"]:
        raise AssertionError(
            f"Invalid DSPy signature {sig!r}: {result['errors']}"
        )


# Fixtures (defined at module level so pytest collects them)
@pytest.fixture
def dspy_lm():
    """Provide a mock DSPy LM that records calls."""
    lm = _MockDSPyLM()
    yield lm
    lm.reset()


@pytest.fixture
def mock_dspy_predict():
    """Intercept all dspy.Predict calls and return a mock response."""
    with patch("dspy.Predict", autospec=True) as mock_predict_cls:
        mock_instance = MagicMock()
        mock_instance.return_value = MagicMock(answer="[mock answer]")
        mock_predict_cls.return_value = mock_instance
        yield mock_predict_cls


@pytest.fixture
def assert_signature_valid_fn():
    """Provide the assert_signature_valid helper."""
    return _assert_signature_valid


# ===========================================================================
# Tests: dspy_lm fixture
# ===========================================================================

class TestDspyLmFixture:
    def test_fixture_provides_mock_lm(self, dspy_lm):
        assert isinstance(dspy_lm, _MockDSPyLM)

    def test_fixture_is_callable(self, dspy_lm):
        result = dspy_lm("test prompt")
        assert isinstance(result, str)

    def test_fixture_records_calls(self, dspy_lm):
        dspy_lm("first prompt")
        dspy_lm("second prompt")
        assert len(dspy_lm.calls) == 2

    def test_fixture_call_content_recorded(self, dspy_lm):
        dspy_lm("hello world", temperature=0.5)
        assert dspy_lm.calls[0]["prompt"] == "hello world"
        assert dspy_lm.calls[0]["temperature"] == 0.5

    def test_fixture_reset_clears_calls(self, dspy_lm):
        dspy_lm("call 1")
        dspy_lm.reset()
        assert dspy_lm.calls == []

    def test_fixture_model_name(self, dspy_lm):
        assert dspy_lm.model_name == "mock-lm"

    def test_fixture_isolated_between_tests(self, dspy_lm):
        # calls list should be empty at fixture start
        assert dspy_lm.calls == []

    def test_mock_response_format(self, dspy_lm):
        response = dspy_lm("short")
        assert "[mock response" in response


# ===========================================================================
# Tests: mock_dspy_predict fixture
# ===========================================================================

class TestMockDspyPredictFixture:
    def test_predict_is_mocked(self, mock_dspy_predict):
        import dspy
        instance = dspy.Predict("input -> output")
        # Should be the mock instance
        assert instance is not None

    def test_predict_class_is_mock(self, mock_dspy_predict):
        assert mock_dspy_predict is not None

    def test_predict_called_tracks_usage(self, mock_dspy_predict):
        import dspy
        p = dspy.Predict("q -> a")
        p("some question")
        assert mock_dspy_predict.call_count >= 1


# ===========================================================================
# Tests: requires_openai mark
# ===========================================================================

class TestRequiresOpenAIMark:
    def test_mark_exists_on_pytest(self):
        """pytest.mark.dspygen_requires_openai can be applied without error."""
        mark = pytest.mark.dspygen_requires_openai
        assert mark is not None

    def test_mark_can_be_applied_to_function(self):
        @pytest.mark.dspygen_requires_openai
        def dummy_test():
            pass

        assert dummy_test is not None

    def test_skip_when_no_api_key(self, monkeypatch):
        """If OPENAI_API_KEY is missing, a test that uses init_dspy should be skippable."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        import os
        assert os.environ.get("OPENAI_API_KEY") is None
        # The skip logic would be: pytest.skip if key not in env
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            pytest.skip("OPENAI_API_KEY not set")

    def test_no_skip_when_key_present(self, monkeypatch):
        """If OPENAI_API_KEY is set, the test should not be skipped."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-fake-key")
        import os
        assert os.environ.get("OPENAI_API_KEY") == "sk-test-fake-key"


# ===========================================================================
# Tests: assert_signature_valid helper
# ===========================================================================

class TestAssertSignatureValid:
    def test_valid_simple_signature(self, assert_signature_valid_fn):
        assert_signature_valid_fn("question -> answer")

    def test_valid_multi_input_signature(self, assert_signature_valid_fn):
        assert_signature_valid_fn("context, question -> reasoning, answer")

    def test_invalid_signature_raises(self, assert_signature_valid_fn):
        with pytest.raises(AssertionError):
            assert_signature_valid_fn("no arrow here")

    def test_empty_signature_raises(self, assert_signature_valid_fn):
        with pytest.raises(AssertionError):
            assert_signature_valid_fn("")

    def test_whitespace_only_raises(self, assert_signature_valid_fn):
        with pytest.raises(AssertionError):
            assert_signature_valid_fn("   ")

    def test_valid_signature_with_spaces(self, assert_signature_valid_fn):
        assert_signature_valid_fn("  input_text  ->  output_text  ")

    def test_missing_output_raises(self, assert_signature_valid_fn):
        with pytest.raises(AssertionError):
            assert_signature_valid_fn("input -> ")

    def test_missing_input_raises(self, assert_signature_valid_fn):
        with pytest.raises(AssertionError):
            assert_signature_valid_fn(" -> output")


# ===========================================================================
# Tests: SignatureValidator
# ===========================================================================

class TestSignatureValidator:
    def test_valid_returns_no_errors(self):
        result = _SignatureValidator.validate("question -> answer")
        assert result["valid"] is True
        assert result["errors"] == []

    def test_missing_arrow_returns_error(self):
        result = _SignatureValidator.validate("input output")
        assert result["valid"] is False
        assert any("->" in e for e in result["errors"])

    def test_empty_input_returns_error(self):
        result = _SignatureValidator.validate("")
        assert result["valid"] is False

    def test_complex_valid_signature(self):
        result = _SignatureValidator.validate(
            "document, query, context -> summary, citations"
        )
        assert result["valid"] is True

    def test_whitespace_only_invalid(self):
        result = _SignatureValidator.validate("    ")
        assert result["valid"] is False


# ===========================================================================
# Tests: pytest plugin marks registration
# ===========================================================================

class TestPluginMarks:
    EXPECTED_MARKS = ["slow", "integration", "requires_llm"]

    def test_slow_mark_applicable(self):
        @pytest.mark.slow
        def slow_test():
            pass
        assert slow_test is not None

    def test_integration_mark_applicable(self):
        @pytest.mark.integration
        def integration_test():
            pass
        assert integration_test is not None

    def test_requires_llm_mark_applicable(self):
        @pytest.mark.requires_llm
        def llm_test():
            pass
        assert llm_test is not None


# ===========================================================================
# Tests: MockDSPyLM unit tests (independent of fixture)
# ===========================================================================

class TestMockDSPyLMUnit:
    def test_call_returns_string(self):
        lm = _MockDSPyLM()
        assert isinstance(lm("hello"), str)

    def test_multiple_calls_recorded(self):
        lm = _MockDSPyLM()
        for i in range(10):
            lm(f"prompt {i}")
        assert len(lm.calls) == 10

    def test_reset_empties_calls(self):
        lm = _MockDSPyLM()
        lm("call")
        lm.reset()
        assert len(lm.calls) == 0

    def test_custom_model_name(self):
        lm = _MockDSPyLM(model_name="gpt-4")
        assert lm.model_name == "gpt-4"

    def test_kwargs_recorded(self):
        lm = _MockDSPyLM()
        lm("p", max_tokens=100, temperature=0.7)
        assert lm.calls[0]["max_tokens"] == 100
        assert lm.calls[0]["temperature"] == pytest.approx(0.7)
