import asyncio
import logging
from typing import Dict, Any, Optional, Callable
from realtime import RealtimeSubscribeStates

from dspygen.rdddy.async_realtime_client import AsyncRealtimeClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PhoenixClient:
    def __init__(self, url: str, api_key: Optional[str] = None):
        self.url = url
        self.api_key = api_key
        self.client = AsyncRealtimeClient(url, api_key)
        self.channel = None

    async def connect(self):
        """Establish the WebSocket connection with retry logic."""
        retries = 3
        for attempt in range(1, retries + 1):
            try:
                await self.client.connect()
                logger.info(f"Connected to WebSocket at {self.url}")
                return
            except Exception as e:
                logger.error(f"Failed to connect to WebSocket (Attempt {attempt}/{retries}): {e}")
                if attempt == retries:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def create_channel(self, channel_name: str, config: Optional[Dict] = None):
        """Create or reuse a channel, ensuring only one channel per client."""
        if not self.client.is_connected:
            raise RuntimeError("Client is not connected. Call connect() first.")

        if self.channel and self.channel.topic == channel_name:
            logger.info(f"Reusing existing channel '{channel_name}'.")
        else:
            self.channel = self.client.channel(channel_name, config or {})
            logger.info(f"Channel '{channel_name}' created.")

    async def subscribe(self, on_subscribe: Optional[Callable] = None):
        """Subscribe to the channel with error handling."""
        if not on_subscribe:
            on_subscribe = self._default_on_subscribe

        if not self.channel:
            raise RuntimeError("No channel exists. Call create_channel() first.")

        await self.channel.subscribe(on_subscribe)

    async def send_broadcast(self, event: str, message: Dict[str, Any], ack: bool = False, self_broadcast: bool = False):
        """Send a broadcast message on the channel."""
        if not self.channel:
            raise RuntimeError("No channel exists. Call create_channel() first.")

        config = {
            "broadcast": {
                "ack": ack,
                "self": self_broadcast
            }
        }
        await self.create_channel(self.channel.topic, config)
        await self.channel.send_broadcast(event, message)
        logger.info(f"Sent broadcast on event '{event}' with message: {message}")

    def on_broadcast(self, event: str, callback: Callable):
        """Register a callback for broadcast events."""
        if not self.channel:
            raise RuntimeError("No channel exists. Call create_channel() first.")

        self.channel.on_broadcast(event, callback)

    async def listen(self):
        """Start listening to the WebSocket."""
        await self.client.listen()

    def _default_on_subscribe(self, status: RealtimeSubscribeStates, err: Optional[Exception] = None):
        """Default subscription status handler."""
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            logger.info('Successfully subscribed to the channel.')
        elif status == RealtimeSubscribeStates.CHANNEL_ERROR:
            logger.error(f'Error subscribing to the channel: {err}')
        elif status == RealtimeSubscribeStates.TIMED_OUT:
            logger.warning('Subscription attempt timed out.')
        elif status == RealtimeSubscribeStates.CLOSED:
            logger.warning('Channel was unexpectedly closed.')


class InhabitantChannelClient(PhoenixClient):
    """Specialized client for handling inhabitant lobby interactions."""

    async def connect_to_inhabitant_lobby(self):
        """Connect and subscribe to the inhabitant lobby channel."""
        await self.connect()  # Establish the WebSocket connection
        await self.create_channel("actor:lobby")  # Create or reuse the channel
        await self.subscribe(self._on_inhabitant_lobby_subscribe)  # Subscribe to the channel

        # Register event handlers
        self.on_broadcast("ping", self.handle_ping)
        self.on_broadcast("shout", self.handle_shout)
        self.on_broadcast("inhabitant_msg", self.handle_inhabitant_msg)

    async def handle_ping(self, payload: Dict):
        """Handle incoming ping events."""
        logger.info(f"Received ping with payload: {payload}")
        # Implement ping response logic if needed

    async def handle_shout(self, payload: Dict):
        """Handle incoming shout events."""
        logger.info(f"Received shout with payload: {payload}")

    async def handle_inhabitant_msg(self, payload: Dict):
        """Handle incoming inhabitant messages."""
        logger.info(f"Received inhabitant_msg with body: {payload.get('body')}")

    async def send_ping(self, message: Dict[str, Any]):
        """Send a ping message to the inhabitant lobby."""
        await self.send_broadcast("ping", message)

    async def send_shout(self, message: Dict[str, Any]):
        """Send a shout message to the inhabitant lobby."""
        await self.send_broadcast("shout", message)

    async def send_inhabitant_msg(self, message: Dict[str, Any]):
        """Send an inhabitant message to the inhabitant lobby."""
        await self.send_broadcast("inhabitant_msg", message)

    def _on_inhabitant_lobby_subscribe(self, status: RealtimeSubscribeStates, err: Optional[Exception]):
        """Handle subscription status specifically for the inhabitant lobby."""
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            logger.info('Connected to inhabitant:lobby!')
        else:
            super()._default_on_subscribe(status, err)


# Example usage
async def main():
    """Main function to run the inhabitant channel client."""
    inhabitant_client = InhabitantChannelClient("ws://localhost:4000/socket/websocket")

    # Connect to the inhabitant:lobby channel
    await inhabitant_client.connect_to_inhabitant_lobby()

    # Send some messages
    await inhabitant_client.send_ping({"hello": "Ping from client!"})
    await inhabitant_client.send_shout({"hello": "This is a shout message!"})
    await inhabitant_client.send_inhabitant_msg({"body": "This is an inhabitant message."})

    # Start listening for events
    await inhabitant_client.listen()


if __name__ == "__main__":
    asyncio.run(main())
