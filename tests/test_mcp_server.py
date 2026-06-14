"""Tests for dspygen MCP server."""

import json
import asyncio
import pytest

pytestmark = pytest.mark.mcp


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run(coro):
    """Run a coroutine synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def mcp_server():
    """Import and return the dspygen MCP server instance."""
    dspygen_mcp = pytest.importorskip(
        "dspygen.mcp.server",
        reason="dspygen.mcp.server not yet available",
    )
    return dspygen_mcp.mcp


# ---------------------------------------------------------------------------
# 1. Server creation
# ---------------------------------------------------------------------------

def test_server_creation():
    """Import Server from dspygen.mcp.server; verify it is a valid MCP server."""
    dspygen_mcp = pytest.importorskip(
        "dspygen.mcp.server",
        reason="dspygen.mcp.server not yet available",
    )
    from mcp.server.fastmcp import FastMCP

    server = dspygen_mcp.mcp
    assert server is not None, "Server object must not be None"
    assert isinstance(server, FastMCP), (
        f"Expected FastMCP instance, got {type(server)}"
    )


# ---------------------------------------------------------------------------
# 2. Tools registered
# ---------------------------------------------------------------------------

def test_server_has_tools(mcp_server):
    """The server must have at least one tool registered."""
    tools = _run(mcp_server.list_tools())
    assert len(tools) > 0, "Server must register at least one tool"
    tool_names = [t.name for t in tools]
    # Spot-check well-known tool names from the spec
    expected_subset = {
        "list_modules",
        "get_module_info",
        "run_module",
        "generate_dspy_signature",
        "generate_dspy_module",
        "list_agents",
        "get_agent_info",
        "create_coder_agent",
        "create_research_agent",
        "execute_pipeline",
        "execute_workflow",
        "list_workflow_examples",
        "validate_pipeline",
        "retrieve_from_chroma",
        "retrieve_from_web",
        "retrieve_from_code",
    }
    registered = set(tool_names)
    missing = expected_subset - registered
    assert not missing, (
        f"Expected tools not found: {missing}. Registered: {registered}"
    )


# ---------------------------------------------------------------------------
# 3. Resources registered
# ---------------------------------------------------------------------------

def test_server_has_resources(mcp_server):
    """The server must expose at least the four catalog resources."""
    resources = _run(mcp_server.list_resources())
    uris = {str(r.uri) for r in resources}
    expected_uris = {
        "dspygen://modules",
        "dspygen://agents",
        "dspygen://workflows",
        "dspygen://signatures",
    }
    missing = expected_uris - uris
    assert not missing, (
        f"Expected resource URIs not found: {missing}. Registered: {uris}"
    )


# ---------------------------------------------------------------------------
# 4. Prompts registered
# ---------------------------------------------------------------------------

def test_server_has_prompts(mcp_server):
    """The server must register at least one prompt."""
    prompts = _run(mcp_server.list_prompts())
    assert len(prompts) > 0, "Server must register at least one prompt"
    prompt_names = [p.name for p in prompts]
    assert any("module" in n.lower() or "generate" in n.lower() for n in prompt_names), (
        f"Expected a 'generate-module' style prompt. Got: {prompt_names}"
    )


# ---------------------------------------------------------------------------
# 5. Module catalog resource
# ---------------------------------------------------------------------------

def test_module_catalog_resource(mcp_server):
    """Read dspygen://modules resource and verify it contains entries."""
    contents = _run(mcp_server.read_resource("dspygen://modules"))
    assert contents, "Resource response must not be empty"
    raw = contents[0].content
    data = json.loads(raw)
    assert isinstance(data, list), "dspygen://modules must return a JSON list"
    assert len(data) >= 10, (
        f"Expected at least 10 module entries, got {len(data)}"
    )
    # Each entry should at minimum have a 'name' key
    for entry in data:
        assert "name" in entry, f"Module entry missing 'name': {entry}"


# ---------------------------------------------------------------------------
# 6. Agent catalog resource
# ---------------------------------------------------------------------------

def test_agent_catalog_resource(mcp_server):
    """Read dspygen://agents resource and verify it contains entries."""
    contents = _run(mcp_server.read_resource("dspygen://agents"))
    assert contents, "Resource response must not be empty"
    raw = contents[0].content
    data = json.loads(raw)
    assert isinstance(data, list), "dspygen://agents must return a JSON list"
    assert len(data) >= 1, "Expected at least one agent in the catalog"
    for entry in data:
        assert "name" in entry, f"Agent entry missing 'name': {entry}"


# ---------------------------------------------------------------------------
# 7. generate-module prompt
# ---------------------------------------------------------------------------

def test_generate_module_prompt(mcp_server):
    """The generate-module prompt must be accessible and have required arguments."""
    prompts = _run(mcp_server.list_prompts())
    prompt_names = [p.name for p in prompts]

    # Find a 'generate-module' or similarly named prompt
    target = next(
        (p for p in prompts if "generate" in p.name.lower() and "module" in p.name.lower()),
        None,
    )
    assert target is not None, (
        f"'generate-module' prompt not found. Available: {prompt_names}"
    )
    # Must have at least one argument
    assert target.arguments and len(target.arguments) >= 1, (
        "generate-module prompt must declare at least one argument"
    )
    arg_names = [a.name for a in target.arguments]
    # Expect at least a 'description' or 'name' argument
    assert any(a in arg_names for a in ("description", "name", "prompt", "module_name")), (
        f"generate-module prompt must have a descriptive argument. Got: {arg_names}"
    )
