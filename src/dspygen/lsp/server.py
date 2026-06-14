"""
dspygen LSP Server — main entry point.

Start in stdio mode (used by most IDE extensions)::

    python -m dspygen.lsp.server

Or programmatically::

    from dspygen.lsp.server import run_stdio, run_tcp

    run_stdio()            # stdio (default for IDE integrations)
    run_tcp("127.0.0.1", 2087)  # TCP (useful for debugging)
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
    version="v1.0.0",
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
# Register feature providers
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
