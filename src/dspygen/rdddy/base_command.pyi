"""PEP 561 type stubs for dspygen.rdddy.base_command."""

from dspygen.rdddy.base_message import BaseMessage

__all__ = ["BaseCommand"]


class BaseCommand(BaseMessage):
    """AbstractCommand message type."""
