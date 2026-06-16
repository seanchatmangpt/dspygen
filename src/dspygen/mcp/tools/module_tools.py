"""
MCP tools for dspygen modules.

Provides tools to list, inspect, and execute dspygen DSPy modules.
All imports of dspygen internals are lazy (inside handlers) to avoid startup failures.
"""

from __future__ import annotations

import ast
import importlib
import json
import sys
from pathlib import Path
from typing import Any

from loguru import logger
from mcp import types

__all__ = ["get_tool_definitions", "handle_tool"]

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _modules_dir() -> Path:
    """Resolve the dspygen modules directory at call-time."""
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        modules_path = candidate / "dspygen" / "modules"
        if modules_path.is_dir():
            return modules_path
    raise FileNotFoundError("Could not locate dspygen/modules directory")


def _list_module_files() -> list[Path]:
    try:
        mdir = _modules_dir()
    except FileNotFoundError:
        return []
    return sorted(
        p for p in mdir.glob("*.py")
        if p.name != "__init__.py" and not p.name.startswith("test")
    )


def _extract_module_info(path: Path) -> dict[str, Any]:
    """Extract metadata from a module file using AST (no import needed)."""
    info: dict[str, Any] = {
        "name": path.stem,
        "file": str(path),
        "docstring": "",
        "classes": [],
        "signatures": [],
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
        info["docstring"] = tree.body[0].value.value.strip()  # type: ignore[union-attr]

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [
                ast.unparse(b) if hasattr(ast, "unparse") else getattr(b, "id", "")
                for b in node.bases
            ]
            class_info: dict[str, Any] = {
                "class_name": node.name,
                "docstring": ast.get_docstring(node) or "",
                "bases": bases,
                "input_fields": [],
                "output_fields": [],
            }
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and isinstance(item.value, ast.Call):
                            func_name = ""
                            if isinstance(item.value.func, ast.Attribute):
                                func_name = item.value.func.attr
                            elif isinstance(item.value.func, ast.Name):
                                func_name = item.value.func.id
                            if func_name == "InputField":
                                class_info["input_fields"].append(target.id)
                            elif func_name == "OutputField":
                                class_info["output_fields"].append(target.id)

            info["classes"].append(class_info)
            if any("Signature" in b for b in bases):
                info["signatures"].append(node.name)

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
    "list_modules",
    "get_module_info",
    "run_module",
    "generate_dspy_signature",
    "generate_dspy_module",
    "scaffold_module",
}


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all module tools."""
    return [
        types.Tool(
            name="list_modules",
            description=(
                "List all available dspygen DSPy modules. "
                "Returns a JSON array with module names, docstrings, and signature class names."
            ),
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_module_info",
            description=(
                "Get detailed information about a specific dspygen module including "
                "its DSPy Signature input/output fields, class names, and docstring."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "Module file stem, e.g. 'blog_module'",
                    }
                },
                "required": ["module_name"],
            },
        ),
        types.Tool(
            name="run_module",
            description=(
                "Import and execute a dspygen module by name. "
                "Calls the module's *_call convenience function with the provided inputs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {
                        "type": "string",
                        "description": "Module file stem, e.g. 'blog_module'",
                    },
                    "inputs": {
                        "type": "object",
                        "description": "Keyword arguments forwarded to the module's call function",
                    },
                },
                "required": ["module_name"],
            },
        ),
        types.Tool(
            name="generate_dspy_signature",
            description=(
                "Generate a DSPy Signature string from a natural-language description "
                "using GenSignatureModule. Example description: 'topic -> blog_post'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Natural language or shorthand description of inputs -> outputs",
                    }
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="generate_dspy_module",
            description=(
                "Generate boilerplate Python code for a new dspygen DSPy module "
                "given a signature string and a class name."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "signature": {
                        "type": "string",
                        "description": "DSPy signature string, e.g. 'topic -> blog_post'",
                    },
                    "class_name": {
                        "type": "string",
                        "description": "Python class name for the generated module",
                        "default": "GeneratedModule",
                    },
                },
                "required": ["signature"],
            },
        ),
        types.Tool(
            name="scaffold_module",
            description=(
                "Generate a complete dspygen-style Python module file from scratch. "
                "Returns a full Python source string with imports, DSPy Signature, "
                "Module class with forward method, a module_call convenience function, "
                "and an if __name__ == '__main__' block."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {
                        "type": "string",
                        "description": "PascalCase class name, e.g. 'BlogPost' (Module suffix added automatically)",
                    },
                    "input_fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of input field names for the DSPy Signature, e.g. ['topic', 'tone']",
                    },
                    "output_field": {
                        "type": "string",
                        "description": "Single output field name for the DSPy Signature, e.g. 'blog_post'",
                    },
                    "description": {
                        "type": "string",
                        "description": "Human-readable description of what this module does (used as docstring)",
                    },
                },
                "required": ["class_name", "input_fields", "output_field", "description"],
            },
        ),
    ]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def handle_tool(name: str, arguments: dict) -> list[types.TextContent] | None:
    """
    Dispatch a tool call.  Returns None if this module does not own *name*.
    """
    if name not in _TOOL_NAMES:
        return None

    if name == "list_modules":
        return await _list_modules(arguments)
    if name == "get_module_info":
        return await _get_module_info(arguments)
    if name == "run_module":
        return await _run_module(arguments)
    if name == "generate_dspy_signature":
        return await _generate_dspy_signature(arguments)
    if name == "generate_dspy_module":
        return await _generate_dspy_module(arguments)
    if name == "scaffold_module":
        return await _scaffold_module(arguments)

    return _err(f"Unhandled tool: {name}")  # shouldn't happen


async def _list_modules(args: dict) -> list[types.TextContent]:
    try:
        files = _list_module_files()
        result = []
        for path in files:
            info = _extract_module_info(path)
            result.append(
                {
                    "name": info["name"],
                    "docstring": info["docstring"][:200] if info["docstring"] else "",
                    "signatures": info["signatures"],
                }
            )
        return _ok(result)
    except Exception as exc:
        return _err(f"list_modules failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _get_module_info(args: dict) -> list[types.TextContent]:
    module_name: str = (args or {}).get("module_name", "")
    if not module_name:
        return _err("module_name argument is required")
    try:
        files = _list_module_files()
        matches = [p for p in files if p.stem == module_name]
        if not matches:
            return _err(f"Module '{module_name}' not found")
        info = _extract_module_info(matches[0])
        return _ok(info)
    except Exception as exc:
        return _err(f"get_module_info failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _run_module(args: dict) -> list[types.TextContent]:
    module_name: str = (args or {}).get("module_name", "")
    inputs: dict = (args or {}).get("inputs", {})
    if not module_name:
        return _err("module_name argument is required")
    try:
        src_dir = str(Path(__file__).resolve().parents[4])
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        mod = importlib.import_module(f"dspygen.modules.{module_name}")

        call_fn_name = module_name.replace("_module", "") + "_call"
        call_fn = getattr(mod, call_fn_name, None)

        if call_fn is None:
            for attr_name in dir(mod):
                if attr_name.endswith("_call") and callable(getattr(mod, attr_name)):
                    call_fn = getattr(mod, attr_name)
                    break

        if call_fn is None:
            return _err(
                f"No *_call function found in module '{module_name}'."
            )

        result = call_fn(**inputs)
        return _ok({"result": str(result)})
    except Exception as exc:
        logger.exception(f"run_module error for {module_name}")
        return _err(f"run_module failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _generate_dspy_signature(args: dict) -> list[types.TextContent]:
    description: str = (args or {}).get("description", "")
    if not description:
        return _err("description argument is required (e.g. 'topic -> blog_post')")
    try:
        src_dir = str(Path(__file__).resolve().parents[4])
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.modules.gen_signature_module import gen_signature_call  # lazy

        result = gen_signature_call(description)
        return _ok({"signature": str(result)})
    except Exception as exc:
        logger.exception("generate_dspy_signature error")
        return _err(f"generate_dspy_signature failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _generate_dspy_module(args: dict) -> list[types.TextContent]:
    signature: str = (args or {}).get("signature", "")
    class_name: str = (args or {}).get("class_name", "GeneratedModule")
    if not signature:
        return _err("signature argument is required")
    try:
        template = (
            f"import dspy\n\n\n"
            f"class {class_name}Signature(dspy.Signature):\n"
            f'    """{signature}"""\n\n'
            f"    # TODO: define InputField / OutputField members\n\n\n"
            f"class {class_name}(dspy.Module):\n"
            f'    """{class_name}"""\n\n'
            f"    def forward(self, **kwargs):\n"
            f"        pred = dspy.ChainOfThought({class_name}Signature)\n"
            f"        return pred(**kwargs)\n"
        )
        return _ok({"module_code": template, "class_name": class_name})
    except Exception as exc:
        return _err(f"generate_dspy_module failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")


async def _scaffold_module(args: dict) -> list[types.TextContent]:
    class_name: str = (args or {}).get("class_name", "")
    input_fields: list = (args or {}).get("input_fields", [])
    output_field: str = (args or {}).get("output_field", "")
    description: str = (args or {}).get("description", "")

    if not class_name:
        return _err("class_name argument is required")
    if not input_fields:
        return _err("input_fields argument is required and must be non-empty")
    if not output_field:
        return _err("output_field argument is required")
    if not description:
        return _err("description argument is required")

    try:
        # Derive snake_case module name and call-function name from PascalCase class_name
        # e.g. "BlogPost" -> "blog_post_module" / "blog_post_call"
        import re
        snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", class_name).lower()
        call_fn_name = f"{snake}_call"

        # Build InputField / OutputField lines
        input_lines = "\n".join(
            f'    {f} = dspy.InputField(desc="{f.replace("_", " ")}")'
            for f in input_fields
        )
        output_line = f'    {output_field} = dspy.OutputField(desc="{output_field.replace("_", " ")}")'

        call_args = ", ".join(f"{f}: str" for f in input_fields)
        call_kwargs = ", ".join(f"{f}={f}" for f in input_fields)
        example_args = ", ".join(f'"{f}_value"' for f in input_fields)

        code = f'''\
"""
{description}
"""

from __future__ import annotations

import dspy
from dspygen.utils.dspy_tools import init_dspy


class {class_name}Signature(dspy.Signature):
    """{description}"""

{input_lines}
{output_line}


class {class_name}Module(dspy.Module):
    """{description}"""

    def __init__(self):
        super().__init__()
        self.predict = dspy.ChainOfThought({class_name}Signature)

    def forward(self, {call_args}) -> str:
        result = self.predict({call_kwargs})
        return getattr(result, "{output_field}", "")


def {call_fn_name}({call_args}) -> str:
    """Convenience wrapper — initialises dspy and runs {class_name}Module."""
    init_dspy()
    module = {class_name}Module()
    return module.forward({call_kwargs})


if __name__ == "__main__":
    result = {call_fn_name}({example_args})
    print(result)
'''
        return [types.TextContent(type="text", text=code)]
    except Exception as exc:
        return _err(f"scaffold_module failed: {type(exc).__name__}: {exc} — check that dspygen is properly configured and inputs are valid.")
