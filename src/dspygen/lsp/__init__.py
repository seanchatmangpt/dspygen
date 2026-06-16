"""
dspygen LSP — Language Server Protocol server for dspygen/DSPy.

Entry points::

    from dspygen.lsp.server import run_stdio, run_tcp

    # Stdio mode (used by most IDE extensions):
    run_stdio()

    # TCP mode (useful for debugging):
    run_tcp(host="127.0.0.1", port=2087)
"""

from .server import run_stdio, run_tcp, server

__version__ = "1.1.0"

__all__ = ["run_stdio", "run_tcp", "server", "__version__"]
