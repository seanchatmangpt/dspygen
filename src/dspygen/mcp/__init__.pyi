"""PEP 561 type stubs for dspygen.mcp."""

from typing import Any

__all__ = ["create_server", "run_stdio", "run_sse"]


def create_server() -> Any: ...
def run_stdio() -> None: ...
def run_sse(app: Any = ...) -> Any: ...
