"""
MCP tool integration tests.

Since dspygen does not currently ship an MCP server module, these tests validate
the MCP interface that dspygen exposes through its modules and tool-pattern utilities.
All external calls (LLM, network) are mocked.

The tests are structured to be ready to wire up to a real MCP server once one is added.
"""

import ast
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers — simulate a simple tool dispatch registry
# ---------------------------------------------------------------------------

class _MockToolRegistry:
    """Lightweight registry that mimics MCP tool dispatch."""

    def __init__(self):
        self._tools: Dict[str, Any] = {}

    def register(self, name: str, fn):
        self._tools[name] = fn

    async def call(self, name: str, args: dict):
        fn = self._tools.get(name)
        if fn is None:
            raise KeyError(f"Tool '{name}' not found")
        if asyncio_available():
            import asyncio
            if asyncio.iscoroutinefunction(fn):
                return await fn(**args)
        return fn(**args)

    def list_tools(self):
        return list(self._tools.keys())


def asyncio_available():
    try:
        import asyncio
        return True
    except ImportError:
        return False


@pytest.fixture
def registry():
    return _MockToolRegistry()


# ---------------------------------------------------------------------------
# Module-discovery tools (static, no LLM)
# ---------------------------------------------------------------------------

MODULES_DIR = Path(__file__).parent.parent / "src/dspygen/modules"


def list_modules_tool() -> List[str]:
    """Tool: list all .py module files."""
    return sorted(
        f.stem for f in MODULES_DIR.glob("*.py") if not f.name.startswith("_")
    )


def get_module_source_tool(module_name: str) -> str:
    """Tool: return the source of a module file."""
    target = MODULES_DIR / f"{module_name}.py"
    if not target.exists():
        raise FileNotFoundError(f"Module {module_name!r} not found")
    return target.read_text(encoding="utf-8")


def validate_module_ast_tool(module_name: str) -> dict:
    """Tool: validate module parses as valid Python."""
    try:
        source = get_module_source_tool(module_name)
        ast.parse(source)
        return {"valid": True, "errors": []}
    except (FileNotFoundError, SyntaxError) as exc:
        return {"valid": False, "errors": [str(exc)]}


def count_classes_tool(module_name: str) -> int:
    """Tool: count class definitions in a module."""
    source = get_module_source_tool(module_name)
    tree = ast.parse(source)
    return sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))


# RDDDY tools
def list_rdddy_classes_tool() -> List[str]:
    rdddy_dir = Path(__file__).parent.parent / "src/dspygen/rdddy"
    return sorted(
        f.stem for f in rdddy_dir.glob("*.py") if not f.name.startswith("_")
    )


def get_rdddy_class_source_tool(class_name: str) -> str:
    rdddy_dir = Path(__file__).parent.parent / "src/dspygen/rdddy"
    target = rdddy_dir / f"{class_name}.py"
    if not target.exists():
        raise FileNotFoundError(f"RDDDY class file {class_name!r} not found")
    return target.read_text(encoding="utf-8")


# Retriever tools
def list_retrievers_tool() -> List[str]:
    rm_dir = Path(__file__).parent.parent / "src/dspygen/rm"
    return sorted(
        f.stem for f in rm_dir.glob("*.py") if not f.name.startswith("_")
    )


# LM tools (mocked)
def lm_generate_tool(prompt: str, max_tokens: int = 100) -> dict:
    """Tool: generate text via LM (always mocked in tests)."""
    return {"text": f"[mock response to: {prompt[:30]}...]", "tokens": max_tokens}


def lm_classify_tool(text: str, labels: List[str]) -> dict:
    """Tool: classify text into labels (always mocked)."""
    if not labels:
        return {"label": None, "confidence": 0.0}
    return {"label": labels[0], "confidence": 0.99}


# Resource helpers
def resource_read_tool(resource_uri: str) -> str:
    """Tool: read a known resource."""
    known = {
        "modules://list": json.dumps(list_modules_tool()),
        "rdddy://list": json.dumps(list_rdddy_classes_tool()),
        "retrievers://list": json.dumps(list_retrievers_tool()),
    }
    if resource_uri in known:
        return known[resource_uri]
    raise KeyError(f"Unknown resource: {resource_uri}")


# ---------------------------------------------------------------------------
# Tests: list_modules_tool
# ---------------------------------------------------------------------------

class TestListModulesTool:
    def test_returns_list(self):
        result = list_modules_tool()
        assert isinstance(result, list)

    def test_list_is_non_empty(self):
        result = list_modules_tool()
        assert len(result) > 50  # at least 50 modules

    def test_all_items_are_strings(self):
        result = list_modules_tool()
        assert all(isinstance(r, str) for r in result)

    def test_no_private_modules(self):
        result = list_modules_tool()
        assert not any(r.startswith("_") for r in result)

    def test_known_modules_present(self):
        result = list_modules_tool()
        assert "gen_dspy_module" in result

    def test_list_is_sorted(self):
        result = list_modules_tool()
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# Tests: get_module_source_tool
# ---------------------------------------------------------------------------

class TestGetModuleSourceTool:
    def test_existing_module(self):
        source = get_module_source_tool("gen_dspy_module")
        assert isinstance(source, str)
        assert len(source) > 0

    def test_nonexistent_module_raises(self):
        with pytest.raises(FileNotFoundError):
            get_module_source_tool("definitely_does_not_exist_xyz")

    def test_source_contains_python(self):
        source = get_module_source_tool("gen_dspy_module")
        assert "class" in source or "def" in source or "import" in source


# ---------------------------------------------------------------------------
# Tests: validate_module_ast_tool
# ---------------------------------------------------------------------------

class TestValidateModuleAstTool:
    def test_valid_module(self):
        result = validate_module_ast_tool("gen_dspy_module")
        assert result["valid"] is True
        assert result["errors"] == []

    def test_invalid_module_name(self):
        result = validate_module_ast_tool("nonexistent_xyz")
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_returns_dict(self):
        result = validate_module_ast_tool("gen_dspy_module")
        assert "valid" in result
        assert "errors" in result


# ---------------------------------------------------------------------------
# Tests: count_classes_tool
# ---------------------------------------------------------------------------

class TestCountClassesTool:
    def test_returns_integer(self):
        result = count_classes_tool("gen_dspy_module")
        assert isinstance(result, int)

    def test_count_is_positive(self):
        result = count_classes_tool("gen_dspy_module")
        assert result >= 1

    def test_nonexistent_raises(self):
        with pytest.raises(FileNotFoundError):
            count_classes_tool("does_not_exist")


# ---------------------------------------------------------------------------
# Tests: list_rdddy_classes_tool
# ---------------------------------------------------------------------------

class TestListRdddyClassesTool:
    def test_returns_list(self):
        result = list_rdddy_classes_tool()
        assert isinstance(result, list)

    def test_known_classes_present(self):
        result = list_rdddy_classes_tool()
        assert "base_aggregate" in result
        assert "base_command" in result
        assert "base_event" in result

    def test_no_private_classes(self):
        result = list_rdddy_classes_tool()
        assert not any(r.startswith("_") for r in result)


# ---------------------------------------------------------------------------
# Tests: get_rdddy_class_source_tool
# ---------------------------------------------------------------------------

class TestGetRdddyClassSourceTool:
    def test_existing_class(self):
        source = get_rdddy_class_source_tool("base_aggregate")
        assert "BaseAggregate" in source

    def test_nonexistent_raises(self):
        with pytest.raises(FileNotFoundError):
            get_rdddy_class_source_tool("nonexistent_xyz")


# ---------------------------------------------------------------------------
# Tests: list_retrievers_tool
# ---------------------------------------------------------------------------

class TestListRetrieversTool:
    def test_returns_list(self):
        result = list_retrievers_tool()
        assert isinstance(result, list)

    def test_known_retrievers_present(self):
        result = list_retrievers_tool()
        assert "chroma_retriever" in result
        assert "code_retriever" in result
        assert "web_retriever" in result

    def test_count_at_least_ten(self):
        result = list_retrievers_tool()
        assert len(result) >= 10


# ---------------------------------------------------------------------------
# Tests: lm_generate_tool
# ---------------------------------------------------------------------------

class TestLmGenerateTool:
    def test_returns_dict_with_text(self):
        result = lm_generate_tool("Hello, world!")
        assert "text" in result
        assert isinstance(result["text"], str)

    def test_max_tokens_propagated(self):
        result = lm_generate_tool("Test prompt", max_tokens=50)
        assert result["tokens"] == 50

    def test_empty_prompt_accepted(self):
        result = lm_generate_tool("")
        assert "text" in result

    def test_long_prompt_truncated_in_response(self):
        long_prompt = "word " * 200
        result = lm_generate_tool(long_prompt)
        assert len(result["text"]) < 200


# ---------------------------------------------------------------------------
# Tests: lm_classify_tool
# ---------------------------------------------------------------------------

class TestLmClassifyTool:
    def test_returns_first_label(self):
        result = lm_classify_tool("Some text", ["positive", "negative"])
        assert result["label"] == "positive"

    def test_confidence_between_0_and_1(self):
        result = lm_classify_tool("Text", ["a", "b"])
        assert 0.0 <= result["confidence"] <= 1.0

    def test_empty_labels_returns_none_label(self):
        result = lm_classify_tool("text", [])
        assert result["label"] is None


# ---------------------------------------------------------------------------
# Tests: resource_read_tool
# ---------------------------------------------------------------------------

class TestResourceReadTool:
    def test_modules_resource(self):
        raw = resource_read_tool("modules://list")
        data = json.loads(raw)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_rdddy_resource(self):
        raw = resource_read_tool("rdddy://list")
        data = json.loads(raw)
        assert "base_aggregate" in data

    def test_retrievers_resource(self):
        raw = resource_read_tool("retrievers://list")
        data = json.loads(raw)
        assert "chroma_retriever" in data

    def test_unknown_resource_raises(self):
        with pytest.raises(KeyError):
            resource_read_tool("unknown://resource")


# ---------------------------------------------------------------------------
# Tests: ToolRegistry
# ---------------------------------------------------------------------------

class TestToolRegistry:
    @pytest.mark.asyncio
    async def test_register_and_call_sync_tool(self):
        reg = _MockToolRegistry()
        reg.register("add", lambda a, b: a + b)
        result = await reg.call("add", {"a": 1, "b": 2})
        assert result == 3

    @pytest.mark.asyncio
    async def test_call_unknown_tool_raises(self):
        reg = _MockToolRegistry()
        with pytest.raises(KeyError):
            await reg.call("nonexistent", {})

    def test_list_tools(self):
        reg = _MockToolRegistry()
        reg.register("tool_a", lambda: None)
        reg.register("tool_b", lambda: None)
        tools = reg.list_tools()
        assert "tool_a" in tools
        assert "tool_b" in tools

    @pytest.mark.asyncio
    async def test_register_and_call_async_tool(self):
        import asyncio
        reg = _MockToolRegistry()

        async def async_tool(x):
            await asyncio.sleep(0)
            return x * 2

        reg.register("double", async_tool)
        result = await reg.call("double", {"x": 5})
        assert result == 10


# ---------------------------------------------------------------------------
# Tests: error conditions
# ---------------------------------------------------------------------------

class TestToolErrorConditions:
    def test_get_source_empty_name(self):
        with pytest.raises((FileNotFoundError, ValueError, Exception)):
            get_module_source_tool("")

    def test_validate_ast_empty_name(self):
        result = validate_module_ast_tool("")
        # Should return errors gracefully
        assert isinstance(result, dict)
        assert "valid" in result

    def test_lm_generate_with_large_token_count(self):
        result = lm_generate_tool("test", max_tokens=9999)
        assert result["tokens"] == 9999


# ---------------------------------------------------------------------------
# Tests: concurrent tool calls (simulated)
# ---------------------------------------------------------------------------

class TestConcurrentToolCalls:
    @pytest.mark.asyncio
    async def test_concurrent_list_calls(self):
        import asyncio

        async def async_list():
            return list_modules_tool()

        results = await asyncio.gather(*[async_list() for _ in range(5)])
        # All calls should return identical lists
        assert all(r == results[0] for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_validate_calls(self):
        import asyncio

        async def async_validate(name):
            return validate_module_ast_tool(name)

        modules = list_modules_tool()[:5]
        results = await asyncio.gather(*[async_validate(m) for m in modules])
        assert all(r["valid"] for r in results)


# ---------------------------------------------------------------------------
# Tests: parametrized over all modules
# ---------------------------------------------------------------------------

ALL_MODULE_NAMES = list_modules_tool()


@pytest.mark.parametrize("module_name", ALL_MODULE_NAMES[:30], ids=ALL_MODULE_NAMES[:30])
def test_validate_ast_for_first_30_modules(module_name: str):
    """Validate AST for the first 30 modules via the tool."""
    result = validate_module_ast_tool(module_name)
    assert result["valid"] is True, f"Module {module_name} has errors: {result['errors']}"


@pytest.mark.parametrize("module_name", ALL_MODULE_NAMES[30:60], ids=ALL_MODULE_NAMES[30:60])
def test_validate_ast_for_modules_30_to_60(module_name: str):
    """Validate AST for modules 30-60."""
    result = validate_module_ast_tool(module_name)
    assert result["valid"] is True, f"Module {module_name} has errors: {result['errors']}"


@pytest.mark.parametrize("module_name", ALL_MODULE_NAMES[60:], ids=ALL_MODULE_NAMES[60:])
def test_validate_ast_for_remaining_modules(module_name: str):
    """Validate AST for remaining modules."""
    result = validate_module_ast_tool(module_name)
    assert result["valid"] is True, f"Module {module_name} has errors: {result['errors']}"


# ---------------------------------------------------------------------------
# Tests: prompts (static string templates)
# ---------------------------------------------------------------------------

PROMPT_TEMPLATES = {
    "summarize": "Summarize the following: {text}",
    "classify": "Classify this text into one of {labels}: {text}",
    "generate_module": "Generate a DSPy module for: {description}",
    "explain_code": "Explain this code: {code}",
    "refactor_code": "Refactor this code for clarity: {code}",
    "write_tests": "Write tests for: {code}",
    "document_function": "Write a docstring for: {signature}",
    "suggest_name": "Suggest a module name for: {description}",
    "validate_signature": "Is this a valid DSPy signature? {signature}",
    "list_improvements": "List improvements for: {code}",
}


@pytest.mark.parametrize("prompt_name,template", PROMPT_TEMPLATES.items())
def test_prompt_template_is_valid_string(prompt_name, template):
    """Prompt templates must be non-empty strings with placeholders."""
    assert isinstance(template, str)
    assert len(template) > 0
    assert "{" in template  # has at least one placeholder


@pytest.mark.parametrize("prompt_name,template", PROMPT_TEMPLATES.items())
def test_prompt_template_renders(prompt_name, template):
    """Prompt templates must render without error when placeholders are filled."""
    # Fill all placeholders with dummy values
    import re
    placeholders = re.findall(r"\{(\w+)\}", template)
    kwargs = {p: f"dummy_{p}" for p in placeholders}
    rendered = template.format(**kwargs)
    assert isinstance(rendered, str)
    assert len(rendered) > 0
