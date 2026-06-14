"""
MCP tools for dspygen agents.

Provides tools to list, inspect, and interact with dspygen FSM-based agents.
All dspygen imports are lazy to avoid startup failures.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

import mcp.types as types
from loguru import logger

__all__ = ["get_tool_definitions", "handle_tool"]

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _agents_dir() -> Path:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        agents_path = candidate / "dspygen" / "agents"
        if agents_path.is_dir():
            return agents_path
    raise FileNotFoundError("Could not locate dspygen/agents directory")


def _list_agent_files() -> list[Path]:
    try:
        adir = _agents_dir()
    except FileNotFoundError:
        return []
    return sorted(
        p for p in adir.glob("*.py")
        if p.name != "__init__.py" and not p.name.startswith("test")
    )


def _extract_agent_info(path: Path) -> dict[str, Any]:
    """Extract FSM state machine metadata from an agent file using AST."""
    info: dict[str, Any] = {
        "name": path.stem,
        "file": str(path),
        "docstring": "",
        "classes": [],
        "states": [],
        "transitions": [],
    }
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception as exc:
        info["error"] = str(exc)
        return info

    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
    ):
        info["docstring"] = tree.body[0].value.value.strip()

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [
            ast.unparse(b) if hasattr(ast, "unparse") else ""
            for b in node.bases
        ]
        is_enum = any("Enum" in b for b in bases)
        is_agent = any("FSMMixin" in b or "Agent" in node.name for b in bases)

        class_info: dict[str, Any] = {
            "class_name": node.name,
            "docstring": ast.get_docstring(node) or "",
            "bases": bases,
            "is_state_enum": is_enum,
            "is_agent": is_agent,
        }

        if is_enum:
            states = []
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for t in item.targets:
                        if isinstance(t, ast.Name):
                            states.append(t.id)
            class_info["states"] = states
            info["states"].extend(states)

        if is_agent:
            transitions = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    for dec in item.decorator_list:
                        dec_name = ""
                        if isinstance(dec, ast.Name):
                            dec_name = dec.id
                        elif isinstance(dec, ast.Call):
                            if isinstance(dec.func, ast.Name):
                                dec_name = dec.func.id
                            elif isinstance(dec.func, ast.Attribute):
                                dec_name = dec.func.attr
                        if dec_name == "trigger":
                            transitions.append(
                                {
                                    "method": item.name,
                                    "docstring": ast.get_docstring(item) or "",
                                }
                            )
            class_info["transitions"] = transitions
            info["transitions"].extend(transitions)

        info["classes"].append(class_info)

    return info


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
    "list_agents",
    "get_agent_info",
    "create_coder_agent",
    "create_research_agent",
}


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all agent tools."""
    return [
        types.Tool(
            name="list_agents",
            description=(
                "List all available dspygen FSM-based agents. "
                "Returns names, state machine states, and number of transitions."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_agent_info",
            description=(
                "Get detailed FSM state machine information for a specific dspygen agent, "
                "including all states and trigger-decorated transition methods."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "Agent file stem, e.g. 'coder_agent'",
                    }
                },
                "required": ["agent_name"],
            },
        ),
        types.Tool(
            name="create_coder_agent",
            description=(
                "Create and run a CoderAgent through its happy-path FSM transitions "
                "(ANALYZING_REQUIREMENTS -> WRITING_CODE -> TESTING_CODE -> COMPLETING_TASK)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "Description of the coding task to perform",
                        "default": "implement a Python function",
                    }
                },
                "required": [],
            },
        ),
        types.Tool(
            name="create_research_agent",
            description=(
                "Create a LearningAgent (research agent) with the given list of research objectives. "
                "The agent uses DuckDuckGo search, URL scraping, and DSPy modules to gather information."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "objectives": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of research topics or learning objectives",
                    }
                },
                "required": ["objectives"],
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

    if name == "list_agents":
        return await _list_agents(arguments)
    if name == "get_agent_info":
        return await _get_agent_info(arguments)
    if name == "create_coder_agent":
        return await _create_coder_agent(arguments)
    if name == "create_research_agent":
        return await _create_research_agent(arguments)

    return _err(f"Unhandled tool: {name}")


async def _list_agents(args: dict) -> list[types.TextContent]:
    try:
        files = _list_agent_files()
        result = []
        for path in files:
            info = _extract_agent_info(path)
            result.append(
                {
                    "name": info["name"],
                    "docstring": info["docstring"][:200],
                    "states": info["states"],
                    "num_transitions": len(info["transitions"]),
                }
            )
        return _ok(result)
    except Exception as exc:
        return _err(f"list_agents failed: {exc}")


async def _get_agent_info(args: dict) -> list[types.TextContent]:
    agent_name: str = (args or {}).get("agent_name", "")
    if not agent_name:
        return _err("agent_name argument is required")
    try:
        files = _list_agent_files()
        matches = [p for p in files if p.stem == agent_name]
        if not matches:
            return _err(f"Agent '{agent_name}' not found")
        info = _extract_agent_info(matches[0])
        return _ok(info)
    except Exception as exc:
        return _err(f"get_agent_info failed: {exc}")


async def _create_coder_agent(args: dict) -> list[types.TextContent]:
    task_description: str = (args or {}).get(
        "task_description", "implement a Python function"
    )
    try:
        src_dir = str(Path(__file__).resolve().parents[4])
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.agents.coder_agent import CoderAgent  # lazy

        agent = CoderAgent()
        initial_state = (
            agent.state.name if hasattr(agent.state, "name") else str(agent.state)
        )

        transitions_taken = []
        agent.start_coding()
        transitions_taken.append("start_coding -> WRITING_CODE")
        agent.test_code()
        transitions_taken.append("test_code -> TESTING_CODE")
        agent.complete_task()
        transitions_taken.append("complete_task -> COMPLETING_TASK")

        final_state = (
            agent.state.name if hasattr(agent.state, "name") else str(agent.state)
        )

        return _ok(
            {
                "task_description": task_description,
                "initial_state": initial_state,
                "final_state": final_state,
                "transitions_taken": transitions_taken,
                "status": "completed",
            }
        )
    except Exception as exc:
        logger.exception("create_coder_agent error")
        return _err(f"create_coder_agent failed: {exc}")


async def _create_research_agent(args: dict) -> list[types.TextContent]:
    objectives: list[str] = (args or {}).get("objectives", [])
    if not objectives:
        return _err("objectives argument is required (list of research topics)")
    try:
        src_dir = str(Path(__file__).resolve().parents[4])
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.agents.research_agent import LearningAgent  # lazy

        agent = LearningAgent(objectives)
        initial_state = (
            agent.state.name if hasattr(agent.state, "name") else str(agent.state)
        )

        return _ok(
            {
                "objectives": objectives,
                "initial_state": initial_state,
                "status": "agent_created",
                "message": (
                    "LearningAgent created in state INPUT_OBJECTIVES. "
                    "Call agent.process_input() then agent.generate_queries() "
                    "to proceed through the research workflow."
                ),
            }
        )
    except Exception as exc:
        logger.exception("create_research_agent error")
        return _err(f"create_research_agent failed: {exc}")
