"""PEP 561 type stubs for dspygen.lsp."""

from typing import Any

__all__ = ["server", "run_stdio", "run_tcp"]

server: Any

def run_stdio() -> None: ...
def run_tcp(host: str = ..., port: int = ...) -> None: ...
