"""
dspygen MCP Server — main entry point.

Exposes the entire dspygen framework as MCP tools, resources, and prompts.

Transport modes:
  stdio  (primary)   — launched by MCP clients as a subprocess
  SSE    (secondary) — mounted on a FastAPI application

Environment variables read at startup:
  DSPYGEN_MODEL     — default LM model name (e.g. 'gpt-4o')
  OPENAI_API_KEY    — OpenAI API key forwarded to dspy
  OLLAMA_HOST       — Ollama base URL (e.g. 'http://localhost:11434')
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

import mcp.types as types
from loguru import logger
from mcp.server import Server
from mcp.server.stdio import stdio_server

__all__ = ["create_server", "run_stdio", "run_sse"]

# ---------------------------------------------------------------------------
# Built-in Prompts
# ---------------------------------------------------------------------------

_PROMPTS: list[types.Prompt] = [
    types.Prompt(
        name="generate-module",
        description=(
            "Template prompt for generating a new dspygen DSPy module. "
            "Provide the module purpose and desired inputs/outputs."
        ),
        arguments=[
            types.PromptArgument(
                name="module_purpose",
                description="What should the module do?",
                required=True,
            ),
            types.PromptArgument(
                name="inputs",
                description="Comma-separated list of input field names",
                required=True,
            ),
            types.PromptArgument(
                name="outputs",
                description="Comma-separated list of output field names",
                required=True,
            ),
        ],
    ),
    types.Prompt(
        name="debug-pipeline",
        description=(
            "Prompt template for debugging a failing dspygen DSL pipeline. "
            "Paste the pipeline YAML and the error message."
        ),
        arguments=[
            types.PromptArgument(
                name="pipeline_yaml",
                description="The YAML content of the failing pipeline",
                required=True,
            ),
            types.PromptArgument(
                name="error_message",
                description="The error or unexpected output observed",
                required=True,
            ),
        ],
    ),
    types.Prompt(
        name="explain-signature",
        description=(
            "Prompt template for explaining what a DSPy Signature does, "
            "its intended use, and example usage."
        ),
        arguments=[
            types.PromptArgument(
                name="signature_class",
                description="The DSPy Signature class name or definition to explain",
                required=True,
            ),
        ],
    ),
]


def _render_generate_module(args: dict[str, str]) -> list[types.PromptMessage]:
    purpose = args.get("module_purpose", "")
    inputs = args.get("inputs", "")
    outputs = args.get("outputs", "")
    text = (
        "You are an expert DSPy developer working with the dspygen framework.\n\n"
        "Generate a complete dspygen DSPy module for the following purpose:\n"
        f"**Purpose:** {purpose}\n\n"
        f"**Input fields:** {inputs}\n"
        f"**Output fields:** {outputs}\n\n"
        "Requirements:\n"
        "1. Define a `dspy.Signature` subclass with a descriptive docstring.\n"
        "2. Assign `dspy.InputField(desc=...)` for each input.\n"
        "3. Assign `dspy.OutputField(desc=...)` for each output.\n"
        "4. Define a `dspy.Module` subclass using `dspy.ChainOfThought` or `dspy.Predict`.\n"
        "5. Add a `<module_name>_call(...)` convenience function.\n"
        "6. Add a Typer CLI `call` command.\n"
        "7. Follow dspygen naming: file as `<snake_case>_module.py`.\n\n"
        "Return only the complete Python source code."
    )
    return [types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))]


def _render_debug_pipeline(args: dict[str, str]) -> list[types.PromptMessage]:
    pipeline_yaml = args.get("pipeline_yaml", "")
    error_message = args.get("error_message", "")
    text = (
        "You are an expert in the dspygen DSL pipeline system.\n\n"
        "Analyse the following failing pipeline and diagnose the root cause.\n\n"
        f"**Pipeline YAML:**\n```yaml\n{pipeline_yaml}\n```\n\n"
        f"**Error observed:**\n```\n{error_message}\n```\n\n"
        "Please:\n"
        "1. Identify the exact cause of the failure.\n"
        "2. Explain the dspygen DSL concepts involved.\n"
        "3. Provide a corrected version of the pipeline YAML.\n"
        "4. Suggest any preventive measures.\n"
    )
    return [types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))]


def _render_explain_signature(args: dict[str, str]) -> list[types.PromptMessage]:
    sig_class = args.get("signature_class", "")
    text = (
        "You are an expert DSPy developer.\n\n"
        "Explain the following DSPy Signature in plain language:\n\n"
        f"```python\n{sig_class}\n```\n\n"
        "Please cover:\n"
        "1. **Purpose** — what task does this signature describe?\n"
        "2. **Inputs** — what each input field represents and expects.\n"
        "3. **Outputs** — what each output field produces.\n"
        "4. **Usage example** — a short Python snippet showing how to use it "
        "   with `dspy.Predict` or `dspy.ChainOfThought`.\n"
        "5. **Best predictor** — recommend Predict vs ChainOfThought and why.\n"
    )
    return [types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))]


_PROMPT_RENDERERS = {
    "generate-module": _render_generate_module,
    "debug-pipeline": _render_debug_pipeline,
    "explain-signature": _render_explain_signature,
}


# ---------------------------------------------------------------------------
# MCP Resources catalog
# ---------------------------------------------------------------------------

_CATALOG_RESOURCES: list[types.Resource] = [
    types.Resource(
        uri="dspygen://modules",
        name="dspygen Module Catalog",
        description="Full JSON catalog of all dspygen DSPy modules with signatures and docstrings.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://agents",
        name="dspygen Agent Catalog",
        description="Full JSON catalog of all dspygen FSM agents with state machine info.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://workflows",
        name="dspygen Workflow Examples",
        description="Catalog of built-in pipeline and workflow YAML examples bundled with dspygen.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://signatures",
        name="dspygen DSPy Signatures",
        description="All discovered DSPy Signature class definitions across the dspygen module library.",
        mimeType="application/json",
    ),
]


# ---------------------------------------------------------------------------
# Server factory
# ---------------------------------------------------------------------------


def create_server() -> Server:
    """
    Build and return a fully configured dspygen MCP Server.

    All tool, resource, and prompt handlers are registered before returning.
    The single list_tools / call_tool pair aggregates all tool submodules.
    """
    server = Server("dspygen")

    # ------------------------------------------------------------------ #
    # Tools — single consolidated list_tools + call_tool
    # ------------------------------------------------------------------ #

    @server.list_tools()
    async def _list_tools() -> list[types.Tool]:
        try:
            from dspygen.mcp.tools import collect_all_tool_definitions  # lazy

            return collect_all_tool_definitions()
        except Exception as exc:
            logger.error(f"list_tools error: {exc}")
            return []

    @server.call_tool()
    async def _call_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent]:
        try:
            from dspygen.mcp.tools import dispatch_tool  # lazy

            return await dispatch_tool(name, arguments or {})
        except ValueError:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name!r}"}),
                )
            ]
        except Exception as exc:
            logger.exception(f"call_tool error for {name!r}")
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps({"error": str(exc)}),
                )
            ]

    # ------------------------------------------------------------------ #
    # Resources
    # ------------------------------------------------------------------ #

    @server.list_resources()
    async def _list_resources() -> list[types.Resource]:
        return _CATALOG_RESOURCES

    @server.read_resource()
    async def _read_resource(uri: str) -> str:  # type: ignore[return]
        try:
            from dspygen.mcp.resources.catalog import (  # lazy
                _build_module_catalog,
                _build_agent_catalog,
                _build_workflow_catalog,
                _build_signatures_catalog,
            )

            if uri == "dspygen://modules":
                data = _build_module_catalog()
            elif uri == "dspygen://agents":
                data = _build_agent_catalog()
            elif uri == "dspygen://workflows":
                data = _build_workflow_catalog()
            elif uri == "dspygen://signatures":
                data = _build_signatures_catalog()
            else:
                return json.dumps({"error": f"Unknown resource URI: {uri}"})
            return json.dumps(data, indent=2)
        except Exception as exc:
            logger.exception(f"read_resource error for {uri}")
            return json.dumps({"error": str(exc)})

    # ------------------------------------------------------------------ #
    # Prompts
    # ------------------------------------------------------------------ #

    @server.list_prompts()
    async def _list_prompts() -> list[types.Prompt]:
        return _PROMPTS

    @server.get_prompt()
    async def _get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        renderer = _PROMPT_RENDERERS.get(name)
        if renderer is None:
            raise ValueError(f"Unknown prompt: {name!r}")
        messages = renderer(arguments or {})
        prompt_obj = next((p for p in _PROMPTS if p.name == name), None)
        description = prompt_obj.description if prompt_obj else ""
        return types.GetPromptResult(description=description, messages=messages)

    logger.info("dspygen MCP server created successfully")
    return server


# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------


def _configure_env() -> None:
    """
    Apply environment-variable configuration to dspygen / dspy if possible.
    Failures here are non-fatal.
    """
    model = os.environ.get("DSPYGEN_MODEL")
    openai_key = os.environ.get("OPENAI_API_KEY")
    ollama_host = os.environ.get("OLLAMA_HOST")

    if model or openai_key:
        try:
            src_dir = str(Path(__file__).resolve().parents[3])
            if src_dir not in sys.path:
                sys.path.insert(0, src_dir)
            import dspy  # lazy

            if openai_key and model:
                lm = dspy.LM(model=model, api_key=openai_key)
                dspy.configure(lm=lm)
                logger.info(f"Configured dspy with model={model}")
            elif model and ollama_host:
                lm = dspy.LM(model=model, api_base=ollama_host)
                dspy.configure(lm=lm)
                logger.info(
                    f"Configured dspy with Ollama model={model} host={ollama_host}"
                )
        except Exception as exc:
            logger.debug(f"Could not auto-configure dspy from env: {exc}")


# ---------------------------------------------------------------------------
# Transport: stdio
# ---------------------------------------------------------------------------


async def _run_stdio_async(server: Server) -> None:
    """Run the server over stdio transport (blocks until client disconnects)."""
    logger.info("Starting dspygen MCP server (stdio transport)")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


def run_stdio() -> None:
    """Entry point for stdio transport (called by ``__main__`` or CLI)."""
    _configure_env()
    server = create_server()
    asyncio.run(_run_stdio_async(server))


# ---------------------------------------------------------------------------
# Transport: SSE (FastAPI)
# ---------------------------------------------------------------------------


def run_sse(app: Any = None) -> Any:
    """
    Mount the dspygen MCP server as an SSE endpoint on a FastAPI app.

    If *app* is None a new FastAPI instance is created and returned.
    The SSE endpoint is available at ``/mcp/sse``.

    Example::

        from fastapi import FastAPI
        from dspygen.mcp.server import run_sse

        app = FastAPI()
        run_sse(app)
    """
    try:
        from fastapi import FastAPI  # lazy
        from mcp.server.sse import SseServerTransport  # lazy
        from starlette.routing import Route, Mount  # lazy
    except ImportError as exc:
        raise ImportError(
            "fastapi and mcp[sse] are required for SSE transport. "
            "Install them with: pip install fastapi mcp[sse]"
        ) from exc

    _configure_env()
    server = create_server()

    if app is None:
        app = FastAPI(title="dspygen MCP Server", version="1.0.0")

    sse_transport = SseServerTransport("/mcp/messages")

    async def handle_sse(request):
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0],
                streams[1],
                server.create_initialization_options(),
            )

    app.router.routes.append(Route("/mcp/sse", endpoint=handle_sse))
    app.router.routes.append(
        Mount("/mcp/messages", app=sse_transport.handle_post_message)
    )

    logger.info("dspygen MCP server mounted at /mcp/sse")
    return app


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_stdio()
