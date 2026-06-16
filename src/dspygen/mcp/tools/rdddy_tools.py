"""
MCP tools for the dspygen RDDDY (Reactive Domain-Driven Design for You) pattern system.

Exposes the full RDDDY pattern system: aggregates, commands, events, queries,
sagas, policies, value objects, read models, event storms, and inhabitants.

All imports of dspygen internals are lazy (inside handlers) to avoid startup failures.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from typing import Any

from loguru import logger
from mcp import types

__all__ = ["get_tool_definitions", "handle_tool"]

# ---------------------------------------------------------------------------
# Response helpers
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


# ---------------------------------------------------------------------------
# RDDDY pattern descriptions
# ---------------------------------------------------------------------------

_RDDDY_PATTERNS = {
    "aggregate": {
        "description": "Domain aggregate root — encapsulates cluster of domain objects treated as single unit. "
                       "Enforces invariants. Extends BaseAggregate.",
        "base_class": "BaseAggregate",
        "import": "from dspygen.rdddy.base_aggregate import BaseAggregate",
    },
    "command": {
        "description": "Domain command — intent to change system state. Extends BaseCommand.",
        "base_class": "BaseCommand",
        "import": "from dspygen.rdddy.base_command import BaseCommand",
    },
    "event": {
        "description": "Domain event — something that happened in the domain. Extends BaseEvent.",
        "base_class": "BaseEvent",
        "import": "from dspygen.rdddy.base_event import BaseEvent",
    },
    "query": {
        "description": "Domain query — request for information without side effects. Extends BaseQuery.",
        "base_class": "BaseQuery",
        "import": "from dspygen.rdddy.base_query import BaseQuery",
    },
    "saga": {
        "description": "Saga orchestration — long-running business process coordinating multiple aggregates. "
                       "Extends BaseSaga.",
        "base_class": "BaseSaga",
        "import": "from dspygen.rdddy.base_saga import BaseSaga",
    },
    "policy": {
        "description": "Domain policy — business rule reacting to events and issuing commands. Extends BasePolicy.",
        "base_class": "BasePolicy",
        "import": "from dspygen.rdddy.base_policy import BasePolicy",
    },
    "value_object": {
        "description": "Value object — immutable domain concept defined by its attributes. Extends BaseValueObject.",
        "base_class": "BaseValueObject",
        "import": "from dspygen.rdddy.base_value_object import BaseValueObject",
    },
    "read_model": {
        "description": "Read model — denormalized view optimized for querying. Extends BaseReadModel.",
        "base_class": "BaseReadModel",
        "import": "from dspygen.rdddy.base_read_model import BaseReadModel",
    },
    "inhabitant": {
        "description": "ServiceColony inhabitant — actor participating in service colony. Extends BaseInhabitant.",
        "base_class": "BaseInhabitant",
        "import": "from dspygen.rdddy.base_inhabitant import BaseInhabitant",
    },
}


# ---------------------------------------------------------------------------
# Code generation helpers
# ---------------------------------------------------------------------------

def _to_pascal(name: str) -> str:
    return "".join(w.capitalize() for w in name.replace("-", "_").split("_"))


def _generate_class_code(
    pattern: str,
    name: str,
    description: str,
    fields: list[dict] | None = None,
) -> str:
    """Generate Python class code for a RDDDY pattern."""
    info = _RDDDY_PATTERNS.get(pattern, {})
    base_class = info.get("base_class", "BaseMessage")
    import_stmt = info.get("import", "from dspygen.rdddy.base_message import BaseMessage")
    pascal_name = _to_pascal(name)

    field_lines = ""
    pydantic_import = ""
    if fields:
        pydantic_import = "\nfrom pydantic import Field\n"
        field_lines = "\n"
        for f in fields:
            fname = f.get("name", "field")
            ftype = f.get("type", "str")
            fdesc = f.get("description", "")
            field_lines += f"    {fname}: {ftype} = Field(..., description={fdesc!r})\n"

    default_doc = f"{pascal_name} — {pattern.replace('_', ' ')} domain class."
    docstring = description or default_doc
    pass_or_fields = field_lines if field_lines else "    pass\n"
    code = (
        f"{import_stmt}{pydantic_import}\n\n"
        f"class {pascal_name}(_{base_class}_):\n"
        f'    """{docstring}\n\n'
        f"    Generated by dspygen MCP RDDDY tools.\n"
        f'    """\n'
        + pass_or_fields
    )
    # Fix placeholder base class names
    code = code.replace(f"_{base_class}_", base_class)
    return code


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------

_TOOL_NAMES = {
    "create_aggregate",
    "create_command",
    "create_event",
    "create_query",
    "create_saga",
    "create_policy",
    "create_value_object",
    "create_read_model",
    "event_storm",
    "create_inhabitant",
    "list_rdddy_patterns",
    "scaffold_domain",
}


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all RDDDY tools."""
    _field_schema = {
        "type": "array",
        "description": "Optional list of field definitions [{name, type, description}]",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "type": {"type": "string", "default": "str"},
                "description": {"type": "string"},
            },
        },
        "default": [],
    }
    _name_prop = {
        "name": {"type": "string", "description": "Class name in snake_case or PascalCase"},
        "description": {"type": "string", "description": "Short description of the class purpose"},
        "fields": _field_schema,
    }

    def _cls_tool(tool_name: str, pattern: str, desc_suffix: str) -> types.Tool:
        return types.Tool(
            name=tool_name,
            description=f"Generate a RDDDY domain {pattern.replace('_', ' ')} class. {desc_suffix}",
            inputSchema={
                "type": "object",
                "properties": _name_prop,
                "required": ["name"],
            },
        )

    return [
        _cls_tool(
            "create_aggregate",
            "aggregate",
            "Returns Python source code for a BaseAggregate subclass implementing the domain aggregate root pattern.",
        ),
        _cls_tool(
            "create_command",
            "command",
            "Returns Python source code for a BaseCommand subclass representing intent to change domain state.",
        ),
        _cls_tool(
            "create_event",
            "event",
            "Returns Python source code for a BaseEvent subclass representing something that happened in the domain.",
        ),
        _cls_tool(
            "create_query",
            "query",
            "Returns Python source code for a BaseQuery subclass representing an information request.",
        ),
        _cls_tool(
            "create_saga",
            "saga",
            "Returns Python source code for a BaseSaga subclass orchestrating a long-running business process.",
        ),
        _cls_tool(
            "create_policy",
            "policy",
            "Returns Python source code for a BasePolicy subclass implementing a domain business rule.",
        ),
        _cls_tool(
            "create_value_object",
            "value_object",
            "Returns Python source code for a BaseValueObject subclass representing an immutable domain concept.",
        ),
        _cls_tool(
            "create_read_model",
            "read_model",
            "Returns Python source code for a BaseReadModel subclass — a denormalized read-optimized view.",
        ),
        types.Tool(
            name="event_storm",
            description=(
                "Given a domain description, generate a full Event Storm model using EventStormingDomainSpecificationModel. "
                "Identifies domain events, commands, aggregates, policies, and read models."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "domain_description": {
                        "type": "string",
                        "description": "High-level description of the business domain to model",
                    },
                    "bounded_context": {
                        "type": "string",
                        "description": "Optional bounded context name",
                        "default": "",
                    },
                },
                "required": ["domain_description"],
            },
        ),
        types.Tool(
            name="create_inhabitant",
            description=(
                "Create a ServiceColony inhabitant class — an actor that participates in the "
                "RDDDY service colony, processing messages and coordinating with other inhabitants."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Inhabitant class name"},
                    "description": {"type": "string", "description": "Description of this inhabitant's role"},
                    "handles": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of message types this inhabitant handles",
                        "default": [],
                    },
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="list_rdddy_patterns",
            description=(
                "List all available RDDDY patterns with their descriptions, base classes, and usage guidance. "
                "Useful for understanding the RDDDY framework before generating code."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="scaffold_domain",
            description=(
                "Given a domain name and description, scaffold ALL RDDDY classes in one call: "
                "aggregate root + commands + events + queries + saga + policy. "
                "Returns a complete domain skeleton as a dict of {class_type: python_code}."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "domain_name": {
                        "type": "string",
                        "description": "Domain name in snake_case, e.g. 'order_management'",
                    },
                    "description": {
                        "type": "string",
                        "description": "Brief description of the domain",
                        "default": "",
                    },
                    "operations": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Key operations, e.g. ['create', 'update', 'cancel']",
                        "default": ["create", "update", "delete"],
                    },
                },
                "required": ["domain_name"],
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

    dispatch = {
        "create_aggregate": (_create_class, "aggregate"),
        "create_command": (_create_class, "command"),
        "create_event": (_create_class, "event"),
        "create_query": (_create_class, "query"),
        "create_saga": (_create_class, "saga"),
        "create_policy": (_create_class, "policy"),
        "create_value_object": (_create_class, "value_object"),
        "create_read_model": (_create_class, "read_model"),
    }

    if name in dispatch:
        fn, pattern = dispatch[name]
        return await fn(arguments, pattern)
    if name == "event_storm":
        return await _event_storm(arguments)
    if name == "create_inhabitant":
        return await _create_inhabitant(arguments)
    if name == "list_rdddy_patterns":
        return await _list_rdddy_patterns(arguments)
    if name == "scaffold_domain":
        return await _scaffold_domain(arguments)

    return _err(f"Unhandled tool: {name}")


async def _create_class(args: dict, pattern: str) -> list[types.TextContent]:
    name: str = (args or {}).get("name", "")
    description: str = (args or {}).get("description", "")
    fields: list = (args or {}).get("fields", [])
    if not name:
        return _err("name argument is required")
    try:
        code = _generate_class_code(pattern, name, description, fields if fields else None)
        pascal_name = _to_pascal(name)
        info = _RDDDY_PATTERNS.get(pattern, {})
        return _ok({
            "pattern": pattern,
            "class_name": pascal_name,
            "base_class": info.get("base_class", ""),
            "code": code,
            "file_name_suggestion": f"{name.lower().rstrip('_module')}_{pattern}.py",
        })
    except Exception as exc:
        logger.exception(f"create_{pattern} error")
        return _err(f"create_{pattern} failed: {exc}")


async def _event_storm(args: dict) -> list[types.TextContent]:
    domain_description: str = (args or {}).get("domain_description", "")
    bounded_context: str = (args or {}).get("bounded_context", "")
    if not domain_description:
        return _err("domain_description argument is required")
    try:
        # Return a structured event storm analysis without requiring dspy to be configured
        domain_words = domain_description.lower().split()
        context_prefix = f"{bounded_context} " if bounded_context else ""

        # Generate plausible event storm artifacts from description keywords
        nouns = [w.capitalize() for w in domain_words if len(w) > 4 and not w.startswith("the")][:5]
        if not nouns:
            nouns = ["Entity", "Resource", "Item"]

        entity = nouns[0] if nouns else "Entity"

        result = {
            "bounded_context": bounded_context or domain_words[0].capitalize() + "Context",
            "domain_description": domain_description,
            "domain_events": [
                f"{entity}Created",
                f"{entity}Updated",
                f"{entity}Deleted",
                f"{entity}StateChanged",
                f"{entity}ProcessCompleted",
            ],
            "commands": [
                f"Create{entity}",
                f"Update{entity}",
                f"Delete{entity}",
                f"Process{entity}",
            ],
            "aggregates": [
                f"{entity}Aggregate",
            ],
            "policies": [
                f"{entity}ValidationPolicy",
                f"{entity}NotificationPolicy",
            ],
            "read_models": [
                f"{entity}ListView",
                f"{entity}DetailView",
            ],
            "sagas": [
                f"{entity}ProcessSaga",
            ],
            "note": (
                "This is a template event storm. For AI-generated models, configure dspy "
                "and call the EventStormingDomainSpecificationModel directly."
            ),
        }

        # Try to use the actual EventStormingDomainSpecificationModel if dspy is available
        try:
            import dspy

            from dspygen.modules.gen_pydantic_instance import GenPydanticInstance
            from dspygen.rdddy.event_storm_model import EventStormingDomainSpecificationModel
            if dspy.settings.lm is not None:
                gen = GenPydanticInstance(model=EventStormingDomainSpecificationModel)
                inst = gen.forward(domain_description)
                result["ai_generated_events"] = [
                    e.model_dump() if hasattr(e, "model_dump") else str(e)
                    for e in (inst.domain_events or [])
                ]
                result["note"] = "AI-generated event storm from EventStormingDomainSpecificationModel."
        except Exception as inner_exc:
            logger.debug(f"Could not run AI event storm: {inner_exc}")

        return _ok(result)
    except Exception as exc:
        logger.exception("event_storm error")
        return _err(f"event_storm failed: {exc}")


async def _create_inhabitant(args: dict) -> list[types.TextContent]:
    name: str = (args or {}).get("name", "")
    description: str = (args or {}).get("description", "")
    handles: list = (args or {}).get("handles", [])
    if not name:
        return _err("name argument is required")
    try:
        pascal_name = _to_pascal(name)
        handles_lines = ""
        if handles:
            handles_lines = "\n    async def process_message(self, message):\n"
            for h in handles:
                handles_lines += f"        # Handle {h}\n"
                handles_lines += f"        if isinstance(message, {h}):\n"
                handles_lines += "            pass  # TODO: implement handler\n"

        code = textwrap.dedent(f"""\
            from dspygen.rdddy.base_inhabitant import BaseInhabitant


            class {pascal_name}(BaseInhabitant):
                \"\"\"{description or f"{pascal_name} — ServiceColony inhabitant."}

                Handles: {', '.join(handles) if handles else 'general messages'}

                Generated by dspygen MCP RDDDY tools.
                \"\"\"
            {handles_lines or '    pass'}
        """)
        return _ok({
            "class_name": pascal_name,
            "code": code,
            "handles": handles,
            "file_name_suggestion": f"{name.lower()}_inhabitant.py",
        })
    except Exception as exc:
        logger.exception("create_inhabitant error")
        return _err(f"create_inhabitant failed: {exc}")


async def _list_rdddy_patterns(_args: dict) -> list[types.TextContent]:
    try:
        result = []
        for pattern_name, info in _RDDDY_PATTERNS.items():
            result.append({
                "pattern": pattern_name,
                "description": info["description"],
                "base_class": info["base_class"],
                "import": info["import"],
                "mcp_tool": f"create_{pattern_name}",
            })
        result.append({
            "pattern": "event_storm",
            "description": "Full Event Storm modeling — generates all domain artifacts from a description.",
            "base_class": "EventStormingDomainSpecificationModel",
            "import": "from dspygen.rdddy.event_storm_model import EventStormingDomainSpecificationModel",
            "mcp_tool": "event_storm",
        })
        result.append({
            "pattern": "scaffold_domain",
            "description": "One-shot scaffold of all RDDDY classes for a domain.",
            "base_class": "multiple",
            "import": "dspygen.rdddy.*",
            "mcp_tool": "scaffold_domain",
        })
        return _ok(result)
    except Exception as exc:
        return _err(f"list_rdddy_patterns failed: {exc}")


async def _scaffold_domain(args: dict) -> list[types.TextContent]:
    domain_name: str = (args or {}).get("domain_name", "")
    description: str = (args or {}).get("description", "")
    operations: list = (args or {}).get("operations", ["create", "update", "delete"])
    if not domain_name:
        return _err("domain_name argument is required")
    try:
        pascal = _to_pascal(domain_name)
        desc = description or f"{pascal} domain"

        scaffold: dict[str, str] = {}

        # Aggregate
        scaffold["aggregate"] = _generate_class_code(
            "aggregate", f"{domain_name}_aggregate", f"{pascal} aggregate root. {desc}"
        )

        # Commands (one per operation)
        for op in operations:
            key = f"command_{op}"
            scaffold[key] = _generate_class_code(
                "command",
                f"{op}_{domain_name}",
                f"Command to {op} a {pascal}.",
                [{"name": f"{domain_name}_id", "type": "str", "description": f"ID of the {pascal}"}],
            )

        # Events (one per operation)
        for op in operations:
            past = op.rstrip("e") + "ed"
            key = f"event_{op}"
            scaffold[key] = _generate_class_code(
                "event",
                f"{domain_name}_{past}",
                f"Event raised when a {pascal} is {past}.",
                [{"name": f"{domain_name}_id", "type": "str", "description": f"ID of the {pascal}"}],
            )

        # Query
        scaffold["query"] = _generate_class_code(
            "query",
            f"get_{domain_name}_by_id",
            f"Query to retrieve a {pascal} by its ID.",
            [{"name": f"{domain_name}_id", "type": "str", "description": f"ID of the {pascal} to retrieve"}],
        )

        # Saga
        scaffold["saga"] = _generate_class_code(
            "saga",
            f"{domain_name}_process_saga",
            f"Saga orchestrating the {pascal} lifecycle process.",
        )

        # Policy
        scaffold["policy"] = _generate_class_code(
            "policy",
            f"{domain_name}_validation_policy",
            f"Policy enforcing business rules for {pascal} operations.",
        )

        # Read model
        scaffold["read_model"] = _generate_class_code(
            "read_model",
            f"{domain_name}_view",
            f"Read model view for {pascal} data.",
            [
                {"name": f"{domain_name}_id", "type": "str", "description": "Primary identifier"},
                {"name": "status", "type": "str", "description": "Current status"},
            ],
        )

        return _ok({
            "domain_name": domain_name,
            "pascal_name": pascal,
            "description": desc,
            "operations": operations,
            "classes_generated": list(scaffold.keys()),
            "code": scaffold,
        })
    except Exception as exc:
        logger.exception("scaffold_domain error")
        return _err(f"scaffold_domain failed: {exc}")
