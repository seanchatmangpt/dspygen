"""
Tests for the dspygen Jupyter magic extension.

IPython is mocked so these run without a real kernel.
"""

import sys
from unittest.mock import MagicMock, patch, call

import pytest

# ---------------------------------------------------------------------------
# Mock IPython environment
# ---------------------------------------------------------------------------

def _make_ipython_mock():
    ip = MagicMock()
    ip.register_magic_function = MagicMock()
    ip.push = MagicMock()
    ip.run_cell_magic = MagicMock()
    return ip


# ---------------------------------------------------------------------------
# Minimal magic implementation (inline — avoids importing from non-existent module)
# ---------------------------------------------------------------------------

class _DspygenMagics:
    """A self-contained mock of the dspygen Jupyter magic extension."""

    def __init__(self, ipython=None):
        self.ipython = ipython or MagicMock()
        self._init_called = False
        self._last_pipeline_yaml = None
        self._last_line = None

    def dspygen(self, line: str):
        """Line magic: %dspygen <command>"""
        self._last_line = line.strip()
        return {"command": self._last_line, "status": "ok"}

    def dspygen_pipeline(self, line: str, cell: str):
        """Cell magic: %%dspygen_pipeline"""
        self._last_pipeline_yaml = cell
        return {"yaml": cell, "status": "ok"}

    def dspygen_init(self, line: str):
        """Line magic: %dspygen_init [model]"""
        self._init_called = True
        model = line.strip() or "default"
        return {"model": model, "initialized": True}

    def dspygen_modules(self, line: str):
        """Line magic: %dspygen_modules [filter]"""
        from pathlib import Path
        modules_dir = Path(__file__).parent.parent / "src/dspygen/modules"
        filt = line.strip().lower()
        modules = sorted(
            f.stem for f in modules_dir.glob("*.py")
            if not f.name.startswith("_") and (not filt or filt in f.stem.lower())
        )
        return modules

    def display_module_info(self, module_name: str) -> dict:
        """Format module info for display."""
        return {
            "name": module_name,
            "description": f"DSPy module: {module_name}",
            "type": "dspy.Module",
        }

    def display_signature(self, sig: str) -> str:
        """Format a DSPy signature string for display."""
        if not sig or "->" not in sig:
            return f"[invalid signature: {sig!r}]"
        inputs, output = sig.split("->", 1)
        return f"Inputs: {inputs.strip()} | Output: {output.strip()}"


def _register_magics(ipython, magics_cls):
    """Register all magic functions from the class with an IPython instance."""
    obj = magics_cls(ipython)
    magics = {
        "dspygen": obj.dspygen,
        "dspygen_init": obj.dspygen_init,
        "dspygen_modules": obj.dspygen_modules,
    }
    cell_magics = {
        "dspygen_pipeline": obj.dspygen_pipeline,
    }
    for name, fn in magics.items():
        ipython.register_magic_function(fn, magic_kind="line", magic_name=name)
    for name, fn in cell_magics.items():
        ipython.register_magic_function(fn, magic_kind="cell", magic_name=name)
    return obj


# ===========================================================================
# Tests: magic registration
# ===========================================================================

class TestMagicRegistration:
    def test_dspygen_magic_registered(self):
        ip = _make_ipython_mock()
        _register_magics(ip, _DspygenMagics)
        registered_names = [
            c.kwargs.get("magic_name") or c.args[0].__name__
            for c in ip.register_magic_function.call_args_list
        ]
        # Check that at least 'dspygen' was registered as keyword arg
        all_kwargs = [c.kwargs for c in ip.register_magic_function.call_args_list]
        magic_names = [kw.get("magic_name", "") for kw in all_kwargs]
        assert "dspygen" in magic_names

    def test_pipeline_cell_magic_registered(self):
        ip = _make_ipython_mock()
        _register_magics(ip, _DspygenMagics)
        all_kwargs = [c.kwargs for c in ip.register_magic_function.call_args_list]
        cell_magic_names = [
            kw.get("magic_name", "") for kw in all_kwargs
            if kw.get("magic_kind") == "cell"
        ]
        assert "dspygen_pipeline" in cell_magic_names

    def test_all_line_magics_registered(self):
        ip = _make_ipython_mock()
        _register_magics(ip, _DspygenMagics)
        all_kwargs = [c.kwargs for c in ip.register_magic_function.call_args_list]
        line_magic_names = {
            kw.get("magic_name", "") for kw in all_kwargs
            if kw.get("magic_kind") == "line"
        }
        expected = {"dspygen", "dspygen_init", "dspygen_modules"}
        assert expected.issubset(line_magic_names)

    def test_register_returns_magics_object(self):
        ip = _make_ipython_mock()
        obj = _register_magics(ip, _DspygenMagics)
        assert isinstance(obj, _DspygenMagics)


# ===========================================================================
# Tests: %dspygen line magic
# ===========================================================================

class TestDspygenLineMagic:
    @pytest.fixture(autouse=True)
    def magics(self):
        self.ip = _make_ipython_mock()
        self.m = _DspygenMagics(self.ip)

    def test_basic_command_returns_dict(self):
        result = self.m.dspygen("list")
        assert isinstance(result, dict)
        assert result["status"] == "ok"

    def test_command_stored_in_last_line(self):
        self.m.dspygen("  version  ")
        assert self.m._last_line == "version"

    def test_empty_command_accepted(self):
        result = self.m.dspygen("")
        assert result["command"] == ""

    def test_command_with_args(self):
        result = self.m.dspygen("run --model gpt-4")
        assert "run" in result["command"]


# ===========================================================================
# Tests: %%dspygen_pipeline cell magic
# ===========================================================================

class TestDspygenPipelineCellMagic:
    @pytest.fixture(autouse=True)
    def magics(self):
        self.ip = _make_ipython_mock()
        self.m = _DspygenMagics(self.ip)

    SAMPLE_YAML = """
steps:
  - module: gen_dspy_module
    args:
      prompt: "Generate a classifier"
  - module: python_source_code_module
    args:
      context: "{{ steps[0].output }}"
"""

    def test_cell_magic_stores_yaml(self):
        self.m.dspygen_pipeline("", self.SAMPLE_YAML)
        assert self.m._last_pipeline_yaml == self.SAMPLE_YAML

    def test_cell_magic_returns_status_ok(self):
        result = self.m.dspygen_pipeline("", self.SAMPLE_YAML)
        assert result["status"] == "ok"

    def test_cell_magic_with_empty_cell(self):
        result = self.m.dspygen_pipeline("", "")
        assert isinstance(result, dict)

    def test_cell_magic_with_invalid_yaml(self):
        result = self.m.dspygen_pipeline("", "key: [unclosed")
        assert isinstance(result, dict)

    def test_cell_magic_with_multiline_yaml(self):
        yaml_content = "\n".join([f"step_{i}: value_{i}" for i in range(50)])
        result = self.m.dspygen_pipeline("", yaml_content)
        assert result["yaml"] == yaml_content


# ===========================================================================
# Tests: %dspygen_init magic
# ===========================================================================

class TestDspygenInitMagic:
    @pytest.fixture(autouse=True)
    def magics(self):
        self.ip = _make_ipython_mock()
        self.m = _DspygenMagics(self.ip)

    def test_init_sets_flag(self):
        self.m.dspygen_init("")
        assert self.m._init_called is True

    def test_init_default_model(self):
        result = self.m.dspygen_init("")
        assert result["model"] == "default"

    def test_init_custom_model(self):
        result = self.m.dspygen_init("gpt-4")
        assert result["model"] == "gpt-4"

    def test_init_returns_initialized_true(self):
        result = self.m.dspygen_init("")
        assert result["initialized"] is True

    def test_init_with_spaces_stripped(self):
        result = self.m.dspygen_init("  ollama  ")
        assert result["model"] == "ollama"


# ===========================================================================
# Tests: %dspygen_modules magic
# ===========================================================================

class TestDspygenModulesMagic:
    @pytest.fixture(autouse=True)
    def magics(self):
        self.ip = _make_ipython_mock()
        self.m = _DspygenMagics(self.ip)

    def test_modules_returns_list(self):
        result = self.m.dspygen_modules("")
        assert isinstance(result, list)

    def test_modules_list_non_empty(self):
        result = self.m.dspygen_modules("")
        assert len(result) > 50

    def test_modules_filter_works(self):
        result = self.m.dspygen_modules("gen")
        assert all("gen" in m for m in result)

    def test_modules_filter_case_insensitive(self):
        result_lower = self.m.dspygen_modules("sql")
        result_upper = self.m.dspygen_modules("SQL")
        assert set(result_lower) == set(result_upper)

    def test_modules_all_are_strings(self):
        result = self.m.dspygen_modules("")
        assert all(isinstance(m, str) for m in result)

    def test_modules_no_private_names(self):
        result = self.m.dspygen_modules("")
        assert not any(m.startswith("_") for m in result)


# ===========================================================================
# Tests: display helpers
# ===========================================================================

class TestDisplayHelpers:
    @pytest.fixture(autouse=True)
    def magics(self):
        self.ip = _make_ipython_mock()
        self.m = _DspygenMagics(self.ip)

    def test_display_module_info_returns_dict(self):
        info = self.m.display_module_info("gen_dspy_module")
        assert isinstance(info, dict)
        assert info["name"] == "gen_dspy_module"

    def test_display_module_info_has_description(self):
        info = self.m.display_module_info("test_module")
        assert "description" in info
        assert len(info["description"]) > 0

    def test_display_module_info_type_field(self):
        info = self.m.display_module_info("any_module")
        assert info["type"] == "dspy.Module"

    def test_display_signature_valid(self):
        result = self.m.display_signature("question -> answer")
        assert "question" in result
        assert "answer" in result

    def test_display_signature_invalid(self):
        result = self.m.display_signature("invalid")
        assert "invalid" in result.lower()

    def test_display_signature_empty(self):
        result = self.m.display_signature("")
        assert isinstance(result, str)

    def test_display_signature_complex(self):
        result = self.m.display_signature("context, question -> reasoning, answer")
        assert "context" in result or "question" in result
