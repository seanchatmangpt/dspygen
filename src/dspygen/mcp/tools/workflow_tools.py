"""
MCP tools for dspygen pipeline and workflow execution.

Provides tools to execute DSL pipelines and YAML-based workflows.
All dspygen imports are lazy to avoid startup failures.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

import mcp.types as types
from loguru import logger

__all__ = ["get_tool_definitions", "handle_tool"]

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _dspygen_root() -> Path:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        if (candidate / "dspygen").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate dspygen source root")


def _pipeline_examples_dir() -> Path:
    return _dspygen_root() / "dspygen" / "llm_pipe" / "examples"


def _workflow_dir() -> Path:
    return _dspygen_root() / "dspygen" / "workflow"


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def _ok(data: Any) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]


def _err(msg: str) -> list[types.TextContent]:
    logger.error(msg)
    return [types.TextContent(type="text", text=json.dumps({"error": msg}))]


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

_TOOL_NAMES = {
    "execute_pipeline",
    "execute_workflow",
    "list_workflow_examples",
    "validate_pipeline",
    "run_pipeline_from_file",
}


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all workflow / pipeline tools."""
    return [
        types.Tool(
            name="execute_pipeline",
            description=(
                "Execute a dspygen DSL pipeline from a YAML string via DSLPipelineExecutor. "
                "Returns the resulting context dict."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "yaml_content": {
                        "type": "string",
                        "description": "Full YAML content of the pipeline DSL",
                    },
                    "init_ctx": {
                        "type": "object",
                        "description": "Optional initial context variables injected into the pipeline",
                    },
                },
                "required": ["yaml_content"],
            },
        ),
        types.Tool(
            name="execute_workflow",
            description=(
                "Execute a dspygen workflow from a YAML string using WorkflowEngine. "
                "Returns the resulting context dict."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_yaml": {
                        "type": "string",
                        "description": "Full YAML content of the workflow definition",
                    }
                },
                "required": ["workflow_yaml"],
            },
        ),
        types.Tool(
            name="list_workflow_examples",
            description=(
                "List all built-in pipeline and workflow YAML examples bundled with dspygen, "
                "including a short content preview of each."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="validate_pipeline",
            description=(
                "Parse and validate a pipeline YAML without executing it. "
                "Returns step count and signature names if valid, or an error message."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "yaml_content": {
                        "type": "string",
                        "description": "Full YAML content of the pipeline DSL to validate",
                    }
                },
                "required": ["yaml_content"],
            },
        ),
        types.Tool(
            name="run_pipeline_from_file",
            description=(
                "Read a pipeline YAML file from disk by path and execute it via DSLPipelineExecutor. "
                "Returns the resulting context dict as TextContent."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Absolute or relative path to a pipeline YAML file on disk",
                    },
                    "init_ctx": {
                        "type": "object",
                        "description": "Optional initial context variables injected into the pipeline",
                    },
                },
                "required": ["file_path"],
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

    if name == "execute_pipeline":
        return await _execute_pipeline(arguments)
    if name == "execute_workflow":
        return await _execute_workflow(arguments)
    if name == "list_workflow_examples":
        return await _list_workflow_examples(arguments)
    if name == "validate_pipeline":
        return await _validate_pipeline(arguments)
    if name == "run_pipeline_from_file":
        return await _run_pipeline_from_file(arguments)

    return _err(f"Unhandled tool: {name}")


async def _execute_pipeline(args: dict) -> list[types.TextContent]:
    yaml_content: str = (args or {}).get("yaml_content", "")
    init_ctx: dict = (args or {}).get("init_ctx", {})
    if not yaml_content:
        return _err("yaml_content argument is required")
    try:
        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.llm_pipe.dsl_pipeline_executor import execute_pipeline as _exec  # lazy

        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml") as tmp:
            tmp.write(yaml_content)
            tmp_path = tmp.name

        try:
            context = _exec(tmp_path, init_ctx if init_ctx else None)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        if hasattr(context, "toDict"):
            ctx_dict = context.toDict()
        elif hasattr(context, "items"):
            ctx_dict = {
                k: v
                for k, v in context.items()
                if isinstance(v, (str, int, float, bool, list, dict, type(None)))
            }
        else:
            ctx_dict = {"result": str(context)}

        return _ok({"status": "success", "context": ctx_dict})
    except Exception as exc:
        logger.exception("execute_pipeline error")
        return _err(f"execute_pipeline failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _execute_workflow(args: dict) -> list[types.TextContent]:
    workflow_yaml: str = (args or {}).get("workflow_yaml", "")
    if not workflow_yaml:
        return _err("workflow_yaml argument is required")
    try:
        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.workflow.workflow_models import Workflow  # lazy
        from dspygen.workflow.workflow_executor import execute_workflow as _exec  # lazy

        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml") as tmp:
            tmp.write(workflow_yaml)
            tmp_path = tmp.name

        try:
            wf = Workflow.from_yaml(tmp_path)
            context = _exec(wf)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        ctx_dict = {}
        if hasattr(context, "items"):
            ctx_dict = {
                k: v
                for k, v in context.items()
                if isinstance(v, (str, int, float, bool, list, dict, type(None)))
            }
        else:
            ctx_dict = {"result": str(context)}

        return _ok({"status": "success", "context": ctx_dict})
    except Exception as exc:
        logger.exception("execute_workflow error")
        return _err(f"execute_workflow failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _list_workflow_examples(args: dict) -> list[types.TextContent]:
    try:
        result = []
        for yaml_dir, cat_type in [
            (_pipeline_examples_dir(), "pipeline"),
            (_workflow_dir(), "workflow"),
        ]:
            if not yaml_dir.is_dir():
                continue
            for yaml_file in sorted(yaml_dir.glob("*.yaml")):
                result.append(
                    {
                        "type": cat_type,
                        "name": yaml_file.stem,
                        "path": str(yaml_file),
                        "content_preview": yaml_file.read_text()[:300],
                    }
                )
        return _ok(result)
    except Exception as exc:
        return _err(f"list_workflow_examples failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _validate_pipeline(args: dict) -> list[types.TextContent]:
    yaml_content: str = (args or {}).get("yaml_content", "")
    if not yaml_content:
        return _err("yaml_content argument is required")
    try:
        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.llm_pipe.dsl_pydantic_models import PipelineDSLModel  # lazy

        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml") as tmp:
            tmp.write(yaml_content)
            tmp_path = tmp.name

        try:
            pipeline = PipelineDSLModel.from_yaml(tmp_path)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        return _ok(
            {
                "valid": True,
                "steps": len(pipeline.steps),
                "signatures": [s.name for s in pipeline.signatures],
                "lm_models": [m.label for m in (pipeline.config.lm_models or [])],
            }
        )
    except Exception as exc:
        logger.exception("validate_pipeline error")
        return _err(f"validate_pipeline failed — invalid pipeline YAML: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _run_pipeline_from_file(args: dict) -> list[types.TextContent]:
    file_path: str = (args or {}).get("file_path", "")
    init_ctx: dict = (args or {}).get("init_ctx", {})
    if not file_path:
        return _err("file_path argument is required")
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.exists():
            return _err(f"File not found: {path}")
        if not path.is_file():
            return _err(f"Path is not a file: {path}")

        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.llm_pipe.dsl_pipeline_executor import execute_pipeline as _exec  # lazy

        context = _exec(str(path), init_ctx if init_ctx else None)

        if hasattr(context, "toDict"):
            ctx_dict = context.toDict()
        elif hasattr(context, "items"):
            ctx_dict = {
                k: v
                for k, v in context.items()
                if isinstance(v, (str, int, float, bool, list, dict, type(None)))
            }
        else:
            ctx_dict = {"result": str(context)}

        return [
            types.TextContent(
                type="text",
                text=json.dumps({"status": "success", "file": str(path), "context": ctx_dict}, indent=2),
            )
        ]
    except Exception as exc:
        logger.exception(f"run_pipeline_from_file error for {file_path!r}")
        return _err(f"run_pipeline_from_file failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")
