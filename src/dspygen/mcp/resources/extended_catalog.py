"""
Extended MCP Resources — dspygen catalog v2.

Adds many more MCP Resources beyond the base catalog:
  dspygen://rdddy                    — full RDDDY pattern catalog
  dspygen://signatures/all           — all DSPy signatures as JSON
  dspygen://modules/{name}           — per-module documentation resource
  dspygen://agents/{name}            — per-agent state machine diagram
  dspygen://workflows/examples/{name} — individual workflow examples
  dspygen://lm/providers             — configured LM providers
  dspygen://rm/catalog               — retrieval module catalog
  dspygen://writers/catalog          — writer catalog
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

from loguru import logger
from mcp import types

__all__ = [
    "get_extended_resources",
    "read_extended_resource",
    "EXTENDED_RESOURCE_URIS",
]

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _src_root() -> Path:
    candidate = Path(__file__).resolve()
    for _ in range(8):
        candidate = candidate.parent
        if (candidate / "dspygen").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate dspygen source root")


def _dspygen_root() -> Path:
    return _src_root() / "dspygen"


# ---------------------------------------------------------------------------
# Resource URI registry
# ---------------------------------------------------------------------------

# Static resources
_STATIC_RESOURCES = [
    types.Resource(
        uri="dspygen://rdddy",
        name="RDDDY Pattern Catalog",
        description="Full catalog of RDDDY (Reactive Domain-Driven Design) patterns: aggregates, commands, events, queries, sagas, policies, value objects, and read models.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://signatures/all",
        name="All DSPy Signatures",
        description="Complete list of every DSPy Signature class discovered across the dspygen module library with fields and docstrings.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://lm/providers",
        name="LM Provider Catalog",
        description="Catalog of configured and available language model providers: OpenAI, Ollama, Groq, Cerebras, Anthropic, Google.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://rm/catalog",
        name="Retrieval Module Catalog",
        description="Catalog of all dspygen retrieval modules (RM): ChromaDB, Python code, document, Google Sheets, data, and web retrievers.",
        mimeType="application/json",
    ),
    types.Resource(
        uri="dspygen://writers/catalog",
        name="Writer Catalog",
        description="Catalog of all dspygen writer modules: code_writer, data_writer, google_sheets_writer.",
        mimeType="application/json",
    ),
]

# URI template prefixes for dynamic resources
_DYNAMIC_PREFIXES = [
    "dspygen://modules/",
    "dspygen://agents/",
    "dspygen://workflows/examples/",
]

EXTENDED_RESOURCE_URIS = {r.uri for r in _STATIC_RESOURCES} | set(_DYNAMIC_PREFIXES)


def get_extended_resources() -> list[types.Resource]:
    """Return all extended MCP Resource descriptors (static + template hints)."""
    resources = list(_STATIC_RESOURCES)

    # Add dynamic per-module resources
    try:
        mdir = _dspygen_root() / "modules"
        if mdir.is_dir():
            for p in sorted(mdir.glob("*.py")):
                if p.name == "__init__.py" or p.name.startswith("test"):
                    continue
                resources.append(types.Resource(
                    uri=f"dspygen://modules/{p.stem}",
                    name=f"Module: {p.stem}",
                    description=f"Documentation and signature info for the {p.stem} dspygen module.",
                    mimeType="application/json",
                ))
    except Exception as exc:
        logger.debug(f"Could not enumerate module resources: {exc}")

    # Add dynamic per-agent resources
    try:
        adir = _dspygen_root() / "agents"
        if adir.is_dir():
            for p in sorted(adir.glob("*.py")):
                if p.name == "__init__.py" or p.name.startswith("test"):
                    continue
                resources.append(types.Resource(
                    uri=f"dspygen://agents/{p.stem}",
                    name=f"Agent: {p.stem}",
                    description=f"State machine diagram and info for the {p.stem} FSM agent.",
                    mimeType="application/json",
                ))
    except Exception as exc:
        logger.debug(f"Could not enumerate agent resources: {exc}")

    # Add workflow example resources
    try:
        for yaml_dir in [
            _dspygen_root() / "workflow",
            _dspygen_root() / "llm_pipe" / "examples",
        ]:
            if yaml_dir.is_dir():
                for p in sorted(yaml_dir.glob("*.yaml")):
                    resources.append(types.Resource(
                        uri=f"dspygen://workflows/examples/{p.stem}",
                        name=f"Workflow: {p.stem}",
                        description=f"Workflow/pipeline YAML example: {p.stem}",
                        mimeType="application/yaml",
                    ))
    except Exception as exc:
        logger.debug(f"Could not enumerate workflow resources: {exc}")

    return resources


# ---------------------------------------------------------------------------
# Resource readers
# ---------------------------------------------------------------------------


def _extract_ast_meta(path: Path) -> dict[str, Any]:
    """Quick AST scan returning docstring, class names, and Signature subclasses."""
    meta: dict[str, Any] = {
        "name": path.stem,
        "file": str(path),
        "docstring": "",
        "classes": [],
        "signatures": [],
        "input_fields": [],
        "output_fields": [],
    }
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return meta

    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
    ):
        meta["docstring"] = tree.body[0].value.value.strip()[:600]  # type: ignore[union-attr]

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [
            ast.unparse(b) if hasattr(ast, "unparse") else getattr(b, "id", "")
            for b in node.bases
        ]
        meta["classes"].append({"name": node.name, "bases": bases})
        if any("Signature" in b for b in bases):
            meta["signatures"].append(node.name)
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if not isinstance(target, ast.Name):
                            continue
                        if not isinstance(item.value, ast.Call):
                            continue
                        func_name = ""
                        if isinstance(item.value.func, ast.Attribute):
                            func_name = item.value.func.attr
                        elif isinstance(item.value.func, ast.Name):
                            func_name = item.value.func.id
                        if func_name == "InputField":
                            meta["input_fields"].append(target.id)
                        elif func_name == "OutputField":
                            meta["output_fields"].append(target.id)
    return meta


def _build_rdddy_catalog() -> dict:
    """Build the RDDDY pattern catalog."""
    patterns = {
        "aggregate": {
            "description": "Domain aggregate root — encapsulates cluster of domain objects. Enforces invariants.",
            "base_class": "BaseAggregate",
            "file": "base_aggregate.py",
            "use_when": "You need a consistency boundary around a group of domain objects.",
        },
        "command": {
            "description": "Intent to change system state. Commands are named in imperative mood.",
            "base_class": "BaseCommand",
            "file": "base_command.py",
            "use_when": "Something is being requested of the system that changes state.",
        },
        "event": {
            "description": "Something that happened in the domain. Events are named in past tense.",
            "base_class": "BaseEvent",
            "file": "base_event.py",
            "use_when": "Recording facts about what happened in the system.",
        },
        "query": {
            "description": "Request for information without side effects (CQRS read side).",
            "base_class": "BaseQuery",
            "file": "base_query.py",
            "use_when": "Fetching data without changing state.",
        },
        "saga": {
            "description": "Long-running business process that coordinates multiple aggregates.",
            "base_class": "BaseSaga",
            "file": "base_saga.py",
            "use_when": "Multi-step business process that may span multiple aggregates or services.",
        },
        "policy": {
            "description": "Business rule that reacts to domain events and issues commands.",
            "base_class": "BasePolicy",
            "file": "base_policy.py",
            "use_when": "Automating reactions to domain events based on business rules.",
        },
        "value_object": {
            "description": "Immutable domain concept defined entirely by its attributes.",
            "base_class": "BaseValueObject",
            "file": "base_value_object.py",
            "use_when": "Modeling domain concepts that have no identity, only attributes.",
        },
        "read_model": {
            "description": "Denormalized view model optimized for querying (CQRS read side).",
            "base_class": "BaseReadModel",
            "file": "base_read_model.py",
            "use_when": "Creating efficient read views tailored to specific UI or API needs.",
        },
        "inhabitant": {
            "description": "ServiceColony actor that processes messages and coordinates with peers.",
            "base_class": "BaseInhabitant",
            "file": "base_inhabitant.py",
            "use_when": "Building reactive actors in a service colony system.",
        },
        "message": {
            "description": "Base message type for all RDDDY communications.",
            "base_class": "BaseMessage",
            "file": "base_message.py",
            "use_when": "As the common base when the specific message type is not yet determined.",
        },
    }

    # Enrich with source file existence
    rdddy_dir = _dspygen_root() / "rdddy"
    for pattern_name, info in patterns.items():
        file_path = rdddy_dir / info["file"]
        info["exists"] = file_path.is_file()  # type: ignore[assignment]
        info["mcp_tool"] = f"create_{pattern_name}" if pattern_name not in ("message",) else None

    return {
        "patterns": patterns,
        "rdddy_directory": str(rdddy_dir),
        "pattern_count": len(patterns),
        "event_storm_tool": "event_storm",
        "scaffold_tool": "scaffold_domain",
        "description": "RDDDY = Reactive Domain-Driven Design for You — a dspygen framework for DDD patterns.",
    }


def _build_lm_providers_catalog() -> dict:
    """Build the LM provider catalog."""
    import os
    providers = {
        "openai": {
            "env_key": "OPENAI_API_KEY",
            "configured": bool(os.environ.get("OPENAI_API_KEY")),
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "o1", "o1-mini"],
            "prefix": "openai/",
            "dspy_example": "dspy.LM('openai/gpt-4o')",
        },
        "ollama": {
            "env_key": "OLLAMA_HOST",
            "configured": bool(os.environ.get("OLLAMA_HOST")),
            "models": ["llama3.2", "llama3.1", "codellama", "mistral", "phi3", "gemma2", "qwen2.5"],
            "prefix": "ollama_chat/",
            "dspy_example": "dspy.LM('ollama_chat/llama3.2', api_base='http://localhost:11434')",
        },
        "groq": {
            "env_key": "GROQ_API_KEY",
            "configured": bool(os.environ.get("GROQ_API_KEY")),
            "models": ["groq/llama-3.1-70b-versatile", "groq/llama-3.1-8b-instant", "groq/mixtral-8x7b-32768"],
            "prefix": "groq/",
            "dspy_example": "dspy.LM('groq/llama-3.1-70b-versatile')",
        },
        "cerebras": {
            "env_key": "CEREBRAS_API_KEY",
            "configured": bool(os.environ.get("CEREBRAS_API_KEY")),
            "models": ["cerebras/llama3.1-8b", "cerebras/llama3.1-70b"],
            "prefix": "cerebras/",
            "dspy_example": "dspy.LM('cerebras/llama3.1-70b')",
        },
        "anthropic": {
            "env_key": "ANTHROPIC_API_KEY",
            "configured": bool(os.environ.get("ANTHROPIC_API_KEY")),
            "models": ["claude-opus-4-5", "claude-sonnet-4-5", "claude-haiku-3-5"],
            "prefix": "anthropic/",
            "dspy_example": "dspy.LM('anthropic/claude-sonnet-4-5')",
        },
        "google": {
            "env_key": "GOOGLE_API_KEY",
            "configured": bool(os.environ.get("GOOGLE_API_KEY")),
            "models": ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash", "gemini/gemini-2.0-flash"],
            "prefix": "gemini/",
            "dspy_example": "dspy.LM('gemini/gemini-1.5-pro')",
        },
    }

    # Check current dspy config
    current_lm = None
    try:
        import dspy
        lm = dspy.settings.lm
        if lm is not None:
            current_lm = {
                "model": getattr(lm, "model", str(lm)),
                "provider": getattr(lm, "provider", "unknown"),
            }
    except Exception:
        pass

    return {
        "current_lm": current_lm,
        "providers": providers,
        "configure_tool": "configure_lm",
        "list_tool": "list_available_models",
    }


def _build_rm_catalog() -> dict:
    """Build the retrieval module catalog."""
    rm_modules = [
        {
            "name": "ChatGPTChromaDBRetriever",
            "file": "chatgpt_chromadb_retriever.py",
            "description": "Query ChatGPT conversation history stored in ChromaDB.",
            "mcp_tool": "retrieve_from_chatgpt_chroma",
            "inputs": ["query", "collection_name", "k", "role"],
        },
        {
            "name": "PythonCodeRetriever",
            "file": "python_code_retriever.py",
            "description": "Search Python source code files semantically.",
            "mcp_tool": "retrieve_from_python_code",
            "inputs": ["query", "directory", "k"],
        },
        {
            "name": "NaturalLanguageDataRetriever",
            "file": "natural_language_data_retriever.py",
            "description": "Convert NL questions to structured data lookups.",
            "mcp_tool": "retrieve_from_natural_language_data",
            "inputs": ["query", "data_source", "k"],
        },
        {
            "name": "GoogleSheetsRetriever",
            "file": "google_sheets_retriever.py",
            "description": "Retrieve rows from Google Sheets by semantic query.",
            "mcp_tool": "retrieve_from_google_sheets",
            "inputs": ["query", "spreadsheet_id", "sheet_name"],
        },
        {
            "name": "DocRetriever",
            "file": "doc_retriever.py",
            "description": "Extract and search text from PDF or DOCX files.",
            "mcp_tool": "retrieve_from_document",
            "inputs": ["query", "file_path", "k"],
        },
        {
            "name": "Wizard",
            "file": "wizard.py",
            "description": "Multi-step guided retrieval wizard.",
            "mcp_tool": "retrieve_with_wizard",
            "inputs": ["query", "context", "max_steps"],
        },
        {
            "name": "StructuredCodeDescSaver",
            "file": "structured_code_desc_saver.py",
            "description": "Save structured code descriptions to ChromaDB for later retrieval.",
            "mcp_tool": "save_structured_code_description",
            "inputs": ["code", "collection_name", "metadata"],
        },
        {
            "name": "DynamicalSignatureUtil",
            "file": "dynamical_signature_util.py",
            "description": "Generate dynamic DSPy Signatures at runtime from descriptions.",
            "mcp_tool": "get_dynamic_signature",
            "inputs": ["description", "execute", "sample_inputs"],
        },
        {
            "name": "ChromaRetriever",
            "file": "chroma_retriever.py",
            "description": "Generic ChromaDB vector retrieval (generic).",
            "mcp_tool": "retrieve_from_chroma",
            "inputs": ["query", "collection_name", "k", "role", "contains"],
        },
        {
            "name": "WebRetriever",
            "file": "web_retriever.py",
            "description": "Retrieve web content by URL or query.",
            "mcp_tool": "retrieve_from_web",
            "inputs": ["query", "num_results"],
        },
    ]

    # Check which RM files exist
    rm_dir = _dspygen_root() / "rm"
    for rm in rm_modules:
        rm["exists"] = (rm_dir / rm["file"]).is_file()  # type: ignore[assignment, operator]

    return {
        "retrieval_modules": rm_modules,
        "rm_directory": str(rm_dir),
        "count": len(rm_modules),
    }


def _build_writers_catalog() -> dict:
    """Build the writer catalog."""
    writers = [
        {
            "name": "code_writer",
            "description": "Generate and write Python source code files.",
            "module": "dspygen.writer.code_writer",
            "call_fn": "code_writer_call",
            "inputs": ["source"],
        },
        {
            "name": "data_writer",
            "description": "Write structured data (JSON, CSV, etc.) to files.",
            "module": "dspygen.writer.data_writer",
            "call_fn": "data_writer_call",
            "inputs": ["data", "format"],
        },
        {
            "name": "google_sheets_writer",
            "description": "Write data to Google Sheets spreadsheets.",
            "module": "dspygen.writer.google_sheets_writer",
            "call_fn": "google_sheets_writer_call",
            "inputs": ["data", "spreadsheet_id", "sheet_name"],
        },
    ]

    writer_dir = _dspygen_root() / "writer"
    for w in writers:
        module_file = writer_dir / f"{w['name']}.py"
        w["exists"] = module_file.is_file()  # type: ignore[assignment]

    return {
        "writers": writers,
        "writer_directory": str(writer_dir),
        "count": len(writers),
        "mcp_tools": ["list_writers", "run_writer", "generate_from_template"],
    }


def _build_all_signatures_catalog() -> list[dict]:
    """Return every DSPy Signature found across all modules."""
    try:
        mdir = _dspygen_root() / "modules"
        if not mdir.is_dir():
            return []
    except Exception:
        return []

    sigs = []
    for p in sorted(mdir.glob("*.py")):
        if p.name == "__init__.py" or p.name.startswith("test"):
            continue
        meta = _extract_ast_meta(p)
        for sig_name in meta["signatures"]:
            sigs.append({
                "module": meta["name"],
                "signature_class": sig_name,
                "docstring": meta["docstring"][:300],
                "input_fields": meta["input_fields"],
                "output_fields": meta["output_fields"],
                "file": meta["file"],
            })
    return sigs


def _build_module_detail(module_name: str) -> dict:
    """Build detailed info for a specific module."""
    try:
        mdir = _dspygen_root() / "modules"
        path = mdir / f"{module_name}.py"
        if not path.is_file():
            return {"error": f"Module '{module_name}' not found"}
        meta = _extract_ast_meta(path)
        try:
            source = path.read_text(encoding="utf-8")
            meta["source_preview"] = source[:1000]
        except Exception:
            pass
        return meta
    except Exception as exc:
        return {"error": str(exc)}


def _build_agent_detail(agent_name: str) -> dict:
    """Build detailed info for a specific agent."""
    try:
        adir = _dspygen_root() / "agents"
        path = adir / f"{agent_name}.py"
        if not path.is_file():
            return {"error": f"Agent '{agent_name}' not found"}
        meta = _extract_ast_meta(path)

        # Extract FSM states
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            transitions: list[Any] = []
            states = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    bases = [
                        ast.unparse(b) if hasattr(ast, "unparse") else ""
                        for b in node.bases
                    ]
                    if any("Enum" in b for b in bases):
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for t in item.targets:
                                    if isinstance(t, ast.Name):
                                        states.append(t.id)
            meta["fsm_states"] = states

            # Try to generate a simple mermaid state diagram
            if states:
                mmd_lines = ["stateDiagram-v2"]
                for i, state in enumerate(states):
                    if i < len(states) - 1:
                        mmd_lines.append(f"    {state} --> {states[i + 1]}")
                meta["mermaid_diagram"] = "\n".join(mmd_lines)
        except Exception:
            pass

        return meta
    except Exception as exc:
        return {"error": str(exc)}


def _build_workflow_detail(workflow_name: str) -> dict:
    """Build detail for a specific workflow example."""
    try:
        for yaml_dir in [
            _dspygen_root() / "workflow",
            _dspygen_root() / "llm_pipe" / "examples",
        ]:
            if not yaml_dir.is_dir():
                continue
            path = yaml_dir / f"{workflow_name}.yaml"
            if path.is_file():
                try:
                    content = path.read_text(encoding="utf-8")
                    return {
                        "name": workflow_name,
                        "file": str(path),
                        "content": content,
                        "size": len(content),
                    }
                except Exception as exc:
                    return {"error": str(exc)}
        return {"error": f"Workflow '{workflow_name}' not found"}
    except Exception as exc:
        return {"error": str(exc)}


def read_extended_resource(uri: str) -> str | None:
    """
    Read a resource by URI.

    Returns JSON string if this module handles the URI, or None if unknown.
    """
    try:
        if uri == "dspygen://rdddy":
            return json.dumps(_build_rdddy_catalog(), indent=2)
        if uri == "dspygen://signatures/all":
            return json.dumps(_build_all_signatures_catalog(), indent=2)
        if uri == "dspygen://lm/providers":
            return json.dumps(_build_lm_providers_catalog(), indent=2)
        if uri == "dspygen://rm/catalog":
            return json.dumps(_build_rm_catalog(), indent=2)
        if uri == "dspygen://writers/catalog":
            return json.dumps(_build_writers_catalog(), indent=2)
        if uri.startswith("dspygen://modules/"):
            module_name = uri[len("dspygen://modules/"):]
            return json.dumps(_build_module_detail(module_name), indent=2)
        if uri.startswith("dspygen://agents/"):
            agent_name = uri[len("dspygen://agents/"):]
            return json.dumps(_build_agent_detail(agent_name), indent=2)
        if uri.startswith("dspygen://workflows/examples/"):
            workflow_name = uri[len("dspygen://workflows/examples/"):]
            data = _build_workflow_detail(workflow_name)
            # Return raw YAML content for workflow files
            if "content" in data:
                return data["content"]  # type: ignore[no-any-return]
            return json.dumps(data, indent=2)

        return None  # Unknown URI — not handled here
    except Exception as exc:
        logger.exception(f"read_extended_resource error for {uri!r}")
        return json.dumps({"error": str(exc)})
