"""
dspygen MCP (Model Context Protocol) server package.

Exposes the entire dspygen framework as MCP tools, resources, and prompts.
"""

from dspygen.mcp.server import create_server, run_stdio, run_sse

__all__ = ["create_server", "run_stdio", "run_sse"]
