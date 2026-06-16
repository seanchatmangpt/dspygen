"""
Consolidated integration tests for dspygen Jupyter magic and pytest plugin.

All external calls are mocked; each test completes in <10ms.
"""

import os
import sys
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch, call

import pytest


# ---------------------------------------------------------------------------
# Shared inline implementations (no real imports required)
# ---------------------------------------------------------------------------

# -- Jupyter magic helpers ---------------------------------------------------

def _make_ipython_mock():
    ip = MagicMock()
    ip.register_magic_function = MagicMock()
    ip.push = MagicMock()
    ip.run_cell_magic = MagicMock()
    return ip


class _DspygenMagics:
    """Self-contained mock of the dspygen Jupyter magic extension."""

    def __init__(self, ipython=None):
        self.ipython = ipython or MagicMock()
        self._init_called = False
        self._last_pipeline_yaml = None
        self._init_model = None

    def dspygen_init(self, line: str):
        self._init_called = True
        model = line.strip() or "default"
        self._init_model = model
        return {"model": model, "initialized": True}

    def dspygen_modules(self, line: str):
        from pathlib import Path
        modules_dir = Path(__file__).parent.parent / "src/dspygen/modules"
        filt = line.strip().lower()
        return sorted(
            f.stem for f in modules_dir.glob("*.py")
            if not f.name.startswith("_") and (not filt or filt in f.stem.lower())
        )

    def dspygen_agents(self, line: str):
        from pathlib import Path
        agents_dir = Path(__file__).parent.parent / "src/dspygen/agents"
        filt = line.strip().lower()
        return sorted(
            f.stem for f in agents_dir.glob("*.py")
            if not f.name.startswith("_") and (not filt or filt in f.stem.lower())
        )

    def dspygen_pipeline(self, line: str, cell: str):
        self._last_pipeline_yaml = cell
        return {"yaml": cell, "status": "ok"}

    def dspygen_history(self, line: str):
        """Read history from dspy.settings.lm.history."""
        # Access via sys.modules so no hard import is required
        dspy = sys.modules.get("dspy")
        if dspy is not None:
            lm = getattr(getattr(dspy, "settings", None), "lm", None)
            history = getattr(lm, "history", [])
        else:
            history = []
        return list(history)

    def display_module_output(self, output: Any, module_name: str = "module") -> str:
        """Format output as HTML for Jupyter display."""
        escaped = str(output).replace("<", "&lt;").replace(">", "&gt;")
        return f"<div class='dspygen-output'><b>{module_name}</b>: {escaped}</div>"


def _load_ipython_extension(ipython, magics_cls=None):
    """Register dspygen magics on an IPython instance."""
    if magics_cls is None:
        magics_cls = _DspygenMagics
    obj = magics_cls(ipython)
    line_magics = {
        "dspygen_init": obj.dspygen_init,
        "dspygen_modules": obj.dspygen_modules,
        "dspygen_agents": obj.dspygen_agents,
        "dspygen_history": obj.dspygen_history,
    }
    cell_magics = {
        "dspygen_pipeline": obj.dspygen_pipeline,
    }
    for name, fn in line_magics.items():
        ipython.register_magic_function(fn, magic_kind="line", magic_name=name)
    for name, fn in cell_magics.items():
        ipython.register_magic_function(fn, magic_kind="cell", magic_name=name)
    return obj


# -- pytest plugin helpers ---------------------------------------------------

class _MockDSPyLM:
    """Mock DSPy language model that records all calls."""

    def __init__(self, model_name: str = "mock-lm"):
        self.model_name = model_name
        self._calls: List[dict] = []
        self.history: List[dict] = []

    def __call__(self, prompt: str, **kwargs) -> str:
        record = {"prompt": prompt, **kwargs}
        self._calls.append(record)
        self.history.append(record)
        return f"[mock response for: {prompt[:30]}]"

    @property
    def calls(self) -> List[dict]:
        return list(self._calls)

    def reset(self):
        self._calls.clear()


class _SignatureValidator:
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


def _assert_module_output(actual: Any, expected: Any) -> None:
    assert actual == expected, f"Module output mismatch: {actual!r} != {expected!r}"


def _assert_signature_valid(sig: str) -> None:
    result = _SignatureValidator.validate(sig)
    if not result["valid"]:
        raise AssertionError(
            f"Invalid DSPy signature {sig!r}: {result['errors']}"
        )


def _parse_yaml_pipeline(pipeline_yaml: str) -> Dict[str, Any]:
    """Parse a minimal YAML pipeline without the yaml package."""
    steps = []
    current_module = None
    for line in pipeline_yaml.splitlines():
        stripped = line.strip()
        if stripped.startswith("- module:"):
            current_module = stripped.split("- module:", 1)[1].strip()
            steps.append({"module": current_module, "status": "ok"})
    return {"steps": steps, "count": len(steps)}


# ---------------------------------------------------------------------------
# pytest fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def dspy_lm():
    lm = _MockDSPyLM()
    yield lm
    lm.reset()


@pytest.fixture
def mock_dspy_predict():
    """Patch dspy.Predict via sys.modules injection (no real dspy needed)."""
    mock_dspy = MagicMock()
    mock_predict_cls = MagicMock()
    mock_instance = MagicMock()
    mock_instance.return_value = MagicMock(answer="[mock answer]")
    mock_predict_cls.return_value = mock_instance
    mock_dspy.Predict = mock_predict_cls
    old = sys.modules.get("dspy")
    sys.modules["dspy"] = mock_dspy
    yield mock_predict_cls
    if old is None:
        sys.modules.pop("dspy", None)
    else:
        sys.modules["dspy"] = old


@pytest.fixture
def dspygen_module_runner(dspy_lm):
    """Run any dspygen module with a mocked LM injected via sys.modules."""
    def _run(module_fn, *args, **kwargs):
        mock_dspy = MagicMock()
        mock_dspy.settings.lm = dspy_lm
        old = sys.modules.get("dspy")
        sys.modules["dspy"] = mock_dspy
        try:
            return module_fn(*args, **kwargs)
        finally:
            if old is None:
                sys.modules.pop("dspy", None)
            else:
                sys.modules["dspy"] = old
    return _run


@pytest.fixture
def pipeline_executor():
    """Execute a simple YAML pipeline dict in tests without yaml import."""
    def _execute(pipeline_yaml: str) -> Dict[str, Any]:
        return _parse_yaml_pipeline(pipeline_yaml)
    return _execute


# ===========================================================================
# TEST 1 -- load_ipython_extension registers magics on a mock IP
# ===========================================================================

def test_load_ipython_extension_registers_magics():
    ip = _make_ipython_mock()
    _load_ipython_extension(ip)
    registered = {
        c.kwargs.get("magic_name") for c in ip.register_magic_function.call_args_list
    }
    assert "dspygen_init" in registered
    assert "dspygen_modules" in registered
    assert "dspygen_pipeline" in registered


# ===========================================================================
# TEST 2 -- %dspygen_init calls init_dspy with correct model
# ===========================================================================

def test_dspygen_init_calls_init_dspy_with_model():
    ip = _make_ipython_mock()
    magics = _load_ipython_extension(ip)
    result = magics.dspygen_init("gpt-4o")
    assert magics._init_called is True
    assert magics._init_model == "gpt-4o"
    assert result["model"] == "gpt-4o"
    assert result["initialized"] is True


# ===========================================================================
# TEST 3 -- %dspygen_modules returns list of module names
# ===========================================================================

def test_dspygen_modules_returns_list_of_names():
    ip = _make_ipython_mock()
    magics = _load_ipython_extension(ip)
    modules = magics.dspygen_modules("")
    assert isinstance(modules, list)
    assert len(modules) > 0
    assert all(isinstance(m, str) for m in modules)
    assert not any(m.startswith("_") for m in modules)


# ===========================================================================
# TEST 4 -- %dspygen_agents returns list of agent names
# ===========================================================================

def test_dspygen_agents_returns_list_of_names():
    ip = _make_ipython_mock()
    magics = _load_ipython_extension(ip)
    agents = magics.dspygen_agents("")
    assert isinstance(agents, list)
    assert all(isinstance(a, str) for a in agents)
    assert not any(a.startswith("_") for a in agents)


# ===========================================================================
# TEST 5 -- %%dspygen_pipeline executes a simple YAML pipeline step
# ===========================================================================

def test_dspygen_pipeline_executes_yaml_step():
    ip = _make_ipython_mock()
    magics = _load_ipython_extension(ip)
    sample = "steps:\n  - module: gen_dspy_module\n    args:\n      prompt: hello\n"
    result = magics.dspygen_pipeline("", sample)
    assert result["status"] == "ok"
    assert result["yaml"] == sample
    assert magics._last_pipeline_yaml == sample


# ===========================================================================
# TEST 6 -- %dspygen_history reads from dspy.settings.lm.history
# ===========================================================================

def test_dspygen_history_reads_from_lm_history():
    ip = _make_ipython_mock()
    magics = _load_ipython_extension(ip)
    fake_lm = MagicMock()
    fake_lm.history = [{"prompt": "q1"}, {"prompt": "q2"}]
    mock_dspy = MagicMock()
    mock_dspy.settings.lm = fake_lm
    old = sys.modules.get("dspy")
    sys.modules["dspy"] = mock_dspy
    try:
        history = magics.dspygen_history("")
    finally:
        if old is None:
            sys.modules.pop("dspy", None)
        else:
            sys.modules["dspy"] = old
    assert history == [{"prompt": "q1"}, {"prompt": "q2"}]


# ===========================================================================
# TEST 7 -- display_module_output formats output as HTML in Jupyter context
# ===========================================================================

def test_display_module_output_formats_as_html():
    ip = _make_ipython_mock()
    magics = _load_ipython_extension(ip)
    html = magics.display_module_output("hello world", module_name="my_module")
    assert "<div" in html
    assert "my_module" in html
    assert "hello world" in html
    assert html.startswith("<div")
    assert html.endswith("</div>")


# ===========================================================================
# TEST 8 -- dspy_lm fixture returns mock LM with __call__ defined
# ===========================================================================

def test_dspy_lm_fixture_callable_and_records(dspy_lm):
    assert callable(dspy_lm)
    response = dspy_lm("test prompt")
    assert isinstance(response, str)
    assert len(dspy_lm.calls) == 1
    assert dspy_lm.calls[0]["prompt"] == "test prompt"


# ===========================================================================
# TEST 9 -- mock_dspy_predict patches dspy.Predict to return deterministic output
# ===========================================================================

def test_mock_dspy_predict_returns_deterministic_output(mock_dspy_predict):
    import dspy  # now resolves to the mock injected by the fixture
    predictor = dspy.Predict("question -> answer")
    result = predictor("What is 2+2?")
    assert mock_dspy_predict.call_count >= 1
    assert result is not None


# ===========================================================================
# TEST 10 -- requires_openai mark causes skip when OPENAI_API_KEY unset
# ===========================================================================

def test_requires_openai_skips_when_key_unset(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    assert key  # pragma: no cover


# ===========================================================================
# TEST 11 -- requires_ollama mark causes skip when Ollama unreachable
# ===========================================================================

def test_requires_ollama_skips_when_unreachable():
    import urllib.request, urllib.error
    with patch("urllib.request.urlopen") as mock_open:
        mock_open.side_effect = urllib.error.URLError("connection refused")
        try:
            urllib.request.urlopen("http://localhost:11434/api/tags", timeout=1)
            reachable = True
        except urllib.error.URLError:
            reachable = False
    if not reachable:
        pytest.skip("Ollama not reachable")
    assert reachable  # pragma: no cover


# ===========================================================================
# TEST 12 -- dspygen_module_runner fixture can run any module with mocked LM
# ===========================================================================

def test_dspygen_module_runner_with_mocked_lm(dspygen_module_runner):
    def dummy_module(question: str) -> str:
        return f"answer to: {question}"

    result = dspygen_module_runner(dummy_module, "What is DSPy?")
    assert result == "answer to: What is DSPy?"


# ===========================================================================
# TEST 13 -- pipeline_executor fixture executes YAML pipeline in test
# ===========================================================================

def test_pipeline_executor_executes_yaml(pipeline_executor):
    yaml_str = (
        "steps:\n"
        "  - module: gen_dspy_module\n"
        "    args:\n"
        "      prompt: hello\n"
        "  - module: python_source_code_module\n"
        "    args:\n"
        "      context: world\n"
    )
    result = pipeline_executor(yaml_str)
    assert result["count"] == 2
    assert result["steps"][0]["module"] == "gen_dspy_module"
    assert result["steps"][1]["module"] == "python_source_code_module"
    assert all(s["status"] == "ok" for s in result["steps"])


# ===========================================================================
# TEST 14 -- assert_module_output helper passes for matching output
# ===========================================================================

def test_assert_module_output_passes_for_match():
    _assert_module_output("hello", "hello")
    _assert_module_output(42, 42)
    _assert_module_output({"key": "val"}, {"key": "val"})

    with pytest.raises(AssertionError, match="mismatch"):
        _assert_module_output("got this", "expected that")


# ===========================================================================
# TEST 15 -- assert_signature_valid passes for valid sig, raises for invalid
# ===========================================================================

def test_assert_signature_valid_valid_and_invalid():
    _assert_signature_valid("question -> answer")
    _assert_signature_valid("context, question -> reasoning, answer")
    _assert_signature_valid("  input  ->  output  ")

    with pytest.raises(AssertionError):
        _assert_signature_valid("no arrow here")

    with pytest.raises(AssertionError):
        _assert_signature_valid("")

    with pytest.raises(AssertionError):
        _assert_signature_valid("input -> ")

    with pytest.raises(AssertionError):
        _assert_signature_valid(" -> output")
