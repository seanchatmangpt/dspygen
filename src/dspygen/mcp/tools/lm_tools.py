"""
MCP tools for LLM/LM configuration and sampling in dspygen.

Provides tools to configure DSPy with different model providers,
list available models, run completions, and optimize modules.

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


def _ensure_path() -> None:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        if (candidate / "dspygen").is_dir():
            sys.path.insert(0, str(candidate))
            return


_TOOL_NAMES = {
    "configure_lm",
    "list_available_models",
    "sample_completion",
    "chain_of_thought",
    "run_program_of_thought",
    "optimize_module",
    "get_lm_history",
}

# Known model providers and their example model IDs
_KNOWN_PROVIDERS = {
    "openai": {
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "o1", "o1-mini"],
        "env_key": "OPENAI_API_KEY",
        "prefix": "openai/",
    },
    "ollama": {
        "models": ["llama3.2", "llama3.1", "codellama", "mistral", "phi3", "gemma2", "qwen2.5"],
        "env_key": "OLLAMA_HOST",
        "prefix": "ollama_chat/",
    },
    "groq": {
        "models": [
            "groq/llama-3.1-70b-versatile",
            "groq/llama-3.1-8b-instant",
            "groq/mixtral-8x7b-32768",
        ],
        "env_key": "GROQ_API_KEY",
        "prefix": "groq/",
    },
    "cerebras": {
        "models": ["cerebras/llama3.1-8b", "cerebras/llama3.1-70b"],
        "env_key": "CEREBRAS_API_KEY",
        "prefix": "cerebras/",
    },
    "anthropic": {
        "models": [
            "claude-opus-4-5",
            "claude-sonnet-4-5",
            "claude-haiku-3-5",
            "claude-3-opus-20240229",
        ],
        "env_key": "ANTHROPIC_API_KEY",
        "prefix": "anthropic/",
    },
    "google": {
        "models": ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash", "gemini/gemini-2.0-flash"],
        "env_key": "GOOGLE_API_KEY",
        "prefix": "gemini/",
    },
}


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all LM tools."""
    return [
        types.Tool(
            name="configure_lm",
            description=(
                "Configure DSPy with a specific language model provider and model. "
                "Supports OpenAI, Ollama, Groq, Cerebras, Anthropic, and Google. "
                "Returns the active model configuration after setup."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model identifier, e.g. 'openai/gpt-4o', 'ollama_chat/llama3.2', 'groq/llama-3.1-70b-versatile'",
                    },
                    "provider": {
                        "type": "string",
                        "description": "Provider: openai, ollama, groq, cerebras, anthropic, google",
                        "default": "openai",
                    },
                    "api_key": {
                        "type": "string",
                        "description": "API key (if not set via environment variable)",
                        "default": "",
                    },
                    "api_base": {
                        "type": "string",
                        "description": "Custom API base URL (for Ollama or custom endpoints)",
                        "default": "",
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature (0.0-2.0)",
                        "default": 0.7,
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum output tokens",
                        "default": 1000,
                    },
                },
                "required": ["model"],
            },
        ),
        types.Tool(
            name="list_available_models",
            description=(
                "List all known LM providers and their available model IDs. "
                "Also reports currently configured DSPy LM settings."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="sample_completion",
            description=(
                "Run a raw DSPy Predict with a given inline signature string. "
                "The signature format is 'input1, input2 -> output1, output2'. "
                "Returns the model's prediction."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "signature": {
                        "type": "string",
                        "description": "DSPy signature string, e.g. 'question -> answer'",
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Input field values matching the signature",
                    },
                },
                "required": ["signature", "inputs"],
            },
        ),
        types.Tool(
            name="chain_of_thought",
            description=(
                "Run a DSPy ChainOfThought predictor on a given signature. "
                "Forces step-by-step reasoning before producing the output. "
                "Useful for complex reasoning tasks."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "signature": {
                        "type": "string",
                        "description": "DSPy signature string, e.g. 'question, context -> answer'",
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Input field values matching the signature",
                    },
                },
                "required": ["signature", "inputs"],
            },
        ),
        types.Tool(
            name="run_program_of_thought",
            description=(
                "Run dspy.ProgramOfThought on a math or code problem. "
                "Generates and executes code to produce a verifiable answer."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "signature": {
                        "type": "string",
                        "description": "DSPy signature string, e.g. 'problem -> solution'",
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Input field values",
                    },
                },
                "required": ["signature", "inputs"],
            },
        ),
        types.Tool(
            name="optimize_module",
            description=(
                "Optimize a dspygen module using BootstrapFewShot or MIPROv2 with provided examples. "
                "Returns the optimized module configuration and metrics."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "Module file stem, e.g. 'blog_module'",
                    },
                    "train_examples": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Training examples as [{inputs: {...}, outputs: {...}}]",
                    },
                    "optimizer": {
                        "type": "string",
                        "description": "Optimizer to use: 'BootstrapFewShot' or 'MIPROv2'",
                        "default": "BootstrapFewShot",
                    },
                    "max_bootstrapped_demos": {
                        "type": "integer",
                        "description": "Maximum bootstrapped demonstrations",
                        "default": 4,
                    },
                },
                "required": ["module_name", "train_examples"],
            },
        ),
        types.Tool(
            name="get_lm_history",
            description=(
                "Retrieve the DSPy LM call history from dspy.settings. "
                "Returns recent LM calls with their prompts and completions."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "last_n": {
                        "type": "integer",
                        "description": "Number of recent calls to return",
                        "default": 10,
                    },
                },
                "required": [],
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
        "configure_lm": _configure_lm,
        "list_available_models": _list_available_models,
        "sample_completion": _sample_completion,
        "chain_of_thought": _chain_of_thought,
        "run_program_of_thought": _run_program_of_thought,
        "optimize_module": _optimize_module,
        "get_lm_history": _get_lm_history,
    }

    handler = handlers.get(name)
    if handler:
        return await handler(arguments or {})
    return _err(f"Unhandled tool: {name}")


async def _configure_lm(args: dict) -> list[types.TextContent]:
    model = args.get("model", "")
    provider = args.get("provider", "openai")
    api_key = args.get("api_key", "")
    api_base = args.get("api_base", "")
    temperature = float(args.get("temperature", 0.7))
    max_tokens = int(args.get("max_tokens", 1000))

    if not model:
        return _err("model is required")

    try:
        import dspy  # lazy

        # Build kwargs
        lm_kwargs: dict = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if api_key:
            lm_kwargs["api_key"] = api_key
        if api_base:
            lm_kwargs["api_base"] = api_base

        lm = dspy.LM(**lm_kwargs)
        dspy.configure(lm=lm)

        logger.info(f"Configured dspy with model={model}, provider={provider}")
        return _ok({
            "configured": True,
            "model": model,
            "provider": provider,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "api_base": api_base or "(default)",
        })
    except Exception as exc:
        logger.exception("configure_lm error")
        return _err(f"configure_lm failed: {exc}")


async def _list_available_models(_args: dict) -> list[types.TextContent]:
    try:
        import os

        import dspy  # lazy

        # Check current configuration
        current_lm = None
        try:
            lm = dspy.settings.lm
            if lm is not None:
                current_lm = {
                    "model": getattr(lm, "model", str(lm)),
                    "provider": getattr(lm, "provider", "unknown"),
                }
        except Exception:
            pass

        # Build provider list with env-key availability
        providers = {}
        for provider_name, info in _KNOWN_PROVIDERS.items():
            env_key = info["env_key"]
            providers[provider_name] = {
                "models": info["models"],
                "env_key": env_key,
                "configured": bool(os.environ.get(env_key)),  # type: ignore[call-overload]
                "model_prefix": info["prefix"],
            }

        return _ok({
            "current_lm": current_lm,
            "providers": providers,
            "usage_example": "Use configure_lm with model='openai/gpt-4o' to set up a provider",
        })
    except Exception as exc:
        logger.exception("list_available_models error")
        return _err(f"list_available_models failed: {exc}")


async def _sample_completion(args: dict) -> list[types.TextContent]:
    signature = args.get("signature", "")
    inputs = args.get("inputs", {})
    if not signature:
        return _err("signature is required")
    if not inputs:
        return _err("inputs is required")
    try:
        import dspy  # lazy
        pred = dspy.Predict(signature)
        result = pred(**inputs)
        # Extract outputs
        outputs = {}
        for key in dir(result):
            if not key.startswith("_"):
                val = getattr(result, key, None)
                if val is not None and not callable(val):
                    outputs[key] = str(val)
        return _ok({
            "signature": signature,
            "inputs": inputs,
            "outputs": outputs,
        })
    except Exception as exc:
        logger.exception("sample_completion error")
        return _err(f"sample_completion failed: {exc}")


async def _chain_of_thought(args: dict) -> list[types.TextContent]:
    signature = args.get("signature", "")
    inputs = args.get("inputs", {})
    if not signature:
        return _err("signature is required")
    if not inputs:
        return _err("inputs is required")
    try:
        import dspy  # lazy
        pred = dspy.ChainOfThought(signature)
        result = pred(**inputs)
        outputs = {}
        for key in dir(result):
            if not key.startswith("_"):
                val = getattr(result, key, None)
                if val is not None and not callable(val):
                    outputs[key] = str(val)
        return _ok({
            "signature": signature,
            "inputs": inputs,
            "outputs": outputs,
            "reasoning": outputs.get("reasoning", outputs.get("rationale", "")),
        })
    except Exception as exc:
        logger.exception("chain_of_thought error")
        return _err(f"chain_of_thought failed: {exc}")


async def _run_program_of_thought(args: dict) -> list[types.TextContent]:
    signature = args.get("signature", "")
    inputs = args.get("inputs", {})
    if not signature:
        return _err("signature is required")
    if not inputs:
        return _err("inputs is required")
    try:
        import dspy  # lazy
        pot = dspy.ProgramOfThought(signature)
        result = pot(**inputs)
        outputs = {}
        for key in dir(result):
            if not key.startswith("_"):
                val = getattr(result, key, None)
                if val is not None and not callable(val):
                    outputs[key] = str(val)
        return _ok({
            "signature": signature,
            "inputs": inputs,
            "outputs": outputs,
        })
    except Exception as exc:
        logger.exception("run_program_of_thought error")
        return _err(f"run_program_of_thought failed: {exc}")


async def _optimize_module(args: dict) -> list[types.TextContent]:
    module_name = args.get("module_name", "")
    train_examples = args.get("train_examples", [])
    optimizer_name = args.get("optimizer", "BootstrapFewShot")
    max_bootstrapped_demos = int(args.get("max_bootstrapped_demos", 4))

    if not module_name:
        return _err("module_name is required")
    if not train_examples:
        return _err("train_examples is required (list of {inputs, outputs} dicts)")

    try:
        import importlib

        import dspy  # lazy

        # Load the module
        mod = importlib.import_module(f"dspygen.modules.{module_name}")

        # Find the module class
        module_class = None
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name, None)
            if (
                attr is not None
                and isinstance(attr, type)
                and issubclass(attr, dspy.Module)
                and attr is not dspy.Module
            ):
                module_class = attr
                break

        if module_class is None:
            return _err(f"No dspy.Module subclass found in {module_name}")

        # Convert examples
        dspy_examples = []
        for ex in train_examples:
            inp = ex.get("inputs", {})
            out = ex.get("outputs", {})
            dspy_examples.append(dspy.Example(**inp, **out).with_inputs(*inp.keys()))

        # Run optimizer
        module_instance = module_class()

        if optimizer_name == "MIPROv2":
            optimizer = dspy.MIPROv2(metric=None, auto="light")
        else:
            optimizer = dspy.BootstrapFewShot(metric=None, max_bootstrapped_demos=max_bootstrapped_demos)

        optimized = optimizer.compile(module_instance, trainset=dspy_examples)

        return _ok({
            "module": module_name,
            "optimizer": optimizer_name,
            "train_examples_count": len(dspy_examples),
            "optimized": True,
            "module_class": module_class.__name__,
            "note": "Module optimized in memory. Use save_path to persist (not yet implemented in MCP).",
        })
    except Exception as exc:
        logger.exception("optimize_module error")
        return _err(f"optimize_module failed: {exc}")


async def _get_lm_history(args: dict) -> list[types.TextContent]:
    last_n = int(args.get("last_n", 10))
    try:
        import dspy  # lazy
        lm = dspy.settings.lm
        if lm is None:
            return _ok({"history": [], "note": "No LM configured. Use configure_lm first."})

        history = getattr(lm, "history", None)
        if history is None:
            # Try to get from inspect
            history = []
            try:
                history = lm.inspect_history(n=last_n)
                return _ok({"history": str(history), "count": last_n})
            except Exception:
                pass
            return _ok({
                "history": [],
                "model": getattr(lm, "model", str(lm)),
                "note": "LM history not available for this provider.",
            })

        recent = list(history)[-last_n:]
        serialized = []
        for h in recent:
            if isinstance(h, dict):
                serialized.append({k: str(v)[:500] for k, v in h.items()})
            else:
                serialized.append(str(h)[:500])  # type: ignore[arg-type]

        return _ok({
            "model": getattr(lm, "model", str(lm)),
            "total_calls": len(list(history)),
            "last_n": last_n,
            "history": serialized,
        })
    except Exception as exc:
        logger.exception("get_lm_history error")
        return _err(f"get_lm_history failed: {exc}")
