import inspect
import uuid
from datetime import datetime, timezone
from importlib import import_module
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from dspygen.utils.yaml_tools import YAMLMixin


class BaseMessage(BaseModel):
    """Base message class for serialization/deserialization compatibility with AsyncAPI."""

    # Identification fields
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="A unique identifier for the message.")
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                                description="A unique identifier used for message correlation.")

    # Metadata fields
    type: str = Field(None, description="The message type, often corresponding to an event or action.")
    content_type: str = Field(default='application/json', description="The content type of the message payload.")
    source: str = Field("service_colony", description="The source of the message, usually a service or application ID.")
    time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat(),
                      description="The timestamp of when the message was created.")    # Data payload

    data: dict = Field(default_factory=dict,
                       description="The main payload of the message, typically containing the business data.")

    # Optional tracing fields
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()),
                          description="A unique identifier for tracing the message flow.")
    trace_parent: str = Field(default_factory=lambda: str(uuid.uuid4()),
                              description="The parent trace identifier, if applicable.")
    trace_state: str = Field(default_factory=lambda: str(uuid.uuid4()),
                             description="Additional trace state information, if applicable.")

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "correlation_id": "123e4567-e89b-12d3-a456-426614174001",
                "type": "order.created",
                "content_type": "application/json",
                "source": "order-service",
                "time": "2023-08-20T15:41:05.235Z",
                "data": {
                    "order_id": "abc123",
                    "user_id": "user456",
                    "amount": 99.99
                },
                "trace_id": "123e4567-e89b-12d3-a456-426614174002",
                "trace_parent": "123e4567-e89b-12d3-a456-426614174003",
                "trace_state": "123e4567-e89b-12d3-a456-426614174004"
            }
        }

    @property
    def inhabitant_id(self) -> int:
        return self.data.get('inhabitant_id', -1)

    @inhabitant_id.setter
    def inhabitant_id(self, value: int):
        self.data['inhabitant_id'] = value

    @property
    def content(self) -> str:
        return self.data.get('content', '')

    @property
    def timestamp(self) -> int:
        return self.data.get('timestamp', int(datetime.now().timestamp() * 1000))

    @property
    def message_type(self) -> str:
        """Calculate the relative import path of the class."""
        module = inspect.getmodule(self)
        relative_path = f"{module.__name__}.{self.__class__.__name__}"
        return relative_path


class MessageList(YAMLMixin, BaseModel):
    messages: list[BaseMessage] = []


class ExceptionMessage(BaseMessage):
    """Generic exception message"""


class TerminationMessage(BaseMessage):
    """Message indicating an inhabitant should be terminated."""


T = TypeVar("T", bound="Message")


class MessageFactory:
    """Factory class to convert YAML data into appropriate Message types."""

    @classmethod
    def create_message(cls, data: dict) -> BaseMessage:
        """Create a message of the appropriate type based on the data provided.

        Parameters:
        - data (dict): A dictionary containing the message data.

        Returns:
        - BaseMessage: The appropriate message type.
        """
        message_class = cls._get_message_class(data["message_type"])
        return message_class(**data)

    @classmethod
    def create_messages_from_list(cls, data_list: list[dict]) -> list[BaseMessage]:
        """Create a list of messages from a list of YAML data dictionaries.

        Parameters:
        - data_list (List[dict]): A list of dictionaries containing message data.

        Returns:
        - List[BaseMessage]: A list of appropriate message types.
        """
        messages = [cls.create_message(data) for data in data_list]
        return messages

    @classmethod
    def _get_message_class(cls, module_name: str) -> type[BaseMessage]:
        """Get the message class corresponding to the module name. Import the module if not already imported.

        Parameters:
        - module_name (str): The module name containing the message class.

        Returns:
        - Type[BaseMessage]: The message class.
        """
        module_path, class_name = module_name.rsplit(".", 1)
        module = import_module(module_path)
        message_class = getattr(module, class_name)
        return message_class
