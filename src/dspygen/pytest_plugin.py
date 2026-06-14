"""DSPyGen pytest plugin — fixtures, marks, and assertions for DSPy testing.

Register by adding to pyproject.toml:
    [tool.poetry.plugins."pytest11"]
    dspygen = "dspygen.pytest_plugin"

Or install directly with:
    pip install dspygen
"""
from __future__ import annotations

import os
from typing import Any, Callable
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Custom marks
# ---------------------------------------------------------------------------

def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "dspy_module: marks tests that require DSPy LM configuration",
    )
    config.addinivalue_line(
        "markers",
        "requires_openai: skip test if OPENAI_API_KEY is not set",
    )
    config.addinivalue_line(
        "markers",
        "requires_ollama: skip test if Ollama is not running",
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Auto-skip tests based on marks."""
    if item.get_closest_marker("requires_openai"):
        if not os.environ.get("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set — skipping OpenAI test")

    if item.get_closest_marker("requires_ollama"):
        import socket
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        # Parse host:port
        if "://" in host:
            host = host.split("://", 1)[1]
        parts = host.split(":")
        hostname = parts[0]
        port = int(parts[1]) if len(parts) > 1 else 11434
        try:
            sock = socket.create_connection((hostname, port), timeout=1)
            sock.close()
        except OSError:
            pytest.skip(f"Ollama not running at {host} — skipping Ollama test")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def dspy_lm(request: pytest.FixtureRequest):
    """Configure DSPy with a mock LM for tests.

    Usage::

        def test_something(dspy_lm):
            # dspy is configured with a mock LM
            result = my_module(input="hello")
            assert result is not None
    """
    import dspy

    mock_lm = MagicMock()
    mock_lm.return_value = {"completions": [{"text": "mock output", "answer": "mock answer"}]}
    mock_lm.__call__ = MagicMock(return_value={"completions": [{"text": "mock output"}]})

    with patch.object(dspy.settings, "lm", mock_lm):
        original_lm = getattr(dspy.settings, "lm", None)
        try:
            # Try the modern dspy.LM mock approach
            dspy.settings.configure(lm=mock_lm)
        except Exception:
            pass
        yield mock_lm
        # Restore original
        try:
            if original_lm is not None:
                dspy.settings.configure(lm=original_lm)
        except Exception:
            pass


@pytest.fixture
def dspygen_module_runner(dspy_lm):
    """Fixture that runs any dspygen module with a mocked LM.

    Usage::

        def test_blog_module(dspygen_module_runner):
            result = dspygen_module_runner("blog_module", topic="AI in 2025")
            assert result is not None
    """
    def _run_module(module_name: str, **kwargs: Any) -> Any:
        import importlib
        try:
            mod = importlib.import_module(f"dspygen.modules.{module_name}")
        except ImportError as e:
            raise ImportError(f"Module 'dspygen.modules.{module_name}' not found: {e}") from e

        # Find the module class (convention: ModuleNameModule or first class ending in Module)
        import inspect
        module_cls = None
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if name.endswith("Module") and obj.__module__ == mod.__name__:
                module_cls = obj
                break

        if module_cls is None:
            raise ValueError(f"No Module class found in dspygen.modules.{module_name}")

        instance = module_cls()
        try:
            return instance.forward(**kwargs)
        except Exception:
            return instance(**kwargs)

    return _run_module


@pytest.fixture
def mock_dspy_predict():
    """Auto-mock dspy.Predict to return deterministic outputs.

    Usage::

        def test_with_predict(mock_dspy_predict):
            import dspy
            predictor = dspy.Predict("question -> answer")
            result = predictor(question="What is AI?")
            # result.answer will be "mock_answer"
    """
    mock_result = MagicMock()
    mock_result.answer = "mock_answer"
    mock_result.output = "mock_output"
    mock_result.text = "mock_text"
    mock_result.completions = [{"text": "mock completion"}]

    with patch("dspy.Predict.__call__", return_value=mock_result) as mock_call:
        yield mock_call


@pytest.fixture
def pipeline_executor():
    """Fixture for DSL pipeline execution in tests.

    Usage::

        def test_pipeline(pipeline_executor):
            yaml_content = '''
            steps:
              - module: blog_module
                args:
                  topic: "Test Topic"
            '''
            result = pipeline_executor(yaml_content)
            assert result is not None
    """
    def _execute_pipeline(yaml_content: str) -> Any:
        import yaml
        try:
            pipeline_def = yaml.safe_load(yaml_content)
        except Exception as e:
            raise ValueError(f"Invalid pipeline YAML: {e}") from e

        results = []
        steps = pipeline_def.get("steps", [])
        for step in steps:
            module_name = step.get("module", "")
            args = step.get("args", {})
            results.append({"module": module_name, "args": args, "status": "skipped_in_test"})

        return {"steps": results, "status": "completed"}

    return _execute_pipeline


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------

def assert_module_output(
    module: Any,
    inputs: dict[str, Any],
    expected: dict[str, Any],
    *,
    partial_match: bool = True,
) -> None:
    """Assert that a dspygen module produces the expected output.

    Args:
        module: An instantiated dspygen module.
        inputs: Dictionary of input field names to values.
        expected: Dictionary of expected output field names to values.
        partial_match: If True, only check the keys present in `expected`.

    Example::

        assert_module_output(
            MyModule(),
            inputs={"question": "What is 2+2?"},
            expected={"answer": "4"},
        )
    """
    try:
        result = module.forward(**inputs)
    except Exception:
        result = module(**inputs)

    if partial_match:
        for key, value in expected.items():
            actual = getattr(result, key, None)
            assert actual is not None, f"Output missing field '{key}'"
            if value is not None:
                assert actual == value, f"Field '{key}': expected {value!r}, got {actual!r}"
    else:
        for key, value in expected.items():
            actual = getattr(result, key, None)
            assert actual == value, f"Field '{key}': expected {value!r}, got {actual!r}"


def assert_signature_valid(sig_str: str) -> None:
    """Assert that a DSPy signature string is syntactically valid.

    Args:
        sig_str: A DSPy signature string like "question -> answer" or
                 "context, question -> reasoning, answer".

    Example::

        assert_signature_valid("question, context -> answer")
        assert_signature_valid("input_text -> summary, keywords")
    """
    import dspy

    if not sig_str or not isinstance(sig_str, str):
        raise AssertionError(f"Signature must be a non-empty string, got: {sig_str!r}")

    if "->" not in sig_str:
        raise AssertionError(
            f"Invalid DSPy signature '{sig_str}': must contain '->' separating inputs from outputs"
        )

    parts = sig_str.split("->")
    if len(parts) != 2:
        raise AssertionError(
            f"Invalid DSPy signature '{sig_str}': must have exactly one '->' separator"
        )

    input_part, output_part = parts
    inputs = [f.strip() for f in input_part.split(",") if f.strip()]
    outputs = [f.strip() for f in output_part.split(",") if f.strip()]

    if not inputs:
        raise AssertionError(f"Signature '{sig_str}' has no input fields")
    if not outputs:
        raise AssertionError(f"Signature '{sig_str}' has no output fields")

    # Attempt to create the signature via dspy
    try:
        sig = dspy.Signature(sig_str)
        assert sig is not None
    except Exception as e:
        raise AssertionError(f"DSPy rejected signature '{sig_str}': {e}") from e
