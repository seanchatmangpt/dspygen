from unittest.mock import AsyncMock

from dspygen.rdddy.base_query import BaseQuery
from dspygen.rdddy.service_colony import ServiceColony
import pytest


@pytest.fixture()
def service_colony(event_loop):
    # Provide the event loop to the inhabitant system
    system = ServiceColony(event_loop)
    # Mock the send_message_over_socket method
    system.send_message_over_socket = AsyncMock(return_value=None)
    return system

# @pytest.mark.asyncio
# async def test_publish_sends_message(service_colony):
#     # Create a mock message with a to_yaml method
#     mock_message = AbstractQuery(inhabitant_id=1, content="Test Message")
#
#     # Call publish, which should now use the mocked send_message_over_socket method
#     await service_colony.publish(mock_message)
#
#     # Assert send_message_over_socket was called with the expected arguments
#     service_colony.send_message_over_socket.assert_awaited_once_with(
#         "localhost", 8000, "mock_yaml_message"
#     )