"""
dspygen MCP prompt library.

Provides an expanded set of MCP Prompts covering:
  - domain_prompts: DDD/RDDDY design prompts
  - module_prompts: DSPy module generation and optimization prompts
  - workflow_prompts: Pipeline/workflow design prompts
"""

from __future__ import annotations

from mcp import types

from dspygen.mcp.prompts.domain_prompts import (
    DOMAIN_PROMPTS,
    DOMAIN_RENDERERS,
)
from dspygen.mcp.prompts.module_prompts import (
    MODULE_PROMPTS,
    MODULE_RENDERERS,
)
from dspygen.mcp.prompts.workflow_prompts import (
    WORKFLOW_PROMPTS,
    WORKFLOW_RENDERERS,
)

__all__ = [
    "ALL_PROMPTS",
    "ALL_RENDERERS",
    "get_all_prompts",
    "render_prompt",
]

ALL_PROMPTS: list[types.Prompt] = DOMAIN_PROMPTS + MODULE_PROMPTS + WORKFLOW_PROMPTS

ALL_RENDERERS: dict = {**DOMAIN_RENDERERS, **MODULE_RENDERERS, **WORKFLOW_RENDERERS}


def get_all_prompts() -> list[types.Prompt]:
    """Return all MCP Prompt descriptors from all prompt modules."""
    return ALL_PROMPTS


def render_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Render a prompt by name.

    Returns a GetPromptResult or raises ValueError if unknown.
    """
    renderer = ALL_RENDERERS.get(name)
    if renderer is None:
        raise ValueError(f"Unknown prompt: {name!r}")

    messages = renderer(arguments or {})
    prompt_obj = next((p for p in ALL_PROMPTS if p.name == name), None)
    description = prompt_obj.description if prompt_obj else ""
    return types.GetPromptResult(description=description, messages=messages)
