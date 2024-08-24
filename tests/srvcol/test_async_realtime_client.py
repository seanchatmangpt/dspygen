import asyncio

import inject
import pytest
from unittest.mock import Mock, call


class MockChannel:
    def __init__(self, name):
        self.name = name
        self.subscribed = False
        self.broadcasts = []
        self.callbacks = {}

    async def subscribe(self, callback):
        self.subscribed = True
        if callback:
            callback('subscribed', None)

    async def send_broadcast(self, event, message):
        self.broadcasts.append((event, message))
        if event in self.callbacks:
            for cb in self.callbacks[event]:
                cb(message)

    def on_broadcast(self, event, callback):
        if event not in self.callbacks:
            self.callbacks[event] = []
        self.callbacks[event].append(callback)


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
            self.channels[name] = MockChannel(name)
        return self.channels[name]


# Let's assume `AsyncRealtimeClient` and `Channel` are part of the system we want to mock.

class TestAsyncRealtimeClientMock:

    @pytest.fixture
    def client_mock(self):
        # This would be our mock implementation of AsyncRealtimeClient
        class MockChannel:
            def __init__(self, name):
                self.name = name
                self.subscribed = False
                self.broadcasts = []
                self.callbacks = {}

            async def subscribe(self, callback):
                self.subscribed = True
                if callback:
                    callback('subscribed', None)

            async def send_broadcast(self, event, message):
                self.broadcasts.append((event, message))
                if event in self.callbacks:
                    for cb in self.callbacks[event]:
                        cb(message)

            def on_broadcast(self, event, callback):
                if event not in self.callbacks:
                    self.callbacks[event] = []
                self.callbacks[event].append(callback)

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
                    self.channels[name] = MockChannel(name)
                return self.channels[name]

        return MockAsyncRealtimeClient

    def test_connect(self, client_mock):
        client = client_mock("ws://localhost:4000/socket/")
        assert not client.connected
        asyncio.run(client.connect())
        assert client.connected

    def test_channel_subscription(self, client_mock):
        client = client_mock("ws://localhost:4000/socket/")
        asyncio.run(client.connect())
        channel = client.channel("test:lobby")
        assert not channel.subscribed
        asyncio.run(channel.subscribe(None))
        assert channel.subscribed

    def test_send_broadcast(self, client_mock):
        client = client_mock("ws://localhost:4000/socket/")
        asyncio.run(client.connect())
        channel = client.channel("test:lobby")
        asyncio.run(channel.subscribe(None))

        # Send a broadcast message
        asyncio.run(channel.send_broadcast("test_event", {"data": "test"}))
        assert len(channel.broadcasts) == 1
        assert channel.broadcasts[0] == ("test_event", {"data": "test"})

    def test_on_broadcast_callback(self, client_mock):
        client = client_mock("ws://localhost:4000/socket/")
        asyncio.run(client.connect())
        channel = client.channel("test:lobby")
        asyncio.run(channel.subscribe(None))

        # Prepare callback
        mock_callback = Mock()
        channel.on_broadcast("test_event", mock_callback)

        # Send a broadcast message
        asyncio.run(channel.send_broadcast("test_event", {"data": "test"}))

        # Check if the callback was triggered
        mock_callback.assert_called_once_with({"data": "test"})
