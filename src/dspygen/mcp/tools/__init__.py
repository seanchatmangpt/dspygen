"""
dspygen MCP tools subpackage.

Each tool module exposes two public symbols:
  - ``get_tool_definitions() -> list[types.Tool]``
  - ``handle_tool(name, arguments) -> list[TextContent] | None``

The server consolidates these into a single list_tools and call_tool handler.
"""

__all__ = [
    "collect_all_tool_definitions",
    "dispatch_tool",
]

# Ordered list of all tool module paths.
# New modules are appended here — the dispatcher tries each in order and
# returns on the first non-None result.
_TOOL_MODULE_PATHS = [
    "dspygen.mcp.tools.module_tools",
    "dspygen.mcp.tools.agent_tools",
    "dspygen.mcp.tools.workflow_tools",
    "dspygen.mcp.tools.retrieval_tools",
    "dspygen.mcp.tools.rdddy_tools",
    "dspygen.mcp.tools.extended_module_tools",
    "dspygen.mcp.tools.extended_retrieval_tools",
    "dspygen.mcp.tools.lm_tools",
    "dspygen.mcp.tools.writer_tools",
]


def collect_all_tool_definitions():
    """Return a flat list of all Tool descriptors from all tool modules."""
    import importlib
    import logging

    _log = logging.getLogger(__name__)
    tools = []
    for module_path in _TOOL_MODULE_PATHS:
        try:
            mod = importlib.import_module(module_path)
            tools.extend(mod.get_tool_definitions())
        except Exception as exc:
            _log.warning(
                "Could not load tool definitions from %s: %s", module_path, exc
            )
    return tools


async def dispatch_tool(name: str, arguments: dict):
    """
    Route a tool call to the owning module.

    Iterates through all registered tool modules and returns the result
    from the first module that claims the tool (returns non-None).

    Raises ValueError if no module owns the tool name.
    """
    import importlib
    import json

    from mcp import types

    for module_path in _TOOL_MODULE_PATHS:
        try:
            mod = importlib.import_module(module_path)
            result = await mod.handle_tool(name, arguments)
            if result is not None:
                return result
        except Exception as exc:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": f"Tool dispatch error in {module_path}: {exc}"}),
                )
            ]

    raise ValueError(f"Unknown tool: {name!r}")
