import inspect
from importlib import import_module
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from dspygen.utils.yaml_tools import YAMLMixin


class BaseMessage(YAMLMixin, BaseModel):
    """Message class using Pydantic for data validation and serialization."""

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    actor_id: int = Field(default=-1, description="The ID of the actor that sent the message. -1 means it was published by the system.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Metadata for the message.")
    content: str | None = Field(default=None, description="The content of the message.")
    message_type: str = Field(default="", description="The type of the message.")

    def __init__(self, **data):
        super().__init__(**data)
        # Calculate the relative import path at runtime
        self.message_type = self._calculate_import_path()

    def _calculate_import_path(self) -> str:
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
    def create_message(cls, data: dict) -> T:
        """Create a message of the appropriate type based on the data provided.

        Parameters:
        - data (dict): A dictionary containing the message data.

        Returns:
        - Type[BaseModel]: The appropriate message type.
        """
        message_class = cls._get_message_class(data["message_type"])
        return message_class(**data)

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
