"""
MCP Prompt library — Pipeline/Workflow design prompts.

5 prompts covering dspygen pipeline/workflow design, debugging, DSL conversion,
optimization, and test generation.
"""

from __future__ import annotations

import mcp.types as types

__all__ = ["WORKFLOW_PROMPTS", "WORKFLOW_RENDERERS"]


def _msg(text: str) -> list[types.PromptMessage]:
    return [types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))]


# ---------------------------------------------------------------------------
# Prompt: design-workflow
# ---------------------------------------------------------------------------

_DESIGN_WORKFLOW = types.Prompt(
    name="design-workflow",
    description=(
        "Design a dspygen DSL pipeline/workflow from a high-level goal. "
        "Produces a YAML DSL definition and Python equivalent."
    ),
    arguments=[
        types.PromptArgument(name="workflow_goal", description="What should this workflow accomplish?", required=True),
        types.PromptArgument(name="input_data", description="What data does the workflow receive as input?", required=True),
        types.PromptArgument(name="expected_output", description="What should the workflow produce?", required=True),
        types.PromptArgument(name="available_modules", description="Comma-separated list of available dspygen modules to use", required=False),
    ],
)


def _render_design_workflow(args: dict) -> list[types.PromptMessage]:
    goal = args.get("workflow_goal", "")
    input_data = args.get("input_data", "")
    output = args.get("expected_output", "")
    modules = args.get("available_modules", "")
    text = (
        "You are an expert dspygen pipeline architect.\n\n"
        f"Design a complete workflow for: **{goal}**\n\n"
        f"**Input:** {input_data}\n"
        f"**Expected output:** {output}\n"
        + (f"**Available modules:** {modules}\n" if modules else "")
        + "\n"
        "Produce:\n\n"
        "1. **Workflow YAML** in dspygen DSL format:\n"
        "```yaml\n"
        "pipeline:\n"
        "  - name: step_name\n"
        "    module: module_name\n"
        "    args:\n"
        "      key: value\n"
        "```\n\n"
        "2. **Step-by-step explanation** of what each pipeline step does\n"
        "3. **Data flow diagram** (Mermaid flowchart)\n"
        "4. **Python equivalent** using dspy.Module composition\n"
        "5. **Error handling** — what happens if a step fails\n"
        "6. **Optimization suggestions** — which steps could be parallelized\n\n"
        "Base the design on available dspygen modules or suggest creating new ones."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: debug-pipeline
# ---------------------------------------------------------------------------

_DEBUG_PIPELINE = types.Prompt(
    name="debug-pipeline",
    description=(
        "Debug a failing dspygen DSL pipeline. "
        "Paste the pipeline YAML and the error message."
    ),
    arguments=[
        types.PromptArgument(name="pipeline_yaml", description="The YAML content of the failing pipeline", required=True),
        types.PromptArgument(name="error_message", description="The error or unexpected output observed", required=True),
        types.PromptArgument(name="input_sample", description="Sample input data that triggers the error", required=False),
    ],
)


def _render_debug_pipeline(args: dict) -> list[types.PromptMessage]:
    yaml_content = args.get("pipeline_yaml", "")
    error = args.get("error_message", "")
    sample = args.get("input_sample", "")
    text = (
        "You are an expert in the dspygen DSL pipeline system.\n\n"
        "Debug this failing pipeline:\n\n"
        f"```yaml\n{yaml_content}\n```\n\n"
        f"**Error observed:**\n```\n{error}\n```\n"
        + (f"\n**Sample input:**\n```\n{sample}\n```\n" if sample else "")
        + "\n"
        "Diagnose:\n"
        "1. **Root cause** — identify the exact failure point\n"
        "2. **DSL concepts** — explain the dspygen DSL concepts involved\n"
        "3. **Corrected YAML** — provide a fixed version\n"
        "4. **Prevention** — how to validate pipelines before running\n"
        "5. **Testing approach** — how to write a test for this pipeline\n"
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: convert-to-yaml-dsl
# ---------------------------------------------------------------------------

_CONVERT_TO_YAML_DSL = types.Prompt(
    name="convert-to-yaml-dsl",
    description="Convert a Python dspygen pipeline script into the dspygen YAML DSL format.",
    arguments=[
        types.PromptArgument(name="python_code", description="Python code using dspygen modules", required=True),
        types.PromptArgument(name="pipeline_name", description="Name for the resulting YAML pipeline", required=False),
    ],
)


def _render_convert_to_yaml_dsl(args: dict) -> list[types.PromptMessage]:
    code = args.get("python_code", "")
    name = args.get("pipeline_name", "converted_pipeline")
    text = (
        "You are an expert in the dspygen DSL pipeline system.\n\n"
        f"Convert this Python pipeline to the dspygen YAML DSL format:\n\n"
        f"```python\n{code}\n```\n\n"
        f"**Pipeline name:** {name}\n\n"
        "Produce:\n"
        "1. **Complete YAML pipeline** — ready to run with `dspygen pipeline run`\n"
        "2. **Mapping explanation** — how each Python construct maps to YAML\n"
        "3. **Validation checklist** — verify the YAML is syntactically correct\n"
        "4. **Limitations** — note any Python-specific logic that cannot be expressed in YAML\n\n"
        "The YAML DSL format uses:\n"
        "```yaml\n"
        "pipeline:\n"
        "  - name: step_name\n"
        "    module: module_path\n"
        "    args: {key: value}\n"
        "    output_key: result_name\n"
        "```"
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: optimize-pipeline
# ---------------------------------------------------------------------------

_OPTIMIZE_PIPELINE = types.Prompt(
    name="optimize-pipeline",
    description="Analyze and optimize a dspygen pipeline for speed, cost, and quality.",
    arguments=[
        types.PromptArgument(name="pipeline_yaml", description="Current pipeline YAML", required=True),
        types.PromptArgument(name="bottleneck", description="Known bottleneck or performance concern", required=False),
        types.PromptArgument(name="optimization_goal", description="Primary goal: speed, cost, quality, or balanced", required=False),
    ],
)


def _render_optimize_pipeline(args: dict) -> list[types.PromptMessage]:
    yaml_content = args.get("pipeline_yaml", "")
    bottleneck = args.get("bottleneck", "")
    goal = args.get("optimization_goal", "balanced")
    text = (
        "You are a dspygen pipeline optimization expert.\n\n"
        f"Optimize this pipeline for **{goal}**:\n\n"
        f"```yaml\n{yaml_content}\n```\n\n"
        + (f"**Known bottleneck:** {bottleneck}\n" if bottleneck else "")
        + "\n"
        "Analyze and provide:\n"
        "1. **Performance analysis** — identify slow/expensive steps\n"
        "2. **Parallelization opportunities** — steps that can run concurrently\n"
        "3. **Caching strategy** — which outputs should be cached\n"
        "4. **Model downgrades** — steps where a smaller model suffices\n"
        "5. **Optimized YAML** — the improved pipeline definition\n"
        "6. **Expected improvements** — estimated speed/cost reduction\n"
        "7. **Monitoring** — what metrics to track in production\n"
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: generate-workflow-tests
# ---------------------------------------------------------------------------

_GENERATE_WORKFLOW_TESTS = types.Prompt(
    name="generate-workflow-tests",
    description="Generate integration tests for a dspygen pipeline/workflow.",
    arguments=[
        types.PromptArgument(name="pipeline_yaml", description="Pipeline YAML to test", required=True),
        types.PromptArgument(name="sample_inputs", description="JSON sample inputs for the pipeline", required=True),
        types.PromptArgument(name="expected_outputs", description="Expected output structure or values", required=False),
    ],
)


def _render_generate_workflow_tests(args: dict) -> list[types.PromptMessage]:
    yaml_content = args.get("pipeline_yaml", "")
    inputs = args.get("sample_inputs", "{}")
    expected = args.get("expected_outputs", "")
    text = (
        "You are an expert dspygen pipeline tester.\n\n"
        "Generate comprehensive tests for this pipeline:\n\n"
        f"```yaml\n{yaml_content}\n```\n\n"
        f"**Sample inputs:** `{inputs}`\n"
        + (f"**Expected outputs:** {expected}\n" if expected else "")
        + "\n"
        "Generate:\n"
        "1. **Unit tests** — test each pipeline step in isolation using `DummyLM`\n"
        "2. **Integration test** — run the full pipeline with mock LM\n"
        "3. **Contract test** — verify output schema matches expected\n"
        "4. **Golden test** — snapshot test to detect regressions\n"
        "5. **Error injection tests** — what happens when a step returns bad output\n"
        "6. **Performance test** — measure pipeline execution time\n"
        "7. **Fixtures** — reusable test data setup\n\n"
        "Return a complete `test_pipeline.py` pytest file."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

WORKFLOW_PROMPTS: list[types.Prompt] = [
    _DESIGN_WORKFLOW,
    _DEBUG_PIPELINE,
    _CONVERT_TO_YAML_DSL,
    _OPTIMIZE_PIPELINE,
    _GENERATE_WORKFLOW_TESTS,
]

WORKFLOW_RENDERERS: dict = {
    "design-workflow": _render_design_workflow,
    "debug-pipeline": _render_debug_pipeline,
    "convert-to-yaml-dsl": _render_convert_to_yaml_dsl,
    "optimize-pipeline": _render_optimize_pipeline,
    "generate-workflow-tests": _render_generate_workflow_tests,
}
