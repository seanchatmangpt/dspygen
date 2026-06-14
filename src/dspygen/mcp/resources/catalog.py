"""
MCP Resources — dspygen catalog.

Registers browsable MCP resources:
  dspygen://modules     — full module catalog JSON
  dspygen://agents      — full agent catalog JSON
  dspygen://workflows   — workflow + pipeline example catalog
  dspygen://signatures  — discovered DSPy signature strings
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import mcp.types as types
from loguru import logger
from mcp.server import Server

__all__ = ["register_resources"]

# ---------------------------------------------------------------------------
# Path helpers (duplicated here to keep resources self-contained)
# ---------------------------------------------------------------------------


def _src_root() -> Path:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        if (candidate / "dspygen").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate dspygen source root")


def _modules_dir() -> Path:
    return _src_root() / "dspygen" / "modules"


def _agents_dir() -> Path:
    return _src_root() / "dspygen" / "agents"


def _workflow_dir() -> Path:
    return _src_root() / "dspygen" / "workflow"


def _pipeline_examples_dir() -> Path:
    return _src_root() / "dspygen" / "llm_pipe" / "examples"


# ---------------------------------------------------------------------------
# Catalog builders
# ---------------------------------------------------------------------------


def _extract_ast_meta(path: Path) -> dict[str, Any]:
    """Quick AST scan returning docstring, class names, and Signature subclasses."""
    meta: dict[str, Any] = {
        "name": path.stem,
        "file": str(path),
        "docstring": "",
        "classes": [],
        "signatures": [],
        "input_fields": [],
        "output_fields": [],
    }
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return meta

    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
    ):
        meta["docstring"] = tree.body[0].value.value.strip()[:400]

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [
            ast.unparse(b) if hasattr(ast, "unparse") else getattr(b, "id", "")
            for b in node.bases
        ]
        meta["classes"].append(node.name)
        if any("Signature" in b for b in bases):
            meta["signatures"].append(node.name)
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if not isinstance(target, ast.Name):
                            continue
                        if not isinstance(item.value, ast.Call):
                            continue
                        func_name = ""
                        if isinstance(item.value.func, ast.Attribute):
                            func_name = item.value.func.attr
                        elif isinstance(item.value.func, ast.Name):
                            func_name = item.value.func.id
                        if func_name == "InputField":
                            meta["input_fields"].append(target.id)
                        elif func_name == "OutputField":
                            meta["output_fields"].append(target.id)
    return meta


def _build_module_catalog() -> list[dict]:
    try:
        mdir = _modules_dir()
    except FileNotFoundError:
        return []
    catalog = []
    for p in sorted(mdir.glob("*.py")):
        if p.name == "__init__.py" or p.name.startswith("test"):
            continue
        catalog.append(_extract_ast_meta(p))
    return catalog


def _build_agent_catalog() -> list[dict]:
    try:
        adir = _agents_dir()
    except FileNotFoundError:
        return []
    catalog = []
    for p in sorted(adir.glob("*.py")):
        if p.name == "__init__.py" or p.name.startswith("test"):
            continue
        meta = _extract_ast_meta(p)
        # Add FSM state info
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [
                        ast.unparse(b) if hasattr(ast, "unparse") else ""
                        for b in node.bases
                    ]
                    if any("Enum" in b for b in bases):
                        states = []
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for t in item.targets:
                                    if isinstance(t, ast.Name):
                                        states.append(t.id)
                        meta.setdefault("states", []).extend(states)
        except Exception:
            pass
        catalog.append(meta)
    return catalog


def _build_workflow_catalog() -> list[dict]:
    catalog = []
    for yaml_dir, cat_type in [
        (_pipeline_examples_dir(), "pipeline"),
        (_workflow_dir(), "workflow"),
    ]:
        try:
            if not yaml_dir.is_dir():
                continue
            for p in sorted(yaml_dir.glob("*.yaml")):
                try:
                    content = p.read_text(encoding="utf-8")
                except Exception:
                    content = ""
                catalog.append(
                    {
                        "type": cat_type,
                        "name": p.stem,
                        "file": str(p),
                        "content_preview": content[:500],
                    }
                )
        except FileNotFoundError:
            pass
    return catalog


def _build_signatures_catalog() -> list[dict]:
    """Return all DSPy Signature class definitions found across modules."""
    try:
        mdir = _modules_dir()
    except FileNotFoundError:
        return []
    sigs = []
    for p in sorted(mdir.glob("*.py")):
        if p.name == "__init__.py" or p.name.startswith("test"):
            continue
        meta = _extract_ast_meta(p)
        for sig_name in meta["signatures"]:
            sigs.append(
                {
                    "module": meta["name"],
                    "signature_class": sig_name,
                    "docstring": meta["docstring"][:200],
                    "input_fields": meta["input_fields"],
                    "output_fields": meta["output_fields"],
                }
            )
    return sigs


# ---------------------------------------------------------------------------
# Resource registration
# ---------------------------------------------------------------------------

_RESOURCES = [
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


def register_resources(server: Server) -> None:
    """Register dspygen catalog as MCP resources on *server*."""

    @server.list_resources()
    async def list_resources() -> list[types.Resource]:
        return _RESOURCES

    @server.read_resource()
    async def read_resource(uri: str) -> str:  # type: ignore[return]
        try:
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
