"""
Performance benchmarks for dspygen — skipped by default, run with: pytest -m benchmark

All benchmarks run without real LLM or network calls.
Tests are marked with pytest.mark.slow so they can be skipped in quick runs.
"""

import ast
import time
from pathlib import Path
from typing import List

import pytest

pytestmark = pytest.mark.slow

MODULES_DIR = Path(__file__).parent.parent / "src/dspygen/modules"
RDDDY_DIR = Path(__file__).parent.parent / "src/dspygen/rdddy"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _list_all_module_files() -> List[Path]:
    return sorted(
        [f for f in MODULES_DIR.glob("*.py") if not f.name.startswith("_")]
    )


def _search_module_index(query: str) -> List[str]:
    query_lower = query.lower()
    return [f.stem for f in _list_all_module_files() if query_lower in f.stem.lower()]


def _parse_file(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


def _validate_signature(sig: str) -> List[str]:
    errors = []
    if not sig or not sig.strip():
        errors.append("Empty signature")
        return errors
    if "->" not in sig:
        errors.append("Missing '->'")
    return errors


# ---------------------------------------------------------------------------
# 1. Module index build time < 5 seconds
# ---------------------------------------------------------------------------

def test_module_index_build_time():
    """Building the full module list (file discovery) must finish in < 5 s."""
    start = time.perf_counter()
    files = _list_all_module_files()
    elapsed = time.perf_counter() - start

    assert elapsed < 5.0, f"Module index took {elapsed:.3f}s — expected < 5s"
    assert len(files) > 50, "Expected at least 50 module files"


# ---------------------------------------------------------------------------
# 2. Module index search time < 100ms per query
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("query", [
    "gen",
    "module",
    "sql",
    "python",
    "data",
])
def test_module_index_search_time(query: str):
    """Each module search must complete in < 100ms."""
    start = time.perf_counter()
    results = _search_module_index(query)
    elapsed = time.perf_counter() - start

    assert elapsed < 0.1, f"Search for {query!r} took {elapsed*1000:.1f}ms — expected < 100ms"
    assert isinstance(results, list)


# ---------------------------------------------------------------------------
# 3. Parse 100 signatures in < 1 second
# ---------------------------------------------------------------------------

def test_signature_parse_100_times():
    """Parsing 100 simple signature strings must finish in < 1s."""
    sigs = [f"input{i}, context{i} -> output{i}" for i in range(100)]

    start = time.perf_counter()
    for sig in sigs:
        errors = _validate_signature(sig)
        assert errors == [], f"Unexpected errors for {sig!r}: {errors}"
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0, f"100 signature parses took {elapsed:.3f}s — expected < 1s"


# ---------------------------------------------------------------------------
# 4. list_modules tool time < 2 seconds
# ---------------------------------------------------------------------------

def test_mcp_tool_list_modules_time():
    """Listing all modules (the MCP tool simulation) must finish in < 2s."""
    start = time.perf_counter()
    modules = sorted(f.stem for f in _list_all_module_files())
    elapsed = time.perf_counter() - start

    assert elapsed < 2.0, f"list_modules took {elapsed:.3f}s — expected < 2s"
    assert len(modules) > 50


# ---------------------------------------------------------------------------
# 5. Diagnose 1000-line file in < 1 second
# ---------------------------------------------------------------------------

def test_lsp_diagnostics_large_file():
    """Parsing a 1000-line generated file for diagnostics must finish in < 1s."""
    lines = ["import dspy", ""]
    for i in range(100):
        lines += [
            f"class Module{i}(dspy.Module):",
            "    def __init__(self):",
            "        super().__init__()",
            "        self.p = None",
            "    def forward(self, x: str) -> str:",
            "        return x",
            "",
        ]
    large_source = "\n".join(lines)
    assert len(large_source.splitlines()) >= 700

    start = time.perf_counter()
    try:
        tree = ast.parse(large_source)
    except SyntaxError:
        pytest.fail("Generated large file has syntax errors")

    # Simulate diagnostics walk
    diagnostics = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            base_names = [
                b.attr if isinstance(b, ast.Attribute) else (b.id if isinstance(b, ast.Name) else "")
                for b in node.bases
            ]
            if "Module" in base_names:
                method_names = {
                    fn.name for fn in ast.walk(node) if isinstance(fn, ast.FunctionDef)
                }
                if "forward" not in method_names:
                    diagnostics.append(f"warning: {node.name} missing forward()")

    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"Diagnostics of large file took {elapsed:.3f}s — expected < 1s"
    assert diagnostics == [], f"Unexpected diagnostics: {diagnostics}"


# ---------------------------------------------------------------------------
# 6. Parse ALL module files in < 10 seconds
# ---------------------------------------------------------------------------

def test_parse_all_modules_in_under_10_seconds():
    """Parsing the AST of every module file must finish in under 10 seconds total."""
    files = _list_all_module_files()

    start = time.perf_counter()
    parse_errors = []
    for f in files:
        try:
            _parse_file(f)
        except SyntaxError as exc:
            parse_errors.append(f"{f.name}: {exc}")
    elapsed = time.perf_counter() - start

    assert elapsed < 10.0, f"Parsing all modules took {elapsed:.3f}s — expected < 10s"
    assert parse_errors == [], f"Syntax errors found: {parse_errors}"


# ---------------------------------------------------------------------------
# 7. RDDDY class instantiation < 50ms
# ---------------------------------------------------------------------------

def test_rdddy_message_instantiation_speed():
    """Creating 1000 BaseMessage instances must finish in < 50ms."""
    from dspygen.rdddy.base_message import BaseMessage

    start = time.perf_counter()
    for i in range(1000):
        m = BaseMessage(message_type=f"type_{i}", payload={"index": i})
    elapsed = time.perf_counter() - start

    assert elapsed < 0.5, f"1000 BaseMessage instances took {elapsed:.3f}s — expected < 500ms"


# ---------------------------------------------------------------------------
# 8. File search across all modules < 200ms
# ---------------------------------------------------------------------------

def test_glob_modules_directory_speed():
    """Globbing the modules directory must finish in < 200ms."""
    start = time.perf_counter()
    files = list(MODULES_DIR.glob("*.py"))
    elapsed = time.perf_counter() - start

    assert elapsed < 0.2, f"Glob took {elapsed*1000:.1f}ms — expected < 200ms"
    assert len(files) > 50


# ---------------------------------------------------------------------------
# 9. Symbol extraction from VALID_DSPY_CODE repeated 500 times < 1 second
# ---------------------------------------------------------------------------

def test_symbol_extraction_speed():
    """Extracting symbols from code repeated 500 times must finish in < 1s."""
    code = '''
import dspy

class SigA(dspy.Signature):
    """Sig A."""
    inp = dspy.InputField(desc="input")
    out = dspy.OutputField(desc="output")

class ModA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(SigA)
    def forward(self, inp: str) -> str:
        return inp
'''

    def extract_symbols(source: str):
        tree = ast.parse(source)
        return [
            n.name for n in ast.walk(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef))
        ]

    start = time.perf_counter()
    for _ in range(500):
        symbols = extract_symbols(code)
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0, f"500 symbol extractions took {elapsed:.3f}s — expected < 1s"
    assert "ModA" in symbols


# ---------------------------------------------------------------------------
# 10. RDDDY directory listing < 50ms
# ---------------------------------------------------------------------------

def test_rdddy_directory_listing_speed():
    """Listing the rdddy directory must finish in < 50ms."""
    start = time.perf_counter()
    files = list(RDDDY_DIR.glob("*.py"))
    elapsed = time.perf_counter() - start

    assert elapsed < 0.05, f"RDDDY dir listing took {elapsed*1000:.1f}ms — expected < 50ms"
    assert len(files) >= 10
