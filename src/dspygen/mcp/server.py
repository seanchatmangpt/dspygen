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

Tool coverage (maximized):
  - 5  generic module tools (list, inspect, run, generate signature/module)
  - 5  agent tools
  - 4  workflow tools
  - 3  generic retrieval tools
  - 12 RDDDY domain tools (create_aggregate, event_storm, scaffold_domain, …)
  - 20 category-specific module tools (generate_tweet, summarize_document, …)
  - 8  extended retrieval tools (per-RM-module)
  - 7  LM configuration and sampling tools
  - 3  writer tools

Resource coverage (maximized):
  - dspygen://modules         — full module catalog
  - dspygen://agents          — full agent catalog
  - dspygen://workflows       — workflow examples catalog
  - dspygen://signatures      — all DSPy signature classes
  - dspygen://rdddy           — RDDDY pattern catalog
  - dspygen://signatures/all  — all signatures (extended)
  - dspygen://lm/providers    — LM provider catalog
  - dspygen://rm/catalog      — retrieval module catalog
  - dspygen://writers/catalog — writer catalog
  - dspygen://modules/{name}  — per-module documentation
  - dspygen://agents/{name}   — per-agent state machine info
  - dspygen://workflows/examples/{name} — individual workflow YAML

Prompt coverage (maximized):
  Domain (10): design-bounded-context, create-aggregate-root, event-storm-domain,
    design-saga, create-value-object, design-api, write-command-handler,
    implement-policy, generate-read-model, scaffold-microservice
  Module (10): generate-module, create-signature, optimize-module, debug-module,
    document-module, test-module, compose-pipeline, chain-modules,
    benchmark-module, refactor-module
  Workflow (5): design-workflow, debug-pipeline, convert-to-yaml-dsl,
    optimize-pipeline, generate-workflow-tests
  Legacy (2): explain-signature (retained for backwards compat)
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from loguru import logger
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

__all__ = ["create_server", "run_stdio", "run_sse"]


# ---------------------------------------------------------------------------
# Legacy prompts (kept for backwards compatibility)
# ---------------------------------------------------------------------------

_LEGACY_PROMPTS: list[types.Prompt] = [
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


_LEGACY_RENDERERS = {
    "explain-signature": _render_explain_signature,
}


# ---------------------------------------------------------------------------
# Base catalog resources (kept for server.py local use)
# ---------------------------------------------------------------------------

_BASE_CATALOG_RESOURCES: list[types.Resource] = [
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
    # Resources — base catalog + extended catalog
    # ------------------------------------------------------------------ #

    @server.list_resources()
    async def _list_resources() -> list[types.Resource]:
        resources = list(_BASE_CATALOG_RESOURCES)
        try:
            from dspygen.mcp.resources.extended_catalog import get_extended_resources  # lazy
            extended = get_extended_resources()
            # Deduplicate by URI
            existing_uris = {r.uri for r in resources}
            for r in extended:
                if r.uri not in existing_uris:
                    resources.append(r)
                    existing_uris.add(r.uri)
        except Exception as exc:
            logger.warning(f"Could not load extended resources: {exc}")
        return resources

    @server.read_resource()
    async def _read_resource(uri: str) -> str:  # type: ignore[return]
        try:
            # Try extended catalog first (handles more URIs including dynamic ones)
            try:
                from dspygen.mcp.resources.extended_catalog import read_extended_resource  # lazy
                result = read_extended_resource(uri)
                if result is not None:
                    return result
            except Exception as exc:
                logger.debug(f"extended_catalog did not handle {uri!r}: {exc}")

            # Fall back to base catalog
            from dspygen.mcp.resources.catalog import (  # lazy
                _build_agent_catalog,
                _build_module_catalog,
                _build_signatures_catalog,
                _build_workflow_catalog,
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
    # Prompts — all prompt libraries + legacy
    # ------------------------------------------------------------------ #

    @server.list_prompts()
    async def _list_prompts() -> list[types.Prompt]:
        prompts: list[types.Prompt] = []
        try:
            from dspygen.mcp.prompts import get_all_prompts  # lazy
            prompts.extend(get_all_prompts())
        except Exception as exc:
            logger.warning(f"Could not load extended prompts: {exc}")

        # Add legacy prompts not already in the list
        existing_names = {p.name for p in prompts}
        for p in _LEGACY_PROMPTS:
            if p.name not in existing_names:
                prompts.append(p)

        return prompts

    @server.get_prompt()
    async def _get_prompt(
        name: str, arguments: dict[str, str] | None
    ) -> types.GetPromptResult:
        # Try extended prompt library first
        try:
            from dspygen.mcp.prompts import render_prompt  # lazy
            return render_prompt(name, arguments or {})
        except ValueError:
            pass  # Not found in extended library; try legacy
        except Exception as exc:
            logger.warning(f"Extended prompt render failed for {name!r}: {exc}")

        # Try legacy prompts
        renderer = _LEGACY_RENDERERS.get(name)
        if renderer is not None:
            messages = renderer(arguments or {})
            prompt_obj = next((p for p in _LEGACY_PROMPTS if p.name == name), None)
            description = prompt_obj.description if prompt_obj else ""
            return types.GetPromptResult(description=description, messages=messages)

        raise ValueError(f"Unknown prompt: {name!r}")

    logger.info("dspygen MCP server created successfully (maximized — tools/resources/prompts)")
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
        from starlette.routing import Mount, Route  # lazy
    except ImportError as exc:
        raise ImportError(
            "fastapi and mcp[sse] are required for SSE transport. "
            "Install them with: pip install fastapi mcp[sse]"
        ) from exc

    _configure_env()
    server = create_server()

    if app is None:
        app = FastAPI(title="dspygen MCP Server", version="2.0.0")

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
