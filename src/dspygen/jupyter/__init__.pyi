"""PEP 561 type stubs for dspygen.jupyter."""

from typing import Any

__all__ = ["load_ipython_extension", "unload_ipython_extension"]


def load_ipython_extension(ip: Any) -> None: ...
def unload_ipython_extension(ip: Any) -> None: ...
