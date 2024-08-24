import asyncio

import inject
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from dspygen.rdddy.async_realtime_client import AsyncRealtimeClient
from dspygen.rdddy.base_message import BaseMessage
from dspygen.rdddy.service_colony import ServiceColony


class MockAsyncRealtimeClient:
    def __init__(self, url):
        self.url = url
        self.connected = False
        self.channels = {}

    async def connect(self):
        self.connected = True

    async def disconnect(self):
        self.connected = False

    def channel(self, name):
        if name not in self.channels:
            self.channels[name] = AsyncMock()
        return self.channels[name]


@pytest.fixture
def configure_injections_for_tests():
    def config(binder):
        mock_realtime_client = MockAsyncRealtimeClient("ws://mocked_url")
        binder.bind(AsyncRealtimeClient, mock_realtime_client)

    inject.configure(config)


@pytest.fixture
def service_colony(configure_injections_for_tests):
    return ServiceColony()


@pytest.mark.asyncio
async def test_service_colony_integration(configure_injections_for_tests):
    service_colony = ServiceColony()
    await service_colony.connect()
    assert service_colony.realtime_client.connected


@pytest.mark.asyncio
async def test_connect(service_colony):
    await service_colony.connect()

    # Ensure the client connected and subscribed to the channel
    assert service_colony.realtime_client.connected
    service_colony.channel.subscribe.assert_called_once()
    service_colony.channel.on_broadcast.assert_called_once_with("message", service_colony._on_message_received)


@pytest.mark.asyncio
@patch('reactivex.subject.Subject.on_next')
async def test_publish(mock_on_next, service_colony):
    await service_colony.connect()

    message = MagicMock(spec=BaseMessage)
    message.model_dump_json.return_value = '{"type": "test_message"}'

    await service_colony.publish(message)

    # Assert that the broadcast was sent
    service_colony.channel.send_broadcast.assert_called_once_with("message", '{"type": "test_message"}')

    # Assert that the event was published to the event stream
    mock_on_next.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_send(service_colony):
    # Setup a mock inhabitant
    mock_inhabitant = MagicMock()
    mock_inhabitant.inhabitant_id = 1
    mock_inhabitant.mailbox = MagicMock()
    service_colony.inhabitants[1] = mock_inhabitant

    message = MagicMock(spec=BaseMessage)
    await service_colony.send(1, message)

    mock_inhabitant.mailbox.on_next.assert_called_once_with(message)


from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_inhabitant_of(service_colony):
    # Use MagicMock for the class and AsyncMock for the start method
    mock_inhabitant_class = MagicMock()
    mock_inhabitant = mock_inhabitant_class.return_value
    mock_inhabitant.inhabitant_id = 1
    mock_inhabitant.start = AsyncMock()  # Make sure start is an AsyncMock since it's awaited

    inhabitant = await service_colony.inhabitant_of(mock_inhabitant_class)

    assert inhabitant == mock_inhabitant
    assert service_colony.inhabitants[1] == mock_inhabitant
    mock_inhabitant.start.assert_called_once_with(service_colony.scheduler)


@pytest.mark.asyncio
async def test_remove_inhabitant(service_colony):
    # Setup a mock inhabitant
    mock_inhabitant = MagicMock()
    mock_inhabitant.inhabitant_id = 1
    service_colony.inhabitants[1] = mock_inhabitant

    await service_colony.remove_inhabitant(1)

    assert 1 not in service_colony.inhabitants


from unittest.mock import MagicMock
from dspygen.rdddy.base_message import BaseMessage

@pytest.mark.asyncio
async def test_wait_for_message(service_colony):
    future = asyncio.ensure_future(service_colony.wait_for_message(BaseMessage))

    # Let the event loop run so the subscription can be set up
    await asyncio.sleep(0)

    service_colony.event_stream.on_next(BaseMessage(data={"hello": "Hello World"}))

    await asyncio.sleep(0)

    result = await future
    assert "Hello World" == result.data.get("hello")
