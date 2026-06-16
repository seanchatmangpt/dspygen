"""
dspygen MCP resources subpackage.

Provides MCP resource handlers exposing the dspygen module/agent/workflow catalog.
"""

__all__ = ["register_resources"]


def register_resources(server):
    from dspygen.mcp.resources.catalog import register_resources as _register
    _register(server)
