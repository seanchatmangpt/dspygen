"""
MCP tools for the dspygen writer system.

Provides tools for listing, inspecting, and running dspygen writers
(code_writer, data_writer, google_sheets_writer) and Jinja2 template generation.

All imports of dspygen internals are lazy (inside handlers) to avoid startup failures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from loguru import logger
from mcp import types

__all__ = ["get_tool_definitions", "handle_tool"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ok(data: Any) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]


def _err(msg: str) -> list[types.TextContent]:
    logger.error(msg)
    return [types.TextContent(type="text", text=json.dumps({"error": msg}))]


def _src_root() -> Path:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        if (candidate / "dspygen").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate dspygen source root")


def _ensure_path() -> None:
    try:
        src = str(_src_root())
        if src not in sys.path:
            sys.path.insert(0, src)
    except Exception:
        pass


def _writer_dir() -> Path:
    return _src_root() / "dspygen" / "writer"


_TOOL_NAMES = {
    "list_writers",
    "run_writer",
    "generate_from_template",
}

# Known writers with their metadata
_KNOWN_WRITERS = {
    "code_writer": {
        "description": "Generate and write Python source code files",
        "module": "dspygen.writer.code_writer",
        "call_fn": "code_writer_call",
        "inputs": ["source"],
    },
    "data_writer": {
        "description": "Write structured data to files (JSON, CSV, etc.)",
        "module": "dspygen.writer.data_writer",
        "call_fn": "data_writer_call",
        "inputs": ["data", "format"],
    },
    "google_sheets_writer": {
        "description": "Write data to Google Sheets spreadsheets",
        "module": "dspygen.writer.google_sheets_writer",
        "call_fn": "google_sheets_writer_call",
        "inputs": ["data", "spreadsheet_id", "sheet_name"],
    },
}


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all writer tools."""
    return [
        types.Tool(
            name="list_writers",
            description=(
                "List all available dspygen writers. "
                "Returns a JSON array with writer names, descriptions, and input schemas."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="run_writer",
            description=(
                "Run a specific dspygen writer with provided context. "
                "Available writers: code_writer, data_writer, google_sheets_writer."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "writer_name": {
                        "type": "string",
                        "description": "Writer name: 'code_writer', 'data_writer', 'google_sheets_writer'",
                    },
                    "context": {
                        "type": "object",
                        "description": "Keyword arguments to pass to the writer's call function",
                    },
                },
                "required": ["writer_name"],
            },
        ),
        types.Tool(
            name="generate_from_template",
            description=(
                "Generate text content from a Jinja2 template string with dspygen context. "
                "Renders the template with provided variables, useful for code generation "
                "and structured text output."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "template": {
                        "type": "string",
                        "description": "Jinja2 template string (use {{ variable }} syntax)",
                    },
                    "variables": {
                        "type": "object",
                        "description": "Template variables as key-value pairs",
                        "default": {},
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Expected output format hint: python, yaml, json, markdown, html",
                        "default": "text",
                    },
                },
                "required": ["template"],
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def handle_tool(name: str, arguments: dict) -> list[types.TextContent] | None:
    """Dispatch a tool call. Returns None if this module does not own *name*."""
    if name not in _TOOL_NAMES:
        return None

    _ensure_path()

    handlers = {
        "list_writers": _list_writers,
        "run_writer": _run_writer,
        "generate_from_template": _generate_from_template,
    }

    handler = handlers.get(name)
    if handler:
        return await handler(arguments or {})
    return _err(f"Unhandled tool: {name}")


async def _list_writers(_args: dict) -> list[types.TextContent]:
    try:
        # Start with known writers
        writers = []
        for writer_name, info in _KNOWN_WRITERS.items():
            writers.append({
                "name": writer_name,
                "description": info["description"],
                "module": info["module"],
                "call_function": info["call_fn"],
                "inputs": info["inputs"],
            })

        # Also scan the writer directory for any additional writers
        try:
            writer_dir = _writer_dir()
            for p in sorted(writer_dir.glob("*.py")):
                if p.name == "__init__.py" or p.stem in _KNOWN_WRITERS:
                    continue
                # Check if it's a writer file
                try:
                    source = p.read_text(encoding="utf-8")
                    if "writer" in p.stem.lower() or "Writer" in source:
                        writers.append({
                            "name": p.stem,
                            "description": f"Writer from {p.name}",
                            "module": f"dspygen.writer.{p.stem}",
                            "call_function": f"{p.stem}_call",
                            "inputs": [],
                        })
                except Exception:
                    pass
        except Exception:
            pass

        return _ok({
            "writers": writers,
            "count": len(writers),
            "writer_directory": str(_writer_dir()) if _writer_dir().is_dir() else "not found",
        })
    except Exception as exc:
        logger.exception("list_writers error")
        return _err(f"list_writers failed: {exc}")


async def _run_writer(args: dict) -> list[types.TextContent]:
    writer_name = args.get("writer_name", "")
    context = args.get("context", {})

    if not writer_name:
        return _err("writer_name is required")

    try:
        import importlib

        # Try known writers first
        writer_info = _KNOWN_WRITERS.get(writer_name)
        if writer_info:
            module_path = writer_info["module"]
            call_fn_name = writer_info["call_fn"]
        else:
            # Try to dynamically find the writer
            module_path = f"dspygen.writer.{writer_name}"
            call_fn_name = f"{writer_name}_call"

        mod = importlib.import_module(module_path)
        call_fn = getattr(mod, call_fn_name, None)

        if call_fn is None:
            # Try to find any *_call function
            for attr_name in dir(mod):
                if attr_name.endswith("_call") and callable(getattr(mod, attr_name)):
                    call_fn = getattr(mod, attr_name)
                    break

        if call_fn is None:
            return _err(f"No *_call function found in writer '{writer_name}'")

        result = call_fn(**(context or {}))
        return _ok({
            "writer": writer_name,
            "result": str(result) if result is not None else "Writer executed (no return value)",
            "context_keys": list((context or {}).keys()),
        })
    except Exception as exc:
        logger.exception(f"run_writer error for {writer_name}")
        return _err(f"run_writer failed for '{writer_name}': {exc}")


async def _generate_from_template(args: dict) -> list[types.TextContent]:
    template_str = args.get("template", "")
    variables = args.get("variables", {})
    output_format = args.get("output_format", "text")

    if not template_str:
        return _err("template is required")

    try:
        # Try Jinja2 first
        try:
            from jinja2 import BaseLoader, Environment, StrictUndefined  # lazy

            env = Environment(
                loader=BaseLoader(),
                undefined=StrictUndefined,
                keep_trailing_newline=True,
            )
            tmpl = env.from_string(template_str)
            rendered = tmpl.render(**(variables or {}))
        except ImportError:
            # Fallback: simple string format
            rendered = template_str
            for key, value in (variables or {}).items():
                rendered = rendered.replace("{{ " + key + " }}", str(value))
                rendered = rendered.replace("{{" + key + "}}", str(value))

        return _ok({
            "rendered": rendered,
            "output_format": output_format,
            "variables_used": list((variables or {}).keys()),
            "template_length": len(template_str),
            "output_length": len(rendered),
        })
    except Exception as exc:
        logger.exception("generate_from_template error")
        return _err(f"generate_from_template failed: {exc}")
