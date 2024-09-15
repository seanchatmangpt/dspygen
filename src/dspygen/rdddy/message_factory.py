from importlib import import_module

from dspygen.rdddy.base_message import BaseMessage


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
