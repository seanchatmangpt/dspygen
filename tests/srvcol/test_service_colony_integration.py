# import asyncio
# from dspygen.rdddy.base_message import BaseMessage, ExceptionMessage
#
# import pytest
# from dspygen.rdddy.async_realtime_client import AsyncRealtimeClient
# from dspygen.rdddy.service_colony import ServiceColony
#
#
# # Fixture for ServiceColony
# @pytest.fixture
# def service_colony():
#     # Instantiate the ServiceColony with injected dependencies
#     colony = ServiceColony(realtime_client=AsyncRealtimeClient("ws://localhost:4000/socket/websocket", ""))
#
#     yield colony
#
#     # Ensure cleanup after tests
#     asyncio.run(colony.shutdown())
#
#
# @pytest.mark.asyncio
# async def test_join_channel(service_colony):
#     await service_colony.connect()
#     assert service_colony.realtime_client.is_connected
#     assert service_colony.channel.topic == 'service_colony:lobby'
#
#
#
#
#
#
# @pytest.mark.asyncio
# async def test_send_and_receive_ping(service_colony):
#     await service_colony.connect()
#
#     # Listen for the "ping_response" from the server
#     future = asyncio.ensure_future(service_colony.wait_for_message(ExceptionMessage))
#
#     await asyncio.sleep(0)
#
#     # Send the ping message
#     await service_colony.publish(ExceptionMessage())
#
#     await asyncio.sleep(0)
#
#     # Wait for the response
#     response = await future
#     assert response is not None
#     assert response.model_dump_json() == '{"response": "Pong!"}'
#
#
# @pytest.mark.asyncio
# async def test_send_and_receive_shout(service_colony):
#     await service_colony.connect()
#
#     # Listen for the "shout_response" from the server
#     future = asyncio.ensure_future(service_colony.wait_for_message(BaseMessage))
#
#     # Send the shout message
#     await service_colony.channel.push("shout", {"message": "test_shout"})
#
#     # Wait for the response
#     response = await future
#     assert response is not None
#     assert response.model_dump_json() == '{"message": "Shouted back!"}'
#
#
# @pytest.mark.asyncio
# async def test_send_and_receive_actor_msg(service_colony):
#     await service_colony.connect()
#
#     # Listen for the "actor_msg" from the server
#     future = asyncio.ensure_future(service_colony.wait_for_message(BaseMessage))
#
#     # Send the actor_msg message
#     await service_colony.channel.push("actor_msg", {"body": "test_actor_msg"})
#
#     # Wait for the response
#     response = await future
#     assert response is not None
#     assert response.model_dump_json() == '{"body": "test_actor_msg"}'
