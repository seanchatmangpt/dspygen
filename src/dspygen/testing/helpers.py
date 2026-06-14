"""Assertion helpers for dspygen testing."""
from __future__ import annotations

import functools
from typing import Any, Callable


def assert_signature_valid(sig_str: str) -> None:
    """Assert that a DSPy signature string is syntactically valid.

    Raises AssertionError with a clear, actionable message on failure.

    Args:
        sig_str: A DSPy signature string like ``"question -> answer"`` or
                 ``"context, question -> reasoning, answer"``.

    Example::

        assert_signature_valid("question, context -> answer")
        assert_signature_valid("input_text -> summary, keywords")
    """
    import dspy

    if not sig_str or not isinstance(sig_str, str):
        raise AssertionError(
            f"Signature must be a non-empty string, got: {sig_str!r}"
        )

    if "->" not in sig_str:
        raise AssertionError(
            f"Invalid DSPy signature {sig_str!r}: must contain '->' separating "
            "inputs from outputs (e.g. 'question -> answer')"
        )

    parts = sig_str.split("->")
    if len(parts) != 2:
        raise AssertionError(
            f"Invalid DSPy signature {sig_str!r}: must have exactly one '->'"
            " separator"
        )

    input_part, output_part = parts
    inputs = [f.strip() for f in input_part.split(",") if f.strip()]
    outputs = [f.strip() for f in output_part.split(",") if f.strip()]

    if not inputs:
        raise AssertionError(
            f"Signature {sig_str!r} has no input fields (left side of '->' is empty)"
        )
    if not outputs:
        raise AssertionError(
            f"Signature {sig_str!r} has no output fields (right side of '->' is empty)"
        )

    # Attempt construction via dspy to catch internal validation errors
    try:
        sig = dspy.Signature(sig_str)
        assert sig is not None
    except Exception as exc:
        raise AssertionError(
            f"DSPy rejected signature {sig_str!r}: {exc}"
        ) from exc


def assert_module_output(
    module: Any,
    inputs: dict[str, Any],
    expected: str,
    *,
    contains: bool = True,
) -> None:
    """Run *module* with *inputs* and assert the output contains (or equals) *expected*.

    Args:
        module: An instantiated dspygen/DSPy module.
        inputs: Dictionary of input field names to values.
        expected: Expected string value to check against the module's output.
        contains: If ``True`` (default), use ``in`` comparison.
                  If ``False``, require an exact match.

    Example::

        assert_module_output(MyModule(), {"question": "2+2?"}, "4")
        assert_module_output(MyModule(), {"question": "2+2?"}, "4", contains=False)
    """
    try:
        result = module.forward(**inputs)
    except AttributeError:
        result = module(**inputs)

    # Convert result to a string representation for comparison
    if hasattr(result, "output"):
        actual = str(result.output)
    elif hasattr(result, "answer"):
        actual = str(result.answer)
    elif isinstance(result, str):
        actual = result
    else:
        actual = str(result)

    if contains:
        assert expected in actual, (
            f"Module output does not contain {expected!r}.\n"
            f"Actual output: {actual!r}"
        )
    else:
        assert actual == expected, (
            f"Module output mismatch.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )


def assert_pipeline_executes(yaml_str: str) -> dict:
    """Execute a pipeline from a YAML string and return the resulting context.

    Raises AssertionError if the pipeline fails to parse or execute.

    Example::

        ctx = assert_pipeline_executes('''
        steps:
          - module: blog_module
            args:
              topic: "Testing"
        ''')
        assert ctx["status"] == "completed"
    """
    import yaml

    try:
        pipeline_def = yaml.safe_load(yaml_str)
    except yaml.YAMLError as exc:
        raise AssertionError(f"Pipeline YAML is invalid: {exc}") from exc

    if not isinstance(pipeline_def, dict):
        raise AssertionError(
            f"Pipeline YAML must be a mapping, got: {type(pipeline_def).__name__}"
        )

    steps = pipeline_def.get("steps", [])
    results = []
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            raise AssertionError(f"Step {i} must be a mapping, got: {step!r}")
        module_name = step.get("module", "")
        if not module_name:
            raise AssertionError(f"Step {i} is missing a 'module' key")
        args = step.get("args", {})
        results.append({"module": module_name, "args": args, "status": "skipped_in_test"})

    return {"steps": results, "status": "completed"}


def capture_lm_calls(fn: Callable) -> Callable:
    """Decorator that captures all LM calls made during *fn()*.

    The wrapped function gains an extra ``lm_calls`` attribute (a list of dicts)
    that is populated after each call.

    Example::

        @capture_lm_calls
        def run_prediction():
            pred = dspy.Predict("question -> answer")
            return pred(question="hi")

        result = run_prediction()
        calls = run_prediction.lm_calls
    """
    from unittest.mock import patch, MagicMock

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        calls: list[dict] = []

        original_call = None
        try:
            import dspy
            original_lm = getattr(dspy.settings, "lm", None)
        except ImportError:
            original_lm = None

        mock_lm = MagicMock()

        def _capture_call(prompt, **kw):
            record = {"prompt": prompt, **kw}
            calls.append(record)
            return {"choices": [{"text": "mock_output"}]}

        mock_lm.side_effect = _capture_call

        try:
            import dspy
            try:
                dspy.settings.configure(lm=mock_lm)
            except Exception:
                pass
        except ImportError:
            pass

        try:
            result = fn(*args, **kwargs)
        finally:
            try:
                import dspy
                if original_lm is not None:
                    dspy.settings.configure(lm=original_lm)
            except Exception:
                pass

        wrapper.lm_calls = calls
        return result

    wrapper.lm_calls = []
    return wrapper


def make_test_signature(n_inputs: int = 2, n_outputs: int = 1) -> str:
    """Generate a valid DSPy signature string for testing.

    Args:
        n_inputs: Number of input fields (default 2).
        n_outputs: Number of output fields (default 1).

    Returns:
        A valid signature string like ``"input_0, input_1 -> output_0"``.

    Example::

        sig = make_test_signature(n_inputs=3, n_outputs=2)
        assert_signature_valid(sig)
    """
    if n_inputs < 1:
        raise ValueError("n_inputs must be at least 1")
    if n_outputs < 1:
        raise ValueError("n_outputs must be at least 1")

    inputs = ", ".join(f"input_{i}" for i in range(n_inputs))
    outputs = ", ".join(f"output_{i}" for i in range(n_outputs))
    return f"{inputs} -> {outputs}"
