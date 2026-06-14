"""Mock factories for dspygen testing."""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch


class MockLM:
    """A mock DSPy LM that returns deterministic outputs based on input hash.

    Can be pre-loaded with specific responses for known prompts.

    Example::

        lm = MockLM(responses={"What is 2+2?": "4"})
        result = lm("What is 2+2?")
        # result == {"choices": [{"text": "4"}]}
    """

    def __init__(self, responses: dict | None = None) -> None:
        self.responses: dict[str, str] = responses or {}
        self.history: list[dict[str, Any]] = []

    def _get_response(self, prompt: str) -> str:
        """Return a pre-loaded response or a deterministic hash-based fallback."""
        if prompt in self.responses:
            return self.responses[prompt]
        # Deterministic output based on input hash
        digest = hashlib.md5(prompt.encode(), usedforsecurity=False).hexdigest()[:8]
        return f"mock_output_{digest}"

    def __call__(self, prompt: str, **kwargs: Any) -> dict:
        text = self._get_response(prompt)
        call_record = {"prompt": prompt, "kwargs": kwargs, "response": text}
        self.history.append(call_record)
        return {"choices": [{"text": text}]}

    def request(self, prompt: str, **kwargs: Any) -> dict:
        """Alias for __call__ — same behaviour, same history recording."""
        return self.__call__(prompt, **kwargs)

    def __repr__(self) -> str:  # pragma: no cover
        return f"MockLM(responses={len(self.responses)}, calls={len(self.history)})"


class MockPredict:
    """Mock dspy.Predict that captures all calls.

    All calls are appended to the class-level ``calls`` list so tests can
    inspect them after the fact.

    Example::

        pred = MockPredict("question -> answer")
        result = pred(question="What is AI?")
        assert result.output == "mock"
        assert MockPredict.calls[-1]["question"] == "What is AI?"
    """

    calls: list[dict[str, Any]] = []

    def __init__(self, signature: str = "", **kwargs: Any) -> None:
        self.signature = signature
        self._kwargs = kwargs
        # Parse output field names from signature, e.g. "question -> answer, summary"
        self._output_fields: list[str] = []
        if "->" in signature:
            output_part = signature.split("->", 1)[1]
            self._output_fields = [f.strip() for f in output_part.split(",") if f.strip()]

    def __call__(self, **kwargs: Any) -> SimpleNamespace:
        MockPredict.calls.append(dict(kwargs))
        ns = SimpleNamespace(output="mock")
        # Populate each declared output field with a mock value
        for field in self._output_fields:
            setattr(ns, field, "mock")
        return ns

    @classmethod
    def reset(cls) -> None:
        """Clear recorded calls between tests."""
        cls.calls.clear()


def make_module_runner(module_class: type, responses: dict | None = None):
    """Return a callable that runs *module_class* with MockLM configured.

    The returned runner patches ``dspy.settings`` so the module sees a real
    (but mock) LM without touching any global state permanently.

    Example::

        runner = make_module_runner(MyDSPyModule)
        result = runner(question="Hello")
    """
    mock_lm = MockLM(responses=responses)

    def runner(**kwargs: Any) -> Any:
        try:
            import dspy
        except ImportError as exc:
            raise ImportError("dspy is required to use make_module_runner") from exc

        with _patch_dspy_lm(mock_lm):
            instance = module_class()
            try:
                return instance.forward(**kwargs)
            except AttributeError:
                return instance(**kwargs)

    return runner


@contextmanager
def mock_lm_context(responses: dict | None = None):
    """Context manager that patches dspy.settings with a MockLM instance.

    Example::

        with mock_lm_context({"hello": "world"}) as lm:
            result = my_predictor(input="hello")
        assert lm.history  # calls were recorded
    """
    try:
        import dspy
    except ImportError as exc:
        raise ImportError("dspy is required to use mock_lm_context") from exc

    lm = MockLM(responses=responses)
    with _patch_dspy_lm(lm):
        yield lm


@contextmanager
def patch_dspy_predict(output: str = "mock_output"):
    """Context manager that patches dspy.Predict to return a fixed *output*.

    Example::

        with patch_dspy_predict("4") as mock_cls:
            pred = dspy.Predict("question -> answer")
            result = pred(question="2+2?")
            assert result.answer == "4"
    """
    mock_result = MagicMock()
    mock_result.output = output
    mock_result.answer = output
    mock_result.text = output

    with patch("dspy.Predict.__call__", return_value=mock_result) as mock_cls:
        yield mock_cls


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _patch_dspy_lm(lm: MockLM):
    """Return a context manager that sets dspy's active LM to *lm*."""
    try:
        import dspy
    except ImportError as exc:
        raise ImportError("dspy is required") from exc

    original = getattr(dspy.settings, "lm", None)

    class _Ctx:
        def __enter__(self):
            try:
                dspy.settings.configure(lm=lm)
            except Exception:
                pass
            return lm

        def __exit__(self, *_):
            try:
                if original is not None:
                    dspy.settings.configure(lm=original)
            except Exception:
                pass

    return _Ctx()
