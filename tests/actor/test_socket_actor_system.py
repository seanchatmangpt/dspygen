from unittest.mock import AsyncMock

from dspygen.rdddy.abstract_query import AbstractQuery
from dspygen.rdddy.actor_system import ActorSystem
import pytest


@pytest.fixture()
def actor_system(event_loop):
    # Provide the event loop to the actor system
    system = ActorSystem(event_loop)
    # Mock the send_message_over_socket method
    system.send_message_over_socket = AsyncMock(return_value=None)
    return system

# @pytest.mark.asyncio
# async def test_publish_sends_message(actor_system):
#     # Create a mock message with a to_yaml method
#     mock_message = AbstractQuery(actor_id=1, content="Test Message")
#
#     # Call publish, which should now use the mocked send_message_over_socket method
#     await actor_system.publish(mock_message)
#
#     # Assert send_message_over_socket was called with the expected arguments
#     actor_system.send_message_over_socket.assert_awaited_once_with(
#         "localhost", 8000, "mock_yaml_message"
#     )