"""
MCP Prompt library — DSPy module generation and optimization prompts.

10 prompts covering module creation, optimization, debugging, testing, and chaining.
"""

from __future__ import annotations

import mcp.types as types

__all__ = ["MODULE_PROMPTS", "MODULE_RENDERERS"]


def _msg(text: str) -> list[types.PromptMessage]:
    return [types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))]


# ---------------------------------------------------------------------------
# Prompt: generate-module (re-export with enhancement)
# ---------------------------------------------------------------------------

_GENERATE_MODULE = types.Prompt(
    name="generate-module",
    description=(
        "Generate a complete dspygen DSPy module from a purpose and I/O spec. "
        "Includes Signature, Module, call function, and Typer CLI."
    ),
    arguments=[
        types.PromptArgument(name="module_purpose", description="What should the module do?", required=True),
        types.PromptArgument(name="inputs", description="Comma-separated input field names", required=True),
        types.PromptArgument(name="outputs", description="Comma-separated output field names", required=True),
        types.PromptArgument(name="predictor", description="Predictor type: Predict, ChainOfThought, ProgramOfThought", required=False),
    ],
)


def _render_generate_module(args: dict) -> list[types.PromptMessage]:
    purpose = args.get("module_purpose", "")
    inputs = args.get("inputs", "")
    outputs = args.get("outputs", "")
    predictor = args.get("predictor", "ChainOfThought")
    text = (
        "You are an expert DSPy developer working with the dspygen framework.\n\n"
        "Generate a complete dspygen DSPy module:\n\n"
        f"**Purpose:** {purpose}\n"
        f"**Input fields:** {inputs}\n"
        f"**Output fields:** {outputs}\n"
        f"**Preferred predictor:** {predictor}\n\n"
        "Requirements:\n"
        "1. Define `class <Name>Signature(dspy.Signature)` with descriptive docstring\n"
        "2. Assign `dspy.InputField(desc=...)` for each input\n"
        "3. Assign `dspy.OutputField(desc=...)` for each output\n"
        "4. Define `class <Name>Module(dspy.Module)` using the specified predictor\n"
        "5. Add `<name>_call(**kwargs)` convenience function\n"
        "6. Add Typer CLI `app = typer.Typer()` with a `call` command\n"
        "7. Add `if __name__ == '__main__': app()` entrypoint\n"
        "8. Follow naming: file as `<snake_case>_module.py`\n\n"
        "Return only complete Python source code. No explanations."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: create-signature
# ---------------------------------------------------------------------------

_CREATE_SIGNATURE = types.Prompt(
    name="create-signature",
    description="Generate a DSPy Signature class from a natural-language task description.",
    arguments=[
        types.PromptArgument(name="task_description", description="What task does the signature perform?", required=True),
        types.PromptArgument(name="example_input", description="Example input value", required=False),
        types.PromptArgument(name="example_output", description="Example output value", required=False),
    ],
)


def _render_create_signature(args: dict) -> list[types.PromptMessage]:
    task = args.get("task_description", "")
    ex_in = args.get("example_input", "")
    ex_out = args.get("example_output", "")
    text = (
        "You are an expert DSPy developer.\n\n"
        f"Create a DSPy Signature class for: **{task}**\n\n"
        + (f"**Example input:** {ex_in}\n" if ex_in else "")
        + (f"**Example output:** {ex_out}\n" if ex_out else "")
        + "\n"
        "Requirements:\n"
        "1. Choose a descriptive class name ending in `Signature`\n"
        "2. Write a clear docstring explaining the task\n"
        "3. Define `dspy.InputField(desc=...)` for each input with helpful descriptions\n"
        "4. Define `dspy.OutputField(desc=...)` for each output\n"
        "5. Recommend the best predictor: `Predict`, `ChainOfThought`, or `ProgramOfThought`\n"
        "6. Explain why that predictor is appropriate\n\n"
        "Return the signature class plus a brief usage example."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: optimize-module
# ---------------------------------------------------------------------------

_OPTIMIZE_MODULE = types.Prompt(
    name="optimize-module",
    description="Optimize a dspygen module using DSPy optimizers (BootstrapFewShot, MIPROv2).",
    arguments=[
        types.PromptArgument(name="module_name", description="Module name or class to optimize", required=True),
        types.PromptArgument(name="metric_description", description="What metric to optimize for?", required=True),
        types.PromptArgument(name="dataset_description", description="Training data description or examples", required=True),
    ],
)


def _render_optimize_module(args: dict) -> list[types.PromptMessage]:
    module = args.get("module_name", "")
    metric = args.get("metric_description", "")
    dataset = args.get("dataset_description", "")
    text = (
        "You are an expert DSPy optimization engineer.\n\n"
        f"Optimize the **{module}** dspygen module.\n\n"
        f"**Optimization metric:** {metric}\n"
        f"**Training data:** {dataset}\n\n"
        "Produce a complete optimization script:\n"
        "1. **Metric function** — Python callable returning a score 0.0–1.0\n"
        "2. **Dataset preparation** — convert examples to `dspy.Example` objects\n"
        "3. **BootstrapFewShot optimization** with the metric\n"
        "4. **MIPROv2 optimization** as an alternative\n"
        "5. **Evaluation code** — measure before/after performance\n"
        "6. **Save/load** — how to persist the optimized module\n\n"
        "Include a comparison table showing expected improvement.\n"
        "Return complete runnable Python code."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: debug-module
# ---------------------------------------------------------------------------

_DEBUG_MODULE = types.Prompt(
    name="debug-module",
    description="Debug a failing or underperforming dspygen module.",
    arguments=[
        types.PromptArgument(name="module_code", description="The module source code", required=True),
        types.PromptArgument(name="error_or_behavior", description="Error message or unexpected behavior observed", required=True),
        types.PromptArgument(name="sample_input", description="Sample input that triggers the issue", required=False),
    ],
)


def _render_debug_module(args: dict) -> list[types.PromptMessage]:
    code = args.get("module_code", "")
    error = args.get("error_or_behavior", "")
    sample = args.get("sample_input", "")
    text = (
        "You are an expert DSPy/dspygen debugging specialist.\n\n"
        "Debug this module:\n\n"
        f"```python\n{code}\n```\n\n"
        f"**Issue:** {error}\n"
        + (f"**Sample input:** `{sample}`\n" if sample else "")
        + "\n"
        "Diagnose:\n"
        "1. **Root cause** — identify the exact issue\n"
        "2. **DSPy concepts** — explain any DSPy/dspygen concepts involved\n"
        "3. **Fix** — provide corrected code\n"
        "4. **Prevention** — how to avoid this in future\n"
        "5. **Tests** — add assertions to catch regressions\n"
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: document-module
# ---------------------------------------------------------------------------

_DOCUMENT_MODULE = types.Prompt(
    name="document-module",
    description="Generate comprehensive documentation for a dspygen module.",
    arguments=[
        types.PromptArgument(name="module_code", description="The module source code", required=True),
        types.PromptArgument(name="doc_format", description="Documentation format: markdown, rst, google, numpy", required=False),
    ],
)


def _render_document_module(args: dict) -> list[types.PromptMessage]:
    code = args.get("module_code", "")
    fmt = args.get("doc_format", "markdown")
    text = (
        "You are a technical writer specializing in DSPy documentation.\n\n"
        f"Generate {fmt} documentation for:\n\n"
        f"```python\n{code}\n```\n\n"
        "Include:\n"
        "1. **Module overview** — what it does and when to use it\n"
        "2. **Signature documentation** — each input/output field explained\n"
        "3. **Usage examples** — 3+ real-world usage examples\n"
        "4. **Parameters reference** — all arguments with types and defaults\n"
        "5. **Return value** — what the module returns\n"
        "6. **Error conditions** — what can go wrong and how to handle it\n"
        "7. **Performance notes** — which model tier this works best with\n"
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: test-module
# ---------------------------------------------------------------------------

_TEST_MODULE = types.Prompt(
    name="test-module",
    description="Generate comprehensive pytest tests for a dspygen module.",
    arguments=[
        types.PromptArgument(name="module_code", description="The module source code", required=True),
        types.PromptArgument(name="test_scenarios", description="Comma-separated test scenarios to cover", required=False),
    ],
)


def _render_test_module(args: dict) -> list[types.PromptMessage]:
    code = args.get("module_code", "")
    scenarios = args.get("test_scenarios", "happy path, edge cases, error handling")
    text = (
        "You are an expert Python tester specializing in DSPy modules.\n\n"
        f"Generate comprehensive pytest tests for:\n\n"
        f"```python\n{code}\n```\n\n"
        f"**Test scenarios:** {scenarios}\n\n"
        "Generate:\n"
        "1. **Unit tests** with `dspy.utils.DummyLM` to avoid real LLM calls\n"
        "2. **Fixture** for the module instance\n"
        "3. **Happy path tests** — correct outputs for good inputs\n"
        "4. **Edge case tests** — empty inputs, long texts, special characters\n"
        "5. **Type validation tests** — correct Pydantic field types\n"
        "6. **Integration test sketch** — with a real LM (marked `@pytest.mark.integration`)\n"
        "7. **Parametrize** tests where applicable\n\n"
        "Return complete pytest file. Use `pytest-mock` for external dependencies."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: compose-pipeline
# ---------------------------------------------------------------------------

_COMPOSE_PIPELINE = types.Prompt(
    name="compose-pipeline",
    description="Compose multiple dspygen modules into a sequential processing pipeline.",
    arguments=[
        types.PromptArgument(name="goal", description="What the pipeline should accomplish end-to-end", required=True),
        types.PromptArgument(name="modules", description="Comma-separated list of module names to chain", required=True),
        types.PromptArgument(name="data_flow", description="How data flows between modules (describe the connections)", required=False),
    ],
)


def _render_compose_pipeline(args: dict) -> list[types.PromptMessage]:
    goal = args.get("goal", "")
    modules = args.get("modules", "")
    data_flow = args.get("data_flow", "")
    text = (
        "You are an expert dspygen pipeline architect.\n\n"
        f"Compose a pipeline to: **{goal}**\n\n"
        f"**Modules to chain:** {modules}\n"
        + (f"**Data flow:** {data_flow}\n" if data_flow else "")
        + "\n"
        "Produce:\n"
        "1. **Pipeline class** extending `dspy.Module` with `forward()` calling each sub-module\n"
        "2. **Data transformation** between module outputs and next module inputs\n"
        "3. **dspygen DSL YAML** version of the pipeline\n"
        "4. **Error handling** — what happens when a step fails\n"
        "5. **Streaming support** — if any module produces incremental output\n"
        "6. **Mermaid flowchart** showing the pipeline steps\n\n"
        "Return both Python code and YAML DSL versions."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: chain-modules
# ---------------------------------------------------------------------------

_CHAIN_MODULES = types.Prompt(
    name="chain-modules",
    description="Chain two or more dspygen modules with automatic output-to-input mapping.",
    arguments=[
        types.PromptArgument(name="module_a", description="First module name or signature", required=True),
        types.PromptArgument(name="module_b", description="Second module name or signature", required=True),
        types.PromptArgument(name="mapping", description="How to map output of A to input of B (optional)", required=False),
    ],
)


def _render_chain_modules(args: dict) -> list[types.PromptMessage]:
    mod_a = args.get("module_a", "")
    mod_b = args.get("module_b", "")
    mapping = args.get("mapping", "")
    text = (
        "You are an expert dspygen module composer.\n\n"
        f"Chain **{mod_a}** → **{mod_b}**.\n\n"
        + (f"**Output-to-input mapping:** {mapping}\n" if mapping else "")
        + "\n"
        "Generate:\n"
        "1. **`ChainedModule`** class that runs A then B\n"
        "2. **Field mapping** — explicit output_of_A → input_of_B connections\n"
        "3. **Type coercion** if needed between modules\n"
        "4. **Single `*_call()` function** for the chain\n"
        "5. **Example usage** with sample data\n\n"
        "Keep the chained module composable so it can be chained further."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: benchmark-module
# ---------------------------------------------------------------------------

_BENCHMARK_MODULE = types.Prompt(
    name="benchmark-module",
    description="Benchmark a dspygen module across multiple models and measure quality metrics.",
    arguments=[
        types.PromptArgument(name="module_name", description="Module to benchmark", required=True),
        types.PromptArgument(name="test_inputs", description="JSON array of test input examples", required=True),
        types.PromptArgument(name="models", description="Comma-separated model identifiers to compare", required=False),
    ],
)


def _render_benchmark_module(args: dict) -> list[types.PromptMessage]:
    module = args.get("module_name", "")
    inputs = args.get("test_inputs", "[]")
    models = args.get("models", "gpt-4o, gpt-4o-mini, ollama_chat/llama3.2")
    text = (
        "You are a DSPy benchmarking expert.\n\n"
        f"Benchmark **{module}** across multiple models.\n\n"
        f"**Test inputs:** {inputs}\n"
        f"**Models to compare:** {models}\n\n"
        "Produce a benchmark script that:\n"
        "1. **Loads** the module for each model\n"
        "2. **Runs** all test inputs through each model\n"
        "3. **Measures**: latency (p50, p95), token usage, quality score\n"
        "4. **Quality metric** — define a scoring function for the outputs\n"
        "5. **Results table** — markdown comparison of all models\n"
        "6. **Cost estimate** — approximate cost per 1000 calls for each model\n"
        "7. **Recommendation** — which model to use for production\n\n"
        "Return complete runnable Python benchmark script."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Prompt: refactor-module
# ---------------------------------------------------------------------------

_REFACTOR_MODULE = types.Prompt(
    name="refactor-module",
    description="Refactor a dspygen module for better performance, readability, or composability.",
    arguments=[
        types.PromptArgument(name="module_code", description="Current module source code", required=True),
        types.PromptArgument(name="refactor_goals", description="What to improve: performance, readability, composability, type safety", required=True),
    ],
)


def _render_refactor_module(args: dict) -> list[types.PromptMessage]:
    code = args.get("module_code", "")
    goals = args.get("refactor_goals", "readability, type safety")
    text = (
        "You are a senior dspygen code reviewer and refactoring expert.\n\n"
        f"Refactor this module for: **{goals}**\n\n"
        f"```python\n{code}\n```\n\n"
        "Produce:\n"
        "1. **Refactored code** — complete updated module\n"
        "2. **Change log** — what was changed and why\n"
        "3. **Breaking changes** — any API changes to be aware of\n"
        "4. **Performance improvements** — quantified where possible\n"
        "5. **Type safety** — add proper type hints throughout\n"
        "6. **Migration guide** — how to update existing callers\n\n"
        "Keep the same module interface (inputs/outputs) unless changes are clearly needed."
    )
    return _msg(text)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

MODULE_PROMPTS: list[types.Prompt] = [
    _GENERATE_MODULE,
    _CREATE_SIGNATURE,
    _OPTIMIZE_MODULE,
    _DEBUG_MODULE,
    _DOCUMENT_MODULE,
    _TEST_MODULE,
    _COMPOSE_PIPELINE,
    _CHAIN_MODULES,
    _BENCHMARK_MODULE,
    _REFACTOR_MODULE,
]

MODULE_RENDERERS: dict = {
    "generate-module": _render_generate_module,
    "create-signature": _render_create_signature,
    "optimize-module": _render_optimize_module,
    "debug-module": _render_debug_module,
    "document-module": _render_document_module,
    "test-module": _render_test_module,
    "compose-pipeline": _render_compose_pipeline,
    "chain-modules": _render_chain_modules,
    "benchmark-module": _render_benchmark_module,
    "refactor-module": _render_refactor_module,
}
