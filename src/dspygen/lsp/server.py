"""
dspygen LSP Server — main entry point.

Start in stdio mode (used by most IDE extensions)::

    python -m dspygen.lsp.server

Or programmatically::

    from dspygen.lsp.server import run_stdio, run_tcp

    run_stdio()            # stdio (default for IDE integrations)
    run_tcp("127.0.0.1", 2087)  # TCP (useful for debugging)

Capabilities implemented
------------------------
- textDocument/completion
- textDocument/hover
- textDocument/publishDiagnostics (via didOpen / didChange)
- textDocument/definition
- textDocument/documentSymbol
- workspace/symbol
- textDocument/rename  (+prepareRename)
- textDocument/codeAction
- textDocument/semanticTokens/full
- textDocument/formatting
- textDocument/references
- textDocument/inlayHint
- textDocument/foldingRange
- textDocument/prepareCallHierarchy / callHierarchy/incomingCalls / callHierarchy/outgoingCalls
- workspace/executeCommand
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger
from lsprotocol import types as lsp_types
from pygls.lsp.server import LanguageServer

# ---------------------------------------------------------------------------
# Logging — write to a file, NOT stdout (stdout is the LSP channel)
# ---------------------------------------------------------------------------

_LOG_PATH = Path.home() / ".cache" / "dspygen" / "lsp.log"
_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logger.remove()  # Remove default stderr handler
logger.add(
    str(_LOG_PATH),
    level="DEBUG",
    rotation="10 MB",
    retention=3,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} — {message}",
    enqueue=True,  # Thread-safe async write
)

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

server = LanguageServer(
    name="dspygen-lsp",
    version="v1.1.0",
    text_document_sync_kind=lsp_types.TextDocumentSyncKind.Incremental,
)

# ---------------------------------------------------------------------------
# Initialize handler — build the module index once at startup
# ---------------------------------------------------------------------------


@server.feature(lsp_types.INITIALIZE)
def on_initialize(params: lsp_types.InitializeParams) -> None:
    """Called by the LSP client after the connection is established."""
    try:
        logger.info("dspygen-lsp: initialising …")
        from ._state import build_state  # noqa: PLC0415

        build_state()
        logger.info("dspygen-lsp: module index ready")
    except Exception as exc:  # noqa: BLE001
        logger.exception(f"dspygen-lsp: error during initialisation: {exc}")


# ---------------------------------------------------------------------------
# Register feature providers — original 4
# ---------------------------------------------------------------------------

from .providers.completion import register_completion  # noqa: E402
from .providers.definition import register_definition  # noqa: E402
from .providers.diagnostics import register_diagnostics  # noqa: E402
from .providers.hover import register_hover  # noqa: E402

register_completion(server)
register_hover(server)
register_diagnostics(server)
register_definition(server)

# ---------------------------------------------------------------------------
# Register feature providers — 10 new capabilities
# ---------------------------------------------------------------------------

from .providers.call_hierarchy import register_call_hierarchy  # noqa: E402
from .providers.code_action import register_code_action  # noqa: E402
from .providers.document_symbol import register_document_symbol  # noqa: E402
from .providers.execute_command import register_execute_command  # noqa: E402
from .providers.folding_range import register_folding_range  # noqa: E402
from .providers.formatting import register_formatting  # noqa: E402
from .providers.inlay_hint import register_inlay_hint  # noqa: E402
from .providers.references import register_references  # noqa: E402
from .providers.rename import register_rename  # noqa: E402
from .providers.semantic_tokens import register_semantic_tokens  # noqa: E402
from .providers.workspace_symbol import register_workspace_symbol  # noqa: E402

register_document_symbol(server)
register_workspace_symbol(server)
register_rename(server)
register_code_action(server)
register_semantic_tokens(server)
register_formatting(server)
register_references(server)
register_inlay_hint(server)
register_folding_range(server)
register_call_hierarchy(server)
register_execute_command(server)

# ---------------------------------------------------------------------------
# Public run helpers
# ---------------------------------------------------------------------------


def run_stdio() -> None:
    """Start the server in stdio mode.  Use this for most IDE integrations."""
    logger.info("dspygen-lsp: starting in stdio mode")
    server.start_io()


def run_tcp(host: str = "127.0.0.1", port: int = 2087) -> None:
    """Start the server in TCP mode.  Useful for debugging with netcat / telnet."""
    logger.info(f"dspygen-lsp: starting TCP server on {host}:{port}")
    server.start_tcp(host, port)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "tcp":
        host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 2087
        run_tcp(host, port)
    else:
        run_stdio()
