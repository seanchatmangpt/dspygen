"""
MCP tools for dspygen retrieval modules.

Provides tools to query ChromaDB, web sources, and local Python code.
All dspygen imports are lazy to avoid startup failures.
"""

from __future__ import annotations

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


def _dspygen_root() -> Path:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        if (candidate / "dspygen").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate dspygen source root")


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
    "retrieve_from_chroma",
    "retrieve_from_web",
    "retrieve_from_code",
}


def get_tool_definitions() -> list[types.Tool]:
    """Return the list of Tool descriptors for all retrieval tools."""
    return [
        types.Tool(
            name="retrieve_from_chroma",
            description=(
                "Query a ChromaDB vector collection for semantically similar documents. "
                "Requires a ChromaDB collection to be populated beforehand."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                    },
                    "collection_name": {
                        "type": "string",
                        "description": "ChromaDB collection name",
                        "default": "chatgpt",
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 5,
                    },
                    "role": {
                        "type": "string",
                        "description": "Metadata role filter (default: 'assistant')",
                        "default": "assistant",
                    },
                    "contains": {
                        "type": "string",
                        "description": "Optional substring filter on document content",
                        "default": "",
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="retrieve_from_web",
            description=(
                "Search the web using DuckDuckGo and return a list of results. "
                "Each result includes title, URL, and a short snippet."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Web search query",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Maximum number of search results",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="retrieve_from_code",
            description=(
                "Search local Python source files using CodeRetriever. "
                "The query is used as a glob pattern (e.g. '*.py') to filter files. "
                "Returns file content excerpts."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Glob pattern or filename filter (e.g. '*.py', '*module*')",
                        "default": "*.py",
                    },
                    "directory": {
                        "type": "string",
                        "description": "Absolute path of directory to search (default: dspygen src)",
                        "default": "",
                    },
                    "max_files": {
                        "type": "integer",
                        "description": "Maximum number of files to return",
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

    if name == "retrieve_from_chroma":
        return await _retrieve_from_chroma(arguments)
    if name == "retrieve_from_web":
        return await _retrieve_from_web(arguments)
    if name == "retrieve_from_code":
        return await _retrieve_from_code(arguments)

    return _err(f"Unhandled tool: {name}")


async def _retrieve_from_chroma(args: dict) -> list[types.TextContent]:
    query: str = (args or {}).get("query", "")
    collection_name: str = (args or {}).get("collection_name", "chatgpt")
    k: int = int((args or {}).get("k", 5))
    role: str = (args or {}).get("role", "assistant")
    contains: str = (args or {}).get("contains", "")
    if not query:
        return _err("query argument is required")
    try:
        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.rm.chroma_retriever import ChromaRetriever  # lazy

        retriever = ChromaRetriever(collection_name=collection_name, k=k)
        docs = retriever.forward(
            query_or_queries=query,
            k=k,
            contains=contains if contains else None,
            role=role,
        )
        flat: list[str] = []
        for item in docs:
            if isinstance(item, list):
                flat.extend(item)
            else:
                flat.append(str(item))

        return _ok(
            {
                "collection": collection_name,
                "query": query,
                "results": flat,
                "count": len(flat),
            }
        )
    except Exception as exc:
        logger.exception("retrieve_from_chroma error")
        return _err(f"retrieve_from_chroma failed: {exc}")


async def _retrieve_from_web(args: dict) -> list[types.TextContent]:
    query: str = (args or {}).get("query", "")
    num_results: int = int((args or {}).get("num_results", 5))
    if not query:
        return _err("query argument is required")
    try:
        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.utils.scraping_tools import execute_duckduckgo_queries  # lazy

        results = execute_duckduckgo_queries(
            {query: query}, max_results=num_results
        )
        return _ok({"query": query, "results": results})
    except Exception as exc:
        logger.exception("retrieve_from_web error")
        return _err(f"retrieve_from_web failed: {exc}")


async def _retrieve_from_code(args: dict) -> list[types.TextContent]:
    query: str = (args or {}).get("query", "*.py")
    directory: str = (args or {}).get("directory", "")
    max_files: int = int((args or {}).get("max_files", 10))
    if not directory:
        try:
            directory = str(_dspygen_root() / "dspygen")
        except FileNotFoundError:
            return _err("directory argument is required")
    try:
        src_dir = str(_dspygen_root())
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        from dspygen.rm.code_retriever import CodeRetriever  # lazy

        retriever = CodeRetriever(path=directory)
        prediction = retriever.forward(query=query)
        passages: list[str] = (
            prediction.passages if hasattr(prediction, "passages") else []
        )
        passages = passages[:max_files]

        return _ok(
            {
                "directory": directory,
                "query": query,
                "files_found": len(passages),
                "passages": [p[:500] for p in passages],
            }
        )
    except Exception as exc:
        logger.exception("retrieve_from_code error")
        return _err(f"retrieve_from_code failed: {exc}")
