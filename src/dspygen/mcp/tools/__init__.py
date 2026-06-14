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


def collect_all_tool_definitions():
    """Return a flat list of all Tool descriptors from all tool modules."""
    tools = []
    for module_path in (
        "dspygen.mcp.tools.module_tools",
        "dspygen.mcp.tools.agent_tools",
        "dspygen.mcp.tools.workflow_tools",
        "dspygen.mcp.tools.retrieval_tools",
    ):
        try:
            import importlib
            mod = importlib.import_module(module_path)
            tools.extend(mod.get_tool_definitions())
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning(
                "Could not load tool definitions from %s: %s", module_path, exc
            )
    return tools


async def dispatch_tool(name: str, arguments: dict):
    """
    Route a tool call to the owning module.

    Returns the list[TextContent] result, or raises ValueError if no module
    owns the tool name.
    """
    import importlib

    for module_path in (
        "dspygen.mcp.tools.module_tools",
        "dspygen.mcp.tools.agent_tools",
        "dspygen.mcp.tools.workflow_tools",
        "dspygen.mcp.tools.retrieval_tools",
    ):
        try:
            mod = importlib.import_module(module_path)
            result = await mod.handle_tool(name, arguments)
            if result is not None:
                return result
        except Exception as exc:
            import mcp.types as types
            import json
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": f"Tool dispatch error in {module_path}: {exc}"}),
                )
            ]

    raise ValueError(f"Unknown tool: {name!r}")
