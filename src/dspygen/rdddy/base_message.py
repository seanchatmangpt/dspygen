import inspect
import uuid
from datetime import datetime
from importlib import import_module
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from dspygen.utils.yaml_tools import YAMLMixin


class BaseMessage(BaseModel):
    """Base message class for serialization/deserialization compatibility with a TypeScript equivalent."""
    actor_id: int = Field(default=-1, description="Unique identifier for the actor that sent the message.")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Universally unique identifier for the message.")
    topic: str = Field(default="default-topic", description="Represents the channel, topic, queue, or subject the message pertains to.")
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000), description="Epoch time in milliseconds for when the message was created or sent.")
    content_type: str = Field(default="application/json", description="MIME type indicating the format of the content.")
    content: str = Field(default="", description="The payload of the message, typically in a serialized format.")
    attributes: dict = Field(default_factory=dict, description="Key-value pairs for additional metadata, akin to headers.")

    def __init__(self, **data: Any):
        super().__init__(**data)
        # Ensure that the 'messageType' attribute exists in the attributes dictionary
        self.attributes.setdefault('messageType', type(self).__name__)


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
    def create_message(cls, data: dict) -> T:
        """Create a message of the appropriate type based on the data provided.

        Parameters:
        - data (dict): A dictionary containing the message data.

        Returns:
        - Type[BaseModel]: The appropriate message type.
        """
        # message_class = cls._get_message_class(data["message_type"])
        return BaseMessage(**data)

    @classmethod
    def create_messages_from_list(cls, data_list: list[dict]) -> list[T]:
        """Create a list of messages from a list of YAML data dictionaries.

        Parameters:
        - data_list (List[dict]): A list of dictionaries containing message  data.

        Returns:
        - List[Type[BaseModel]]: A list of appropriate message types.
        """
        messages = [cls.create_message(data) for data in data_list]
        return messages

    @classmethod
    def _get_message_class(cls, module_name: str) -> type[T]:
        """Get the message class corresponding to the module name. Import the module if not already imported.

        Parameters:
        - module_name (str): The module name containing the message class.

        Returns:
        - Type[BaseModel]: The message class.
        """
        # module_name = 'livingcharter.domain.collaboration_context.AgentCreated'
        # slice off the last period
        module_path, class_name = module_name.rsplit(".", 1)

        # Assuming that the message class is named the same as the last part of the module name
        module = import_module(module_path)
        message_class = getattr(module, class_name)

        return message_class
