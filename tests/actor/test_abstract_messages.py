# import pytest
# import os
# from pathlib import Path
# import asyncio
# from dspygen.rdddy.base_message import BaseMessage, ExceptionMessage, TerminationMessage,  MessageList
#
# @pytest.fixture
# def message_data():
#     return {
#         "messages": [
#             {
#                 "message_type": "dspygen.rdddy.base_message.ExceptionMessage",
#                 "attributes": {"key": "value1"},
#                 "content": "This is a test message",
#                 "data": {
#                     "content": "This is a test message",
#                     "attributes": {"key": "value1"}
#                 }
#             },
#             {
#                 "message_type": "dspygen.rdddy.base_message.TerminationMessage",
#                 "attributes": {"key": "value2"},
#                 "content": "This is another test message",
#                 "data": {
#                     "content": "This is another test message",
#                     "attributes": {"key": "value2"}
#                 }
#             }
#         ]
#     }
#
# @pytest.fixture
# async def message_list(tmp_path, message_data):
#     file_path = tmp_path / "messages.yaml"
#     messages = [MessageFactory.create_message(msg) for msg in message_data["messages"]]
#     message_list = MessageList(messages=messages)
#     await message_list.ato_yaml(str(file_path))
#     return str(file_path), message_list
#
# @pytest.mark.asyncio
# async def test_aio_context_load(message_list):
#     file_path, original_message_list = await message_list
#
#     async with MessageList.aio_context(file_path=file_path) as loaded_message_list:
#         assert len(loaded_message_list.messages) == len(original_message_list.messages), "Number of messages loaded does not match."
#
# @pytest.mark.asyncio
# async def test_aio_context_save(message_data, tmp_path):
#     file_path = tmp_path / "new_messages.yaml"
#     async with MessageList.aio_context(file_path=str(file_path)) as message_list:
#         for msg_data in message_data["messages"]:
#             message = MessageFactory.create_message(msg_data)
#             message_list.messages.append(message)
#
#     async with MessageList.aio_context(file_path=str(file_path)) as saved_message_list:
#         assert len(saved_message_list.messages) == len(message_data["messages"]), "Not all messages were saved."
#         for msg_data, saved_msg in zip(message_data["messages"], saved_message_list.messages):
#             print("Original message:", msg_data)
#             print("Saved message:", saved_msg)
#             assert saved_msg.data["attributes"] == msg_data["attributes"], "Metadata does not match."
#             assert saved_msg.data["content"] == msg_data["content"], "Content does not match."
#
# @pytest.fixture(autouse=True)
# def cleanup(request, tmp_path):
#     def remove_temp_files():
#         for item in tmp_path.iterdir():
#             if item.is_file():
#                 item.unlink()
#
#     request.addfinalizer(remove_temp_files)
#
# def main():
#     import sys
#     import pytest
#     sys.exit(pytest.main([__file__]))
#
# if __name__ == "__main__":
#     main()
