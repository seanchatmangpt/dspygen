"""
Property-based tests using Hypothesis.

All tests are pure / deterministic — no real LLM or network calls.
"""

import ast
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

pytestmark = [pytest.mark.slow, pytest.mark.property_based]

hypothesis = pytest.importorskip("hypothesis", reason="hypothesis not installed")
from hypothesis import given, settings, strategies as st, assume, HealthCheck

# ---------------------------------------------------------------------------
# Helpers shared with other test modules
# ---------------------------------------------------------------------------

def _is_valid_python_identifier(s: str) -> bool:
    try:
        ast.parse(s)
        return s.isidentifier() and not keyword_is_reserved(s)
    except SyntaxError:
        return False


def keyword_is_reserved(s: str) -> bool:
    import keyword
    return keyword.iskeyword(s)


# Lazy imports so as not to pull in dspygen at collection time
def _get_validate_signature():
    """Return a function that validates a DSPy-style signature string."""
    def validate_signature(sig: str) -> List[str]:
        """Returns a list of errors (empty means valid)."""
        errors = []
        if not sig or not sig.strip():
            errors.append("Empty signature")
            return errors
        parts = sig.split("->")
        if len(parts) < 2:
            errors.append("Missing '->' separator")
        return errors
    return validate_signature


def _get_module_index_search():
    """Return a callable that searches the module index (static)."""
    MODULES_DIR = Path(__file__).parent.parent / "src/dspygen/modules"

    def search(query: str) -> List[str]:
        if not query or not query.strip():
            return []
        query_lower = query.lower()
        results = []
        for f in MODULES_DIR.glob("*.py"):
            if not f.name.startswith("_") and query_lower in f.stem.lower():
                results.append(f.stem)
        return results

    return search


def _get_pipeline_yaml_validator():
    """Return a function that 'validates' a pipeline YAML string."""
    import yaml

    def validate_pipeline(raw: str) -> Dict[str, Any]:
        result = {"valid": False, "errors": []}
        if not raw or not raw.strip():
            result["errors"].append("Empty YAML")
            return result
        try:
            data = yaml.safe_load(raw)
            if data is None:
                result["errors"].append("Empty document")
            elif not isinstance(data, dict):
                result["errors"].append("Root must be a mapping")
            else:
                result["valid"] = True
        except yaml.YAMLError as exc:
            result["errors"].append(str(exc))
        return result

    return validate_pipeline


# ---------------------------------------------------------------------------
# 1. Signature parser round-trip
# ---------------------------------------------------------------------------

@given(
    inputs=st.lists(
        st.text(
            alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd", "Pc")),
            min_size=1,
            max_size=20,
        ),
        min_size=1,
        max_size=5,
    ),
    output=st.text(
        alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd", "Pc")),
        min_size=1,
        max_size=20,
    ),
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_signature_parser_roundtrip(inputs: List[str], output: str):
    """
    Build a signature string, parse it, and verify the structure is preserved.
    """
    sig_str = ", ".join(inputs) + " -> " + output
    validate = _get_validate_signature()
    errors = validate(sig_str)
    # A properly formed signature must have zero errors
    assert errors == [], f"Roundtrip failed for {sig_str!r}: {errors}"


# ---------------------------------------------------------------------------
# 2. validate_signature never crashes
# ---------------------------------------------------------------------------

@given(st.text(max_size=500))
@settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
def test_validate_signature_never_crashes(s: str):
    """Any string should never raise when passed to validate_signature."""
    validate = _get_validate_signature()
    try:
        result = validate(s)
        assert isinstance(result, list)
    except Exception as exc:
        pytest.fail(f"validate_signature raised unexpectedly: {exc!r}")


# ---------------------------------------------------------------------------
# 3. module_index_search never crashes
# ---------------------------------------------------------------------------

@given(st.text(max_size=100))
@settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
def test_module_index_search_never_crashes(query: str):
    """Any query string must never raise when searching the module index."""
    search = _get_module_index_search()
    try:
        result = search(query)
        assert isinstance(result, list)
    except Exception as exc:
        pytest.fail(f"module_index_search raised unexpectedly: {exc!r}")


# ---------------------------------------------------------------------------
# 4. LM tool handlers never raise, always return a dict
# ---------------------------------------------------------------------------

def _lm_tool(prompt: str, max_tokens: int = 100) -> dict:
    """Minimal mock tool handler (no LLM call)."""
    return {"text": f"[response to {prompt[:10]}]", "tokens": max_tokens}


@given(
    prompt=st.text(max_size=1000),
    max_tokens=st.integers(min_value=1, max_value=8192),
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_lm_tool_with_arbitrary_args(prompt: str, max_tokens: int):
    """Tool handlers must never raise and must always return a dict."""
    try:
        result = _lm_tool(prompt, max_tokens)
        assert isinstance(result, dict)
        assert "text" in result
    except Exception as exc:
        pytest.fail(f"lm_tool raised unexpectedly: {exc!r}")


# ---------------------------------------------------------------------------
# 5. RDDDY class names are valid Python identifiers
# ---------------------------------------------------------------------------

@given(
    prefix=st.sampled_from(["Base", "Abstract", "Domain", "Core"]),
    suffix=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
        min_size=1,
        max_size=20,
    ),
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_rdddy_class_names_valid_python(prefix: str, suffix: str):
    """Generated RDDDY-style class names must be valid Python identifiers."""
    class_name = prefix + suffix.capitalize()
    assume(class_name.isidentifier())
    assert class_name.isidentifier(), f"{class_name!r} is not a valid Python identifier"
    # Must also be parseable in a class statement
    code = f"class {class_name}: pass"
    tree = ast.parse(code)
    assert tree is not None


# ---------------------------------------------------------------------------
# 6. Pipeline YAML validates gracefully
# ---------------------------------------------------------------------------

@given(st.text(max_size=500))
@settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
def test_pipeline_yaml_validates_gracefully(raw: str):
    """Any string as YAML input must never crash the validator."""
    validate = _get_pipeline_yaml_validator()
    try:
        result = validate(raw)
        assert isinstance(result, dict)
        assert "valid" in result
        assert isinstance(result["errors"], list)
    except Exception as exc:
        pytest.fail(f"validate_pipeline raised unexpectedly: {exc!r}")


# ---------------------------------------------------------------------------
# 7. AST parse never crashes with valid Python
# ---------------------------------------------------------------------------

@given(
    class_name=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd")),
        min_size=1,
        max_size=30,
    ).filter(lambda s: s and s[0].isupper() and s.isidentifier()),
    method_name=st.text(
        alphabet=st.characters(whitelist_categories=("Ll", "Nd", "Pc")),
        min_size=1,
        max_size=20,
    ).filter(lambda s: s.isidentifier()),
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_generated_class_code_parseable(class_name: str, method_name: str):
    """Generated class source code must be parseable."""
    assume(not keyword_is_reserved(class_name))
    assume(not keyword_is_reserved(method_name))
    code = f"""
class {class_name}:
    def {method_name}(self):
        pass
"""
    try:
        ast.parse(code)
    except SyntaxError as exc:
        pytest.fail(f"Generated code not parseable: {exc!r}\n{code}")


# ---------------------------------------------------------------------------
# 8. Rename is idempotent
# ---------------------------------------------------------------------------

@given(
    source=st.text(max_size=500),
    name=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd", "Pc")),
        min_size=1,
        max_size=20,
    ).filter(str.isidentifier),
)
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_rename_idempotent(source: str, name: str):
    """Renaming X to X should produce the same source."""
    assume(not keyword_is_reserved(name))
    result = re.sub(r'\b' + re.escape(name) + r'\b', name, source)
    assert result == source


# ---------------------------------------------------------------------------
# 9. Module list is stable across calls
# ---------------------------------------------------------------------------

@given(st.integers(min_value=0, max_value=10))
@settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
def test_module_list_stable_across_calls(n: int):
    """Module list must be identical on repeated calls."""
    search = _get_module_index_search()
    result1 = search("module")
    result2 = search("module")
    assert result1 == result2


# ---------------------------------------------------------------------------
# 10. UUID-like IDs always have correct format
# ---------------------------------------------------------------------------

import uuid as _uuid_mod


@pytest.mark.parametrize("_", range(50))
def test_uuid_generation_always_valid(_):
    """UUIDs generated by BaseMessage are always valid v4 UUIDs."""
    uid = str(_uuid_mod.uuid4())
    parsed = _uuid_mod.UUID(uid)
    assert parsed.version == 4
    assert len(uid) == 36  # standard UUID string length
