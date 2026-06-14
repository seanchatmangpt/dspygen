"""Reusable pytest fixtures for dspygen testing.

Import these fixtures directly in your test files or add
``from dspygen.testing.fixtures import *`` to ``tests/conftest.py`` to make
them auto-available project-wide.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any, Callable

import pytest

from dspygen.testing.factories import MockLM, MockPredict, mock_lm_context


@pytest.fixture()
def dspy_lm():
    """Configure dspy with a MockLM for the duration of the test, then restore.

    Yields the MockLM instance so tests can inspect ``lm.history``.

    Example::

        def test_prediction(dspy_lm):
            pred = dspy.Predict("question -> answer")
            pred(question="What is AI?")
            assert dspy_lm.history  # call was recorded
    """
    try:
        import dspy
    except ImportError:
        pytest.skip("dspy is not installed")

    lm = MockLM()
    original = getattr(dspy.settings, "lm", None)
    try:
        dspy.settings.configure(lm=lm)
    except Exception:
        pass

    yield lm

    try:
        if original is not None:
            dspy.settings.configure(lm=original)
    except Exception:
        pass


@pytest.fixture()
def mock_predict(monkeypatch):
    """Patch dspy.Predict globally for the test duration.

    Resets MockPredict.calls before yielding so tests don't see stale data.

    Yields the MockPredict class so tests can inspect ``MockPredict.calls``.

    Example::

        def test_predict(mock_predict):
            import dspy
            pred = dspy.Predict("question -> answer")
            pred(question="hello")
            assert mock_predict.calls[-1] == {"question": "hello"}
    """
    MockPredict.reset()
    try:
        monkeypatch.setattr("dspy.Predict", MockPredict)
    except (AttributeError, ImportError):
        pytest.skip("dspy is not installed or dspy.Predict not patchable")

    yield MockPredict

    MockPredict.reset()


@pytest.fixture()
def pipeline_executor():
    """Return a function that runs a pipeline defined as a YAML string.

    The returned callable accepts a YAML string and returns the context dict.

    Example::

        def test_pipeline(pipeline_executor):
            ctx = pipeline_executor('''
            steps:
              - module: echo_module
                args: {text: "hello"}
            ''')
            assert ctx["status"] == "completed"
    """
    from dspygen.testing.helpers import assert_pipeline_executes

    def _run(yaml_str: str) -> dict:
        return assert_pipeline_executes(yaml_str)

    return _run


@pytest.fixture()
def module_runner():
    """Return a function that runs any dspygen module with a mock LM.

    Usage::

        def test_my_module(module_runner):
            runner = module_runner(MyDSPyModule)
            result = runner(question="What is AI?")
    """
    from dspygen.testing.factories import make_module_runner

    def _make(module_class: type, responses: dict | None = None) -> Callable:
        return make_module_runner(module_class, responses=responses)

    return _make


@pytest.fixture()
def tmp_dspygen_config(tmp_path: Path):
    """Provide a temporary directory containing a minimal ``.dspygen.env`` file.

    Yields the ``tmp_path`` directory (a :class:`pathlib.Path`).  The env file
    contains safe placeholder values suitable for offline / CI testing.

    Example::

        def test_config_loading(tmp_dspygen_config):
            env_file = tmp_dspygen_config / ".dspygen.env"
            assert env_file.exists()
    """
    env_file = tmp_path / ".dspygen.env"
    env_file.write_text(
        "OPENAI_API_KEY=mock_key_for_testing\n"
        "DSPYGEN_ENV=test\n"
        "DSPYGEN_LM=mock\n"
    )
    yield tmp_path
