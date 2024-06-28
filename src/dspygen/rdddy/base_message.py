import inspect
import uuid
from datetime import datetime
from importlib import import_module
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from dspygen.utils.yaml_tools import YAMLMixin


class BaseMessage(BaseModel):
    """Base message class for serialization/deserialization compatibility with a TypeScript equivalent."""
    data: dict = Field(default_factory=dict, description="Key-value pairs for additional metadata, akin to headers.")
    datacontenttype: str = Field(default='application/json', description="The content type of the data.")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="A unique identifier for the message.")
    pubsubname: str = Field(default='pubsub', description="The name of the pub/sub component.")
    source: str = Field("", description="The Dapr application ID.")
    specversion: str = Field(default='1.0', description="The pubsub spec version.")
    topic: str = Field("", description="The topic name.")
    traceid: str = Field(default_factory=lambda: str(uuid.uuid4()), description="A unique identifier for the trace.")
    traceparent: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The parent trace identifier.")
    tracestate: str = Field(default_factory=lambda: str(uuid.uuid4()), description="The trace state.")
    type: str = Field("", description="The Dapr message type.")

    @property
    def actor_id(self) -> int:
        return self.data.get('actor_id', -1)

    @actor_id.setter
    def actor_id(self, value: int):
        self.data['actor_id'] = value

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
    """Message indicating an actor should be terminated."""


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
