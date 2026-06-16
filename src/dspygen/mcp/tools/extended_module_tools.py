"""
MCP tools for category-specific dspygen module execution.

Provides direct, named tools for the most commonly-used dspygen modules,
eliminating the need to know internal module names.

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
    "generate_tweet",
    "summarize_document",
    "natural_language_to_sql",
    "generate_blog_post",
    "generate_code_comments",
    "translate_data_format",
    "classify_customer_feedback",
    "generate_mermaid_diagram",
    "cobol_to_python",
    "generate_pydantic_class",
    "generate_cli_module",
    "generate_jsx",
    "ask_dataframe",
    "ask_data",
    "generate_nuxt_component",
    "chatbot_response",
    "check_condition",
    "generate_test",
    "optimize_bytecode",
    "translate_bpmn_to_bpel",
}


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all extended module tools."""
    return [
        types.Tool(
            name="generate_tweet",
            description=(
                "Generate a tweet or social-media post using dspygen's tweet module. "
                "Returns a short, engaging post on the given topic."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic or content to tweet about"},
                    "tone": {
                        "type": "string",
                        "description": "Tone: 'professional', 'casual', 'humorous', etc.",
                        "default": "professional",
                    },
                },
                "required": ["topic"],
            },
        ),
        types.Tool(
            name="summarize_document",
            description=(
                "Summarize a text document using DocumentSummarizerModule. "
                "Returns a concise summary preserving key points."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "document": {"type": "string", "description": "Text content to summarize"},
                    "max_length": {
                        "type": "integer",
                        "description": "Target summary length in words",
                        "default": 150,
                    },
                },
                "required": ["document"],
            },
        ),
        types.Tool(
            name="natural_language_to_sql",
            description=(
                "Convert a natural-language question to a SQL query using NaturalLanguageToSqlModule. "
                "Provide the question and optionally a schema description."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Natural language question"},
                    "schema": {
                        "type": "string",
                        "description": "Optional SQL schema context (table names, columns)",
                        "default": "",
                    },
                },
                "required": ["question"],
            },
        ),
        types.Tool(
            name="generate_blog_post",
            description=(
                "Generate a complete blog post on a given topic using BlogModule. "
                "Returns structured blog content with title, sections, and conclusion."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Blog post topic"},
                    "audience": {
                        "type": "string",
                        "description": "Target audience for the blog post",
                        "default": "general readers",
                    },
                    "word_count": {
                        "type": "integer",
                        "description": "Approximate target word count",
                        "default": 800,
                    },
                },
                "required": ["topic"],
            },
        ),
        types.Tool(
            name="generate_code_comments",
            description=(
                "Generate documentation comments for source code using CodeCommentsToDocumentationModule. "
                "Returns the code annotated with docstrings and inline comments."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Source code to document"},
                    "language": {
                        "type": "string",
                        "description": "Programming language (python, javascript, java, etc.)",
                        "default": "python",
                    },
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="translate_data_format",
            description=(
                "Translate data between formats (JSON→YAML, CSV→JSON, XML→JSON, etc.) "
                "using DataFormatTranslatorModule."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "Source data content as a string"},
                    "source_format": {
                        "type": "string",
                        "description": "Source format: json, yaml, csv, xml, toml, etc.",
                    },
                    "target_format": {
                        "type": "string",
                        "description": "Target format: json, yaml, csv, xml, toml, etc.",
                    },
                },
                "required": ["data", "source_format", "target_format"],
            },
        ),
        types.Tool(
            name="classify_customer_feedback",
            description=(
                "Classify customer feedback by sentiment and category using CustomerFeedbackClassifierModule. "
                "Returns sentiment (positive/negative/neutral) and category labels."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "feedback": {"type": "string", "description": "Customer feedback text to classify"},
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of categories to classify into",
                        "default": [],
                    },
                },
                "required": ["feedback"],
            },
        ),
        types.Tool(
            name="generate_mermaid_diagram",
            description=(
                "Generate a Mermaid.js diagram from a description using MermaidJsModule. "
                "Returns Mermaid diagram syntax for flowcharts, sequence diagrams, ERDs, etc."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the diagram to generate",
                    },
                    "diagram_type": {
                        "type": "string",
                        "description": "Mermaid diagram type: flowchart, sequenceDiagram, erDiagram, classDiagram, etc.",
                        "default": "flowchart",
                    },
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="cobol_to_python",
            description=(
                "Convert COBOL source code to equivalent Python using CobolToPythonModule. "
                "Returns Python code that replicates the COBOL logic."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "cobol_code": {"type": "string", "description": "COBOL source code to convert"},
                },
                "required": ["cobol_code"],
            },
        ),
        types.Tool(
            name="generate_pydantic_class",
            description=(
                "Generate a Pydantic model class from a description or JSON schema using GenPydanticClass. "
                "Returns a complete Python Pydantic model definition."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the model or JSON schema example",
                    },
                    "class_name": {
                        "type": "string",
                        "description": "Python class name for the generated model",
                        "default": "GeneratedModel",
                    },
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="generate_cli_module",
            description=(
                "Generate a Typer CLI module from a description using GenCliModule. "
                "Returns Python CLI code using the Typer framework."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Description of the CLI tool to generate",
                    },
                    "commands": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of CLI command names",
                        "default": [],
                    },
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="generate_jsx",
            description=(
                "Generate a React JSX component from a description using JsxModule or ReactJsxModule. "
                "Returns a functional React component with props and hooks."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Component description and requirements"},
                    "component_name": {
                        "type": "string",
                        "description": "React component name (PascalCase)",
                        "default": "GeneratedComponent",
                    },
                    "use_typescript": {
                        "type": "boolean",
                        "description": "Whether to generate TypeScript (.tsx) code",
                        "default": False,
                    },
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="ask_dataframe",
            description=(
                "Ask a natural-language question about a CSV/DataFrame using AskDfModule. "
                "Returns the answer derived from the data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Question to answer from the data"},
                    "csv_data": {
                        "type": "string",
                        "description": "CSV data as a string (header row + data rows)",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to CSV file (alternative to csv_data)",
                        "default": "",
                    },
                },
                "required": ["question"],
            },
        ),
        types.Tool(
            name="ask_data",
            description=(
                "Answer natural-language questions about structured data using AskDataModule. "
                "Suitable for database-style queries on text-described datasets."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Question to answer"},
                    "data_description": {
                        "type": "string",
                        "description": "Description or sample of the data to query",
                    },
                },
                "required": ["question", "data_description"],
            },
        ),
        types.Tool(
            name="generate_nuxt_component",
            description=(
                "Generate a Nuxt.js Vue component from a description using NuxtModule. "
                "Returns a complete .vue single-file component."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Component requirements and purpose"},
                    "component_name": {
                        "type": "string",
                        "description": "Component name in PascalCase",
                        "default": "GeneratedComponent",
                    },
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="chatbot_response",
            description=(
                "Generate a chatbot response to a user message using ChatbotResponseGeneratorModule. "
                "Optionally provide conversation history for context."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "user_message": {"type": "string", "description": "The user's message"},
                    "system_prompt": {
                        "type": "string",
                        "description": "System prompt defining the chatbot persona",
                        "default": "You are a helpful assistant.",
                    },
                    "conversation_history": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Previous conversation turns [{role, content}]",
                        "default": [],
                    },
                },
                "required": ["user_message"],
            },
        ),
        types.Tool(
            name="check_condition",
            description=(
                "Check whether there is sufficient information to answer a question using ConditionSufficientInfoModule. "
                "Returns a boolean and explanation of what is missing."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Question to check"},
                    "context": {
                        "type": "string",
                        "description": "Available context/information",
                        "default": "",
                    },
                },
                "required": ["question"],
            },
        ),
        types.Tool(
            name="generate_test",
            description=(
                "Generate pytest test cases for a Python function or module using pytest_module. "
                "Returns complete pytest test code."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code (function or class) to generate tests for",
                    },
                    "test_scenarios": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional specific scenarios to test",
                        "default": [],
                    },
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="optimize_bytecode",
            description=(
                "Analyze and optimize Python bytecode or source code using CodeToBytecodeOptimizerModule. "
                "Returns optimization suggestions and improved code."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python source code to optimize"},
                    "optimization_level": {
                        "type": "string",
                        "description": "Optimization level: 'basic', 'moderate', 'aggressive'",
                        "default": "moderate",
                    },
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="translate_bpmn_to_bpel",
            description=(
                "Translate a BPMN business process description to BPEL XML using Bpmn2BpelModule. "
                "Returns BPEL XML representing the business process."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "bpmn_description": {
                        "type": "string",
                        "description": "BPMN process description or XML content",
                    },
                    "process_name": {
                        "type": "string",
                        "description": "Name for the BPEL process",
                        "default": "GeneratedProcess",
                    },
                },
                "required": ["bpmn_description"],
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
        "generate_tweet": _generate_tweet,
        "summarize_document": _summarize_document,
        "natural_language_to_sql": _natural_language_to_sql,
        "generate_blog_post": _generate_blog_post,
        "generate_code_comments": _generate_code_comments,
        "translate_data_format": _translate_data_format,
        "classify_customer_feedback": _classify_customer_feedback,
        "generate_mermaid_diagram": _generate_mermaid_diagram,
        "cobol_to_python": _cobol_to_python,
        "generate_pydantic_class": _generate_pydantic_class,
        "generate_cli_module": _generate_cli_module,
        "generate_jsx": _generate_jsx,
        "ask_dataframe": _ask_dataframe,
        "ask_data": _ask_data,
        "generate_nuxt_component": _generate_nuxt_component,
        "chatbot_response": _chatbot_response,
        "check_condition": _check_condition,
        "generate_test": _generate_test,
        "optimize_bytecode": _optimize_bytecode,
        "translate_bpmn_to_bpel": _translate_bpmn_to_bpel,
    }

    handler = handlers.get(name)
    if handler:
        return await handler(arguments or {})
    return _err(f"Unhandled tool: {name}")


def _call_module(module_path: str, fn_name: str, **kwargs) -> Any:
    """Lazy-import a dspygen module and call the specified function."""
    import importlib
    mod = importlib.import_module(module_path)
    fn = getattr(mod, fn_name)
    return fn(**kwargs)


async def _generate_tweet(args: dict) -> list[types.TextContent]:
    topic = args.get("topic", "")
    tone = args.get("tone", "professional")
    if not topic:
        return _err("topic is required")
    try:
        # Try tweet module, fall back to generic gen_module
        try:
            result = _call_module(
                "dspygen.modules.tweet_dg_module",
                "tweet_dg_call",
                topic=topic,
                tone=tone,
            )
        except (ImportError, AttributeError):
            result = _call_module(
                "dspygen.modules.gen_module",
                "gen_call",
                signature="topic, tone -> tweet",
                topic=topic,
                tone=tone,
            )
        return _ok({"tweet": str(result), "topic": topic, "tone": tone})
    except Exception as exc:
        logger.exception("generate_tweet error")
        return _err(f"generate_tweet failed: {exc}")


async def _summarize_document(args: dict) -> list[types.TextContent]:
    document = args.get("document", "")
    max_length = int(args.get("max_length", 150))
    if not document:
        return _err("document is required")
    try:
        result = _call_module(
            "dspygen.modules.document_summarizer_module",
            "document_summarizer_call",
            document=document,
        )
        return _ok({"summary": str(result), "max_length": max_length})
    except Exception as exc:
        logger.exception("summarize_document error")
        return _err(f"summarize_document failed: {exc}")


async def _natural_language_to_sql(args: dict) -> list[types.TextContent]:
    question = args.get("question", "")
    schema = args.get("schema", "")
    if not question:
        return _err("question is required")
    try:
        kwargs = {"question": question}
        if schema:
            kwargs["schema"] = schema
        try:
            result = _call_module(
                "dspygen.modules.natural_language_to_sql_module",
                "natural_language_to_sql_call",
                **kwargs,
            )
        except (ImportError, AttributeError):
            result = _call_module(
                "dspygen.modules.df_sql_module",
                "df_sql_call",
                question=question,
            )
        return _ok({"sql": str(result), "question": question})
    except Exception as exc:
        logger.exception("natural_language_to_sql error")
        return _err(f"natural_language_to_sql failed: {exc}")


async def _generate_blog_post(args: dict) -> list[types.TextContent]:
    topic = args.get("topic", "")
    audience = args.get("audience", "general readers")
    word_count = int(args.get("word_count", 800))
    if not topic:
        return _err("topic is required")
    try:
        result = _call_module(
            "dspygen.modules.blog_module",
            "blog_call",
            topic=topic,
            audience=audience,
        )
        return _ok({"blog_post": str(result), "topic": topic, "audience": audience})
    except Exception as exc:
        logger.exception("generate_blog_post error")
        return _err(f"generate_blog_post failed: {exc}")


async def _generate_code_comments(args: dict) -> list[types.TextContent]:
    code = args.get("code", "")
    language = args.get("language", "python")
    if not code:
        return _err("code is required")
    try:
        result = _call_module(
            "dspygen.modules.code_comments_to_documentation_module",
            "code_comments_to_documentation_call",
            code=code,
        )
        return _ok({"documented_code": str(result), "language": language})
    except Exception as exc:
        logger.exception("generate_code_comments error")
        return _err(f"generate_code_comments failed: {exc}")


async def _translate_data_format(args: dict) -> list[types.TextContent]:
    data = args.get("data", "")
    source_format = args.get("source_format", "")
    target_format = args.get("target_format", "")
    if not data or not source_format or not target_format:
        return _err("data, source_format, and target_format are required")
    try:
        result = _call_module(
            "dspygen.modules.data_format_translator_module",
            "data_format_translator_call",
            data=data,
            source_format=source_format,
            target_format=target_format,
        )
        return _ok({
            "result": str(result),
            "source_format": source_format,
            "target_format": target_format,
        })
    except Exception as exc:
        logger.exception("translate_data_format error")
        return _err(f"translate_data_format failed: {exc}")


async def _classify_customer_feedback(args: dict) -> list[types.TextContent]:
    feedback = args.get("feedback", "")
    categories = args.get("categories", [])
    if not feedback:
        return _err("feedback is required")
    try:
        kwargs: dict = {"feedback": feedback}
        if categories:
            kwargs["categories"] = categories
        result = _call_module(
            "dspygen.modules.customer_feedback_classifier_module",
            "customer_feedback_classifier_call",
            **kwargs,
        )
        return _ok({"classification": str(result), "feedback_excerpt": feedback[:200]})
    except Exception as exc:
        logger.exception("classify_customer_feedback error")
        return _err(f"classify_customer_feedback failed: {exc}")


async def _generate_mermaid_diagram(args: dict) -> list[types.TextContent]:
    description = args.get("description", "")
    diagram_type = args.get("diagram_type", "flowchart")
    if not description:
        return _err("description is required")
    try:
        try:
            result = _call_module(
                "dspygen.modules.mermaid_js_module",
                "mermaid_js_call",
                description=description,
                diagram_type=diagram_type,
            )
        except (ImportError, AttributeError):
            result = _call_module(
                "dspygen.modules.mermaid_js_module",
                "mermaid_js_call",
                description=description,
            )
        return _ok({
            "mermaid_code": str(result),
            "diagram_type": diagram_type,
            "description": description,
        })
    except Exception as exc:
        logger.exception("generate_mermaid_diagram error")
        return _err(f"generate_mermaid_diagram failed: {exc}")


async def _cobol_to_python(args: dict) -> list[types.TextContent]:
    cobol_code = args.get("cobol_code", "")
    if not cobol_code:
        return _err("cobol_code is required")
    try:
        result = _call_module(
            "dspygen.modules.cobol_to_python_module",
            "cobol_to_python_call",
            cobol_code=cobol_code,
        )
        return _ok({"python_code": str(result)})
    except Exception as exc:
        logger.exception("cobol_to_python error")
        return _err(f"cobol_to_python failed: {exc}")


async def _generate_pydantic_class(args: dict) -> list[types.TextContent]:
    description = args.get("description", "")
    class_name = args.get("class_name", "GeneratedModel")
    if not description:
        return _err("description is required")
    try:
        try:
            result = _call_module(
                "dspygen.modules.gen_pydantic_class",
                "gen_pydantic_class_call",
                description=description,
                class_name=class_name,
            )
        except (ImportError, AttributeError):
            result = _call_module(
                "dspygen.modules.gen_pydantic_instance",
                "gen_pydantic_instance_call",
                description=description,
            )
        return _ok({"pydantic_code": str(result), "class_name": class_name})
    except Exception as exc:
        logger.exception("generate_pydantic_class error")
        return _err(f"generate_pydantic_class failed: {exc}")


async def _generate_cli_module(args: dict) -> list[types.TextContent]:
    description = args.get("description", "")
    commands = args.get("commands", [])
    if not description:
        return _err("description is required")
    try:
        kwargs: dict = {"description": description}
        if commands:
            kwargs["commands"] = ", ".join(commands)
        result = _call_module(
            "dspygen.modules.gen_cli_module",
            "gen_cli_call",
            **kwargs,
        )
        return _ok({"cli_code": str(result), "commands": commands})
    except Exception as exc:
        logger.exception("generate_cli_module error")
        return _err(f"generate_cli_module failed: {exc}")


async def _generate_jsx(args: dict) -> list[types.TextContent]:
    description = args.get("description", "")
    component_name = args.get("component_name", "GeneratedComponent")
    use_typescript = bool(args.get("use_typescript", False))
    if not description:
        return _err("description is required")
    try:
        try:
            result = _call_module(
                "dspygen.modules.jsx_module",
                "jsx_call",
                description=description,
                component_name=component_name,
            )
        except (ImportError, AttributeError):
            result = _call_module(
                "dspygen.modules.react_jsx_module",
                "react_jsx_call",
                description=description,
                component_name=component_name,
            )
        return _ok({
            "jsx_code": str(result),
            "component_name": component_name,
            "typescript": use_typescript,
        })
    except Exception as exc:
        logger.exception("generate_jsx error")
        return _err(f"generate_jsx failed: {exc}")


async def _ask_dataframe(args: dict) -> list[types.TextContent]:
    question = args.get("question", "")
    csv_data = args.get("csv_data", "")
    file_path = args.get("file_path", "")
    if not question:
        return _err("question is required")
    if not csv_data and not file_path:
        return _err("Either csv_data or file_path is required")
    try:
        if file_path:
            import pandas as pd
            df = pd.read_csv(file_path)
            csv_data = df.to_csv(index=False)

        result = _call_module(
            "dspygen.modules.ask_df_module",
            "ask_df_call",
            question=question,
            df_str=csv_data,
        )
        return _ok({"answer": str(result), "question": question})
    except Exception as exc:
        logger.exception("ask_dataframe error")
        return _err(f"ask_dataframe failed: {exc}")


async def _ask_data(args: dict) -> list[types.TextContent]:
    question = args.get("question", "")
    data_description = args.get("data_description", "")
    if not question or not data_description:
        return _err("question and data_description are required")
    try:
        result = _call_module(
            "dspygen.modules.ask_data_module",
            "ask_data_call",
            question=question,
            data=data_description,
        )
        return _ok({"answer": str(result), "question": question})
    except Exception as exc:
        logger.exception("ask_data error")
        return _err(f"ask_data failed: {exc}")


async def _generate_nuxt_component(args: dict) -> list[types.TextContent]:
    description = args.get("description", "")
    component_name = args.get("component_name", "GeneratedComponent")
    if not description:
        return _err("description is required")
    try:
        result = _call_module(
            "dspygen.modules.nuxt_module",
            "nuxt_call",
            description=description,
            component_name=component_name,
        )
        return _ok({"vue_code": str(result), "component_name": component_name})
    except Exception as exc:
        logger.exception("generate_nuxt_component error")
        return _err(f"generate_nuxt_component failed: {exc}")


async def _chatbot_response(args: dict) -> list[types.TextContent]:
    user_message = args.get("user_message", "")
    system_prompt = args.get("system_prompt", "You are a helpful assistant.")
    conversation_history = args.get("conversation_history", [])
    if not user_message:
        return _err("user_message is required")
    try:
        result = _call_module(
            "dspygen.modules.chatbot_response_generator_module",
            "chatbot_response_generator_call",
            user_message=user_message,
            system_prompt=system_prompt,
        )
        return _ok({"response": str(result), "user_message": user_message})
    except Exception as exc:
        logger.exception("chatbot_response error")
        return _err(f"chatbot_response failed: {exc}")


async def _check_condition(args: dict) -> list[types.TextContent]:
    question = args.get("question", "")
    context = args.get("context", "")
    if not question:
        return _err("question is required")
    try:
        kwargs: dict = {"question": question}
        if context:
            kwargs["context"] = context
        result = _call_module(
            "dspygen.modules.condition_sufficient_info_module",
            "condition_sufficient_info_call",
            **kwargs,
        )
        return _ok({"result": str(result), "question": question, "has_context": bool(context)})
    except Exception as exc:
        logger.exception("check_condition error")
        return _err(f"check_condition failed: {exc}")


async def _generate_test(args: dict) -> list[types.TextContent]:
    code = args.get("code", "")
    test_scenarios = args.get("test_scenarios", [])
    if not code:
        return _err("code is required")
    try:
        try:
            result = _call_module(
                "dspygen.modules.pytest_module",
                "pytest_call",
                code=code,
            )
        except (ImportError, AttributeError):
            result = _call_module(
                "dspygen.modules.gen_module",
                "gen_call",
                signature="code, scenarios -> pytest_tests",
                code=code,
                scenarios=", ".join(test_scenarios) if test_scenarios else "standard",
            )
        return _ok({"test_code": str(result), "scenarios": test_scenarios})
    except Exception as exc:
        logger.exception("generate_test error")
        return _err(f"generate_test failed: {exc}")


async def _optimize_bytecode(args: dict) -> list[types.TextContent]:
    code = args.get("code", "")
    optimization_level = args.get("optimization_level", "moderate")
    if not code:
        return _err("code is required")
    try:
        result = _call_module(
            "dspygen.modules.code_to_bytecode_optimizer_module",
            "code_to_bytecode_optimizer_call",
            code=code,
        )
        return _ok({
            "optimized_code": str(result),
            "optimization_level": optimization_level,
        })
    except Exception as exc:
        logger.exception("optimize_bytecode error")
        return _err(f"optimize_bytecode failed: {exc}")


async def _translate_bpmn_to_bpel(args: dict) -> list[types.TextContent]:
    bpmn_description = args.get("bpmn_description", "")
    process_name = args.get("process_name", "GeneratedProcess")
    if not bpmn_description:
        return _err("bpmn_description is required")
    try:
        result = _call_module(
            "dspygen.modules.bpmn2_bpel_module",
            "bpmn2_bpel_call",
            bpmn_description=bpmn_description,
            process_name=process_name,
        )
        return _ok({"bpel_xml": str(result), "process_name": process_name})
    except Exception as exc:
        logger.exception("translate_bpmn_to_bpel error")
        return _err(f"translate_bpmn_to_bpel failed: {exc}")
