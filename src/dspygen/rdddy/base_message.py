import inspect
import uuid
from datetime import datetime, timezone

from pydantic import Field

from dslmodel import DSLModel



class BaseMessage(DSLModel):
    """Base message class for the Exodus Service Colony framework, designed to facilitate communication
    between autonomous services."""

    # Identification fields
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="A unique identifier for the message.")
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                                description="A unique identifier used for message correlation.")

    # Metadata fields
    message_type: str = Field(None, description="The type of the message, e.g., proposal, vote, command.")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(),
                           description="The timestamp when the message was created.")

    # Data payload
    payload: dict = Field(default_factory=dict,
                          description="The main content of the message, typically containing the data relevant to the action or event.")

    # Optional tracing fields
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                          description="A unique identifier for tracing the message flow.")
    trace_context: dict = Field(default_factory=dict, description="Additional context for tracing the message flow.")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "correlation_id": "123e4567-e89b-12d3-a456-426614174001",
                "message_type": "proposal",
                "timestamp": "2023-08-20T15:41:05.235Z",
                "payload": {
                    "proposal_id": "prop-001",
                    "description": "Proposal for new service integration.",
                    "details": {"service_name": "NewAnalyticsService", "capabilities": ["data-mining", "AI-analysis"]}
                },
                "trace_id": "123e4567-e89b-12d3-a456-426614174002",
                "trace_context": {"parent_id": "123e4567-e89b-12d3-a456-426614174003"}
            }
        }

    @property
    def sender(self) -> str:
        return self.source_loa

    @sender.setter
    def sender(self, value: str):
        self.source_loa = value

    @property
    def receiver(self) -> str:
        return self.target_loa

    @receiver.setter
    def receiver(self, value: str):
        self.target_loa = value

    @property
    def message_content(self) -> dict:
        return self.payload

    @property
    def created_at(self) -> str:
        return self.timestamp

    @property
    def full_message_type(self) -> str:
        """Returns the full import path of the message class."""
        module = inspect.getmodule(self)
        return f"{module.__name__}.{self.__class__.__name__}"


class MessageList(DSLModel):
    messages: list[BaseMessage] = []


class ExceptionMessage(BaseMessage):
    """Generic exception message"""


class TerminationMessage(BaseMessage):
    """Message indicating an actor should be terminated."""

