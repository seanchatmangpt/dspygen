# import asyncio
# import pytest
# from unittest.mock import Mock, patch
# from dspygen.rdddy.service_colony import ServiceColony
# from dspygen.rdddy.base_message import BaseMessage
# from dspygen.rdddy.base_inhabitant import BaseInhabitant
#
#
# class TestMessage(BaseMessage):
#     content: str
#
#
# class TestInhabitant(BaseInhabitant):
#     def __init__(self, system, inhabitant_id=None):
#         super().__init__(system, inhabitant_id)
#         self.received_messages = []
#
#     async def handle_message(self, message):
#         self.received_messages.append(message)
#
#
# @pytest.fixture
# async def service_colony():
#     system = ServiceColony()
#     yield system
#     await system.shutdown()
#
#
# @pytest.mark.asyncio
# async def test_inhabitant_creation(service_colony):
#     inhabitant = await service_colony.inhabitant_of(TestInhabitant)
#     assert inhabitant.inhabitant_id in service_colony.inhabitants
#     assert isinstance(service_colony.inhabitants[inhabitant.inhabitant_id], TestInhabitant)
#
#
# @pytest.mark.asyncio
# async def test_multiple_inhabitant_creation(service_colony):
#     inhabitants = await service_colony.inhabitants_of([TestInhabitant, TestInhabitant])
#     assert len(inhabitants) == 2
#     assert all(isinstance(inhabitant, TestInhabitant) for inhabitant in inhabitants)
#     assert all(inhabitant.inhabitant_id in service_colony.inhabitants for inhabitant in inhabitants)
#
#
# @pytest.mark.asyncio
# async def test_publish_message(service_colony):
#     inhabitant1 = await service_colony.inhabitant_of(TestInhabitant)
#     inhabitant2 = await service_colony.inhabitant_of(TestInhabitant)
#     message = TestMessage(content="Test message")
#
#     await service_colony.publish(message)
#     await asyncio.sleep(0.1)  # Allow time for message processing
#
#     assert message in inhabitant1.received_messages
#     assert message in inhabitant2.received_messages
#
#
# @pytest.mark.asyncio
# async def test_send_message_to_specific_inhabitant(service_colony):
#     inhabitant1 = await service_colony.inhabitant_of(TestInhabitant)
#     inhabitant2 = await service_colony.inhabitant_of(TestInhabitant)
#     message = TestMessage(content="Test message")
#
#     await service_colony.send(inhabitant1.inhabitant_id, message)
#     await asyncio.sleep(0.1)  # Allow time for message processing
#
#     assert message in inhabitant1.received_messages
#     assert message not in inhabitant2.received_messages
#
#
# @pytest.mark.asyncio
# async def test_remove_inhabitant(service_colony):
#     inhabitant = await service_colony.inhabitant_of(TestInhabitant)
#     assert inhabitant.inhabitant_id in service_colony.inhabitants
#
#     await service_colony.remove_inhabitant(inhabitant.inhabitant_id)
#     assert inhabitant.inhabitant_id not in service_colony.inhabitants
#
#
# @pytest.mark.asyncio
# async def test_wait_for_message(service_colony):
#     async def publish_after_delay():
#         await asyncio.sleep(0.1)
#         await service_colony.publish(TestMessage(content="Delayed message"))
#
#     asyncio.create_task(publish_after_delay())
#     received_message = await service_colony.wait_for_message(TestMessage)
#
#     assert isinstance(received_message, TestMessage)
#     assert received_message.content == "Delayed message"
#
#
# @pytest.mark.asyncio
# async def test_service_colony_shutdown(service_colony):
#     inhabitant1 = await service_colony.inhabitant_of(TestInhabitant)
#     inhabitant2 = await service_colony.inhabitant_of(TestInhabitant)
#
#     await service_colony.shutdown()
#
#     assert len(service_colony.inhabitants) == 0
#
#
# @pytest.mark.asyncio
# async def test_publish_invalid_message(service_colony):
#     with pytest.raises(ValueError):
#         await service_colony.publish(BaseMessage())
#
#
# @pytest.mark.asyncio
# async def test_getitem_access(service_colony):
#     inhabitant = await service_colony.inhabitant_of(TestInhabitant)
#     retrieved_inhabitant = service_colony[inhabitant.inhabitant_id]
#     assert retrieved_inhabitant is inhabitant
#
#
# @pytest.mark.asyncio
# async def test_send_to_nonexistent_inhabitant(service_colony):
#     message = TestMessage(content="Test message")
#     await service_colony.send(999, message)  # 999 is a non-existent inhabitant ID
#     # This should not raise an exception, but log a debug message
#
#
# @pytest.mark.asyncio
# async def test_remove_nonexistent_inhabitant(service_colony):
#     await service_colony.remove_inhabitant(999)  # 999 is a non-existent inhabitant ID
#     # This should not raise an exception, but log a debug message
#
#
# @pytest.mark.asyncio
# async def test_websocket_integration(service_colony):
#     with patch('websockets.connect') as mock_connect:
#         mock_websocket = Mock()
#         mock_connect.return_value.__aenter__.return_value = mock_websocket
#
#         service_colony.websocket_uri = "ws://test.com"
#         await service_colony.publish(TestMessage(content="WebSocket test"))
#
#         mock_websocket.send.assert_called_once()
#
#
# if __name__ == "__main__":
#     pytest.main([__file__])