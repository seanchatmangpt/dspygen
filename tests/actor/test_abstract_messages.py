import pytest
import os
from pydantic import BaseModel
import asyncio

from dspygen.rdddy.abstract_message import *


# Import your classes here, assuming they're defined in the same file or appropriately imported


@pytest.fixture
def message_data():
    # Providing a fixture for sample message data
    return {
        "messages": [
            ExceptionMessage(
                metadata={"key": "value1"},
                content="This is a test message",
            ).model_dump(),
            TerminationMessage(
                metadata={"key": "value2"},
                content="This is another test message",
            ).model_dump()
        ]
    }


@pytest.fixture
async def message_list(tmp_path, message_data):
    # Create a temporary YAML file and save the message list to it
    file_path = tmp_path / "messages.yaml"
    messages = [MessageFactory.create_message(msg) for msg in message_data["messages"]]
    message_list = MessageList(messages=messages)
    await message_list.ato_yaml(str(file_path))
    return str(file_path), message_list


@pytest.mark.asyncio
async def test_aio_context_load(message_list):
    file_path, original_message_list = await message_list  # Add await here

    async with MessageList.aio_context(file_path=file_path) as loaded_message_list:
        assert len(loaded_message_list.messages) == len(original_message_list.messages), "Number of messages loaded does not match."


@pytest.mark.asyncio
async def test_aio_context_save(message_data, tmp_path):
    file_path = tmp_path / "new_messages.yaml"
    async with MessageList.aio_context(file_path=str(file_path)) as message_list:
        for msg_data in message_data["messages"]:
            message = MessageFactory.create_message(msg_data)
            message_list.messages.append(message)

    # Read back the file to ensure data was saved correctly
    async with MessageList.aio_context(file_path=str(file_path)) as saved_message_list:
        assert len(saved_message_list.messages) == len(message_data["messages"]), "Not all messages were saved."
        for msg_data, saved_msg in zip(message_data["messages"], saved_message_list.messages):
            assert saved_msg.metadata == msg_data["metadata"], "Metadata does not match."
            assert saved_msg.content == msg_data["content"], "Content does not match."


@pytest.fixture(autouse=True)
def cleanup(request, tmp_path):
    # Cleanup: Remove temporary files after each test
    def remove_temp_files():
        for item in tmp_path.iterdir():
            if item.is_file():
                item.unlink()

    request.addfinalizer(remove_temp_files)
