"""
MCP tools for individual dspygen retrieval module (RM) operations.

Provides named tools for each retrieval module: ChromaDB, Python code,
natural language data, Google Sheets, documents, wizard, structured code
descriptions, and dynamic signatures.

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
    "retrieve_from_chatgpt_chroma",
    "retrieve_from_python_code",
    "retrieve_from_natural_language_data",
    "retrieve_from_google_sheets",
    "retrieve_from_document",
    "retrieve_with_wizard",
    "save_structured_code_description",
    "get_dynamic_signature",
}


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all extended retrieval tools."""
    return [
        types.Tool(
            name="retrieve_from_chatgpt_chroma",
            description=(
                "Query a ChatGPT conversation ChromaDB collection for semantically similar messages. "
                "Uses ChatGPTChromaDBRetriever to search exported ChatGPT history stored in ChromaDB."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Semantic search query"},
                    "collection_name": {
                        "type": "string",
                        "description": "ChromaDB collection name",
                        "default": "chatgpt",
                    },
                    "k": {"type": "integer", "description": "Number of results", "default": 5},
                    "role": {
                        "type": "string",
                        "description": "Filter by role: 'assistant', 'user', or '' for all",
                        "default": "assistant",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="retrieve_from_python_code",
            description=(
                "Search Python source code files using PythonCodeRetriever. "
                "Returns relevant code excerpts based on a semantic query."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Code search query"},
                    "directory": {
                        "type": "string",
                        "description": "Directory to search (default: dspygen source)",
                        "default": "",
                    },
                    "k": {"type": "integer", "description": "Number of results", "default": 5},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="retrieve_from_natural_language_data",
            description=(
                "Retrieve data using natural language queries via NaturalLanguageDataRetriever. "
                "Converts NL questions to structured data lookups."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Natural language data query"},
                    "data_source": {
                        "type": "string",
                        "description": "Data source path or connection string",
                        "default": "",
                    },
                    "k": {"type": "integer", "description": "Maximum results to return", "default": 10},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="retrieve_from_google_sheets",
            description=(
                "Retrieve data from a Google Sheets spreadsheet using GoogleSheetsRetriever. "
                "Returns matching rows based on the query."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "Google Sheets spreadsheet ID",
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "Sheet name (default: first sheet)",
                        "default": "Sheet1",
                    },
                    "k": {"type": "integer", "description": "Maximum rows to return", "default": 10},
                },
                "required": ["query", "spreadsheet_id"],
            },
        ),
        types.Tool(
            name="retrieve_from_document",
            description=(
                "Extract and search text from PDF or DOCX documents using DocRetriever. "
                "Returns relevant passages matching the query."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "file_path": {
                        "type": "string",
                        "description": "Absolute path to the PDF or DOCX file",
                    },
                    "k": {"type": "integer", "description": "Number of passages to return", "default": 5},
                },
                "required": ["query", "file_path"],
            },
        ),
        types.Tool(
            name="retrieve_with_wizard",
            description=(
                "Use the dspygen Wizard retrieval pattern to gather context through "
                "guided, multi-step retrieval. Useful for complex information needs."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Primary information need"},
                    "context": {
                        "type": "string",
                        "description": "Additional context to guide retrieval",
                        "default": "",
                    },
                    "max_steps": {
                        "type": "integer",
                        "description": "Maximum wizard steps",
                        "default": 3,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="save_structured_code_description",
            description=(
                "Save a structured description of Python code to ChromaDB using StructuredCodeDescSaver. "
                "Enables future semantic search over the codebase."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python source code to describe and save"},
                    "collection_name": {
                        "type": "string",
                        "description": "ChromaDB collection to save to",
                        "default": "code_descriptions",
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata to store with the description",
                        "default": {},
                    },
                },
                "required": ["code"],
            },
        ),
        types.Tool(
            name="get_dynamic_signature",
            description=(
                "Generate a dynamic DSPy Signature at runtime using DynamicalSignatureUtil. "
                "Creates a callable Signature class from a description string."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Signature description in 'inputs -> outputs' format",
                    },
                    "execute": {
                        "type": "boolean",
                        "description": "If True, also execute the signature with sample_inputs",
                        "default": False,
                    },
                    "sample_inputs": {
                        "type": "object",
                        "description": "Sample inputs to execute the signature with (if execute=True)",
                        "default": {},
                    },
                },
                "required": ["description"],
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
        "retrieve_from_chatgpt_chroma": _retrieve_from_chatgpt_chroma,
        "retrieve_from_python_code": _retrieve_from_python_code,
        "retrieve_from_natural_language_data": _retrieve_from_natural_language_data,
        "retrieve_from_google_sheets": _retrieve_from_google_sheets,
        "retrieve_from_document": _retrieve_from_document,
        "retrieve_with_wizard": _retrieve_with_wizard,
        "save_structured_code_description": _save_structured_code_description,
        "get_dynamic_signature": _get_dynamic_signature,
    }

    handler = handlers.get(name)
    if handler:
        return await handler(arguments or {})
    return _err(f"Unhandled tool: {name}")


async def _retrieve_from_chatgpt_chroma(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    collection_name = args.get("collection_name", "chatgpt")
    k = int(args.get("k", 5))
    role = args.get("role", "assistant")
    if not query:
        return _err("query is required")
    try:
        from dspygen.rm.chatgpt_chromadb_retriever import ChatGPTChromaDBRetriever  # lazy
        retriever = ChatGPTChromaDBRetriever(collection_name=collection_name, k=k)
        kwargs: dict = {"query_or_queries": query, "k": k}
        if role:
            kwargs["role"] = role
        docs = retriever.forward(**kwargs)
        results = []
        for item in (docs if isinstance(docs, list) else [docs]):
            results.append(str(item)[:1000])
        return _ok({"query": query, "collection": collection_name, "results": results, "count": len(results)})
    except Exception as exc:
        logger.exception("retrieve_from_chatgpt_chroma error")
        return _err(f"retrieve_from_chatgpt_chroma failed: {exc}")


async def _retrieve_from_python_code(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    directory = args.get("directory", "")
    k = int(args.get("k", 5))
    if not query:
        return _err("query is required")
    try:
        from dspygen.rm.python_code_retriever import PythonCodeRetriever  # lazy
        kwargs: dict = {"k": k}
        if directory:
            kwargs["path"] = directory
        retriever = PythonCodeRetriever(**kwargs)
        result = retriever.forward(query=query)
        passages = result.passages if hasattr(result, "passages") else [str(result)]
        return _ok({
            "query": query,
            "directory": directory,
            "passages": [p[:800] for p in passages[:k]],
            "count": len(passages),
        })
    except Exception as exc:
        logger.exception("retrieve_from_python_code error")
        return _err(f"retrieve_from_python_code failed: {exc}")


async def _retrieve_from_natural_language_data(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    data_source = args.get("data_source", "")
    k = int(args.get("k", 10))
    if not query:
        return _err("query is required")
    try:
        from dspygen.rm.natural_language_data_retriever import NaturalLanguageDataRetriever  # lazy
        kwargs: dict = {"k": k}
        if data_source:
            kwargs["data_source"] = data_source
        retriever = NaturalLanguageDataRetriever(**kwargs)
        result = retriever.forward(query=query)
        data = result if isinstance(result, list) else [str(result)]
        return _ok({"query": query, "results": data[:k], "count": len(data)})
    except Exception as exc:
        logger.exception("retrieve_from_natural_language_data error")
        return _err(f"retrieve_from_natural_language_data failed: {exc}")


async def _retrieve_from_google_sheets(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    spreadsheet_id = args.get("spreadsheet_id", "")
    sheet_name = args.get("sheet_name", "Sheet1")
    k = int(args.get("k", 10))
    if not query or not spreadsheet_id:
        return _err("query and spreadsheet_id are required")
    try:
        from dspygen.rm.google_sheets_retriever import GoogleSheetsRetriever  # lazy
        retriever = GoogleSheetsRetriever(
            spreadsheet_id=spreadsheet_id,
            sheet_name=sheet_name,
            k=k,
        )
        result = retriever.forward(query=query)
        rows = result if isinstance(result, list) else [str(result)]
        return _ok({
            "query": query,
            "spreadsheet_id": spreadsheet_id,
            "sheet": sheet_name,
            "rows": rows[:k],
            "count": len(rows),
        })
    except Exception as exc:
        logger.exception("retrieve_from_google_sheets error")
        return _err(f"retrieve_from_google_sheets failed: {exc}")


async def _retrieve_from_document(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    file_path = args.get("file_path", "")
    k = int(args.get("k", 5))
    if not query or not file_path:
        return _err("query and file_path are required")
    try:
        from dspygen.rm.doc_retriever import DocRetriever  # lazy
        retriever = DocRetriever(file_path=file_path, k=k)
        result = retriever.forward(query=query)
        passages = result.passages if hasattr(result, "passages") else [str(result)]
        return _ok({
            "query": query,
            "file": file_path,
            "passages": [p[:1000] for p in passages[:k]],
            "count": len(passages),
        })
    except Exception as exc:
        logger.exception("retrieve_from_document error")
        return _err(f"retrieve_from_document failed: {exc}")


async def _retrieve_with_wizard(args: dict) -> list[types.TextContent]:
    query = args.get("query", "")
    context = args.get("context", "")
    max_steps = int(args.get("max_steps", 3))
    if not query:
        return _err("query is required")
    try:
        from dspygen.rm.wizard import Wizard  # lazy
        wizard = Wizard(max_steps=max_steps)
        result = wizard.forward(query=query, context=context)
        return _ok({
            "query": query,
            "context_provided": bool(context),
            "result": str(result),
            "max_steps": max_steps,
        })
    except Exception as exc:
        logger.exception("retrieve_with_wizard error")
        return _err(f"retrieve_with_wizard failed: {exc}")


async def _save_structured_code_description(args: dict) -> list[types.TextContent]:
    code = args.get("code", "")
    collection_name = args.get("collection_name", "code_descriptions")
    metadata = args.get("metadata", {})
    if not code:
        return _err("code is required")
    try:
        from dspygen.rm.structured_code_desc_saver import StructuredCodeDescSaver  # lazy
        saver = StructuredCodeDescSaver(collection_name=collection_name)
        result = saver.forward(code=code, metadata=metadata)
        return _ok({
            "saved": True,
            "collection": collection_name,
            "code_length": len(code),
            "result": str(result) if result else "Saved successfully",
        })
    except Exception as exc:
        logger.exception("save_structured_code_description error")
        return _err(f"save_structured_code_description failed: {exc}")


async def _get_dynamic_signature(args: dict) -> list[types.TextContent]:
    description = args.get("description", "")
    execute = bool(args.get("execute", False))
    sample_inputs = args.get("sample_inputs", {})
    if not description:
        return _err("description is required")
    try:
        from dspygen.rm.dynamical_signature_util import DynamicalSignatureUtil  # lazy
        util = DynamicalSignatureUtil()
        sig_class = util.create_signature(description)
        result: dict = {
            "description": description,
            "signature_class_name": getattr(sig_class, "__name__", str(sig_class)),
            "inputs": [f for f in dir(sig_class) if not f.startswith("_")],
        }
        if execute and sample_inputs:
            import dspy  # lazy
            pred = dspy.Predict(sig_class)
            execution_result = pred(**sample_inputs)
            result["execution_result"] = str(execution_result)
        return _ok(result)
    except Exception as exc:
        logger.exception("get_dynamic_signature error")
        return _err(f"get_dynamic_signature failed: {exc}")
