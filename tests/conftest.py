"""
pytest conftest.py — project-wide fixtures and import stubs.

This file is automatically loaded by pytest before any test module.

Key responsibilities:
1. Add src/ to sys.path so `import dspygen` works without installing.
2. Provide mock stubs for heavyweight optional dependencies (dslmodel, etc.)
   so that tests can run in environments where these are not installed.
3. Register custom pytest marks to silence PytestUnknownMarkWarning.
"""

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# 1. Ensure src/ is on sys.path
# ---------------------------------------------------------------------------

_SRC = Path(__file__).parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


# ---------------------------------------------------------------------------
# 2a. Patch dspy for removed/missing attributes before any test imports it
# ---------------------------------------------------------------------------

try:
    import dspy as _dspy
    # Newer dspy versions removed these; add stubs so legacy code doesn't crash at import time
    for _attr in ["OpenAI", "OllamaLocal", "Cohere", "TGI", "VLLM"]:
        if not hasattr(_dspy, _attr):
            setattr(_dspy, _attr, MagicMock())
except ImportError:
    pass


# ---------------------------------------------------------------------------
# 2b. Stub unavailable heavy dependencies
# ---------------------------------------------------------------------------

def _make_dslmodel_stub():
    """Create a minimal dslmodel stub that satisfies dspygen's imports."""
    try:
        from pydantic import BaseModel
    except ImportError:
        BaseModel = object

    class DSLModel(BaseModel if BaseModel is not object else object):
        """Minimal DSLModel stub for test environments."""

        class Config:
            arbitrary_types_allowed = True
            populate_by_name = True

    stub = types.ModuleType("dslmodel")
    stub.DSLModel = DSLModel
    return stub


# Register dslmodel stub early so any subsequent imports of dspygen.rdddy.* work
if "dslmodel" not in sys.modules:
    try:
        import dslmodel  # noqa: F401
    except ModuleNotFoundError:
        _stub = _make_dslmodel_stub()
        sys.modules["dslmodel"] = _stub

# Stub modules that are truly platform-specific (macOS only) and absent in CI
_MACOS_ONLY_DEPS = [
    "osascript",
    "pyobjc",
    "pyobjc_framework_eventkit",
    "EventKit",
    "Foundation",
    "AppKit",
    "Contacts",
    "EventKit",
]

for _mod_name in _MACOS_ONLY_DEPS:
    if _mod_name not in sys.modules:
        _mock = MagicMock()
        _mock.__name__ = _mod_name
        _mock.__package__ = _mod_name.split(".")[0]
        _mock.__path__ = []
        _mock.__spec__ = None
        sys.modules[_mod_name] = _mock


# ---------------------------------------------------------------------------
# 3. Register custom pytest marks
# ---------------------------------------------------------------------------

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow-running")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "requires_llm: mark test as requiring a real LLM")
    config.addinivalue_line(
        "markers",
        "dspygen_requires_openai: skip test if OPENAI_API_KEY is not set",
    )
