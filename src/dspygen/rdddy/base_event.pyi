"""PEP 561 type stubs for dspygen.rdddy.base_event."""

from dspygen.rdddy.base_message import BaseMessage

__all__ = ["BaseEvent"]


class BaseEvent(BaseMessage):
    """Event message type."""
