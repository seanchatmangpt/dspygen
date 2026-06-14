import asyncio
from typing import Any, Callable, Dict, Optional

from loguru import logger
from realtime import RealtimeSubscribeStates

from dspygen.rdddy.async_realtime_client import AsyncRealtimeClient


class PhoenixClient:
    """Wrapper around :class:`AsyncRealtimeClient` for Phoenix channel communication.

    Supports use as an async context manager::

        async with PhoenixClient(url) as client:
            await client.create_channel("my:channel")
            await client.subscribe()
            await client.listen()
    """

    def __init__(self, url: str, api_key: Optional[str] = None) -> None:
        self.url: str = url
        self.api_key: Optional[str] = api_key
        self.client: AsyncRealtimeClient = AsyncRealtimeClient(url, api_key)
        self.channel = None

    # ------------------------------------------------------------------
    # Async context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "PhoenixClient":
        """Connect on entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Disconnect on exit, regardless of whether an exception occurred."""
        await self.disconnect()

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    async def connect(self, retries: int = 3) -> None:
        """Establish the WebSocket connection with exponential-backoff retry logic.

        Args:
            retries: Maximum number of connection attempts before raising.
        """
        for attempt in range(1, retries + 1):
            try:
                await self.client.connect()
                logger.info(f"Connected to WebSocket at {self.url}")
                return
            except Exception as e:
                logger.error(f"Failed to connect to WebSocket (attempt {attempt}/{retries}): {e}")
                if attempt == retries:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def disconnect(self) -> None:
        """Gracefully unsubscribe from the active channel and close the WebSocket."""
        try:
            if self.channel:
                try:
                    await self.channel.unsubscribe()
                    logger.info(f"Unsubscribed from channel '{self.channel.topic}'.")
                except Exception as e:
                    logger.warning(f"Error unsubscribing from channel: {e}")
                self.channel = None

            if self.client.is_connected:
                await self.client.close()
                logger.info(f"WebSocket connection to {self.url} closed.")
        except Exception as e:
            logger.warning(f"Error during disconnect: {e}")

    async def is_healthy(self) -> bool:
        """Return ``True`` if the underlying WebSocket connection is open.

        This is a lightweight check that does not send any network traffic.
        """
        try:
            return bool(self.client.is_connected)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Channel management
    # ------------------------------------------------------------------

    async def create_channel(self, channel_name: str, config: Optional[Dict[str, Any]] = None) -> None:
        """Create or reuse a channel, ensuring only one channel per client.

        Args:
            channel_name: The Phoenix channel topic (e.g. ``"room:lobby"``).
            config: Optional channel configuration dict passed to the realtime client.
        """
        if not self.client.is_connected:
            raise RuntimeError("Client is not connected. Call connect() first.")

        if self.channel and self.channel.topic == channel_name:
            logger.info(f"Reusing existing channel '{channel_name}'.")
        else:
            self.channel = self.client.channel(channel_name, config or {})
            logger.info(f"Channel '{channel_name}' created.")

    async def subscribe(self, on_subscribe: Optional[Callable] = None) -> None:
        """Subscribe to the channel with optional status callback.

        Args:
            on_subscribe: Callback invoked with ``(status, error)`` on state
                changes.  Falls back to :meth:`_default_on_subscribe`.
        """
        if not self.channel:
            raise RuntimeError("No channel exists. Call create_channel() first.")

        await self.channel.subscribe(on_subscribe or self._default_on_subscribe)

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------

    async def send_broadcast(
        self,
        event: str,
        message: Dict[str, Any],
        ack: bool = False,
        self_broadcast: bool = False,
    ) -> None:
        """Send a broadcast message on the current channel.

        Args:
            event: The broadcast event name.
            message: Payload dict to broadcast.
            ack: Whether the server should acknowledge receipt.
            self_broadcast: Whether the sender receives its own broadcast.
        """
        if not self.channel:
            raise RuntimeError("No channel exists. Call create_channel() first.")

        config: Dict[str, Any] = {
            "broadcast": {
                "ack": ack,
                "self": self_broadcast,
            }
        }
        await self.create_channel(self.channel.topic, config)
        await self.channel.send_broadcast(event, message)
        logger.info(f"Sent broadcast on event '{event}': {message}")

    def on_broadcast(self, event: str, callback: Callable) -> None:
        """Register a callback for a specific broadcast event.

        Args:
            event: The broadcast event name to listen for.
            callback: Callable invoked with the event payload dict.
        """
        if not self.channel:
            raise RuntimeError("No channel exists. Call create_channel() first.")

        self.channel.on_broadcast(event, callback)

    async def listen(self) -> None:
        """Block and process incoming WebSocket messages until disconnected."""
        await self.client.listen()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _default_on_subscribe(
        self, status: RealtimeSubscribeStates, err: Optional[Exception] = None
    ) -> None:
        """Default subscription status handler."""
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            logger.info("Successfully subscribed to the channel.")
        elif status == RealtimeSubscribeStates.CHANNEL_ERROR:
            logger.error(f"Error subscribing to the channel: {err}")
        elif status == RealtimeSubscribeStates.TIMED_OUT:
            logger.warning("Subscription attempt timed out.")
        elif status == RealtimeSubscribeStates.CLOSED:
            logger.warning("Channel was unexpectedly closed.")

    def __repr__(self) -> str:
        connected = "connected" if self.client.is_connected else "disconnected"
        channel = self.channel.topic if self.channel else "none"
        return f"PhoenixClient(url={self.url!r}, status={connected}, channel={channel!r})"


class InhabitantChannelClient(PhoenixClient):
    """Specialized client for handling inhabitant lobby interactions."""

    async def connect_to_inhabitant_lobby(self) -> None:
        """Connect and subscribe to the inhabitant lobby channel."""
        await self.connect()
        await self.create_channel("actor:lobby")
        await self.subscribe(self._on_inhabitant_lobby_subscribe)

        # Register event handlers
        self.on_broadcast("ping", self.handle_ping)
        self.on_broadcast("shout", self.handle_shout)
        self.on_broadcast("inhabitant_msg", self.handle_inhabitant_msg)

    async def handle_ping(self, payload: Dict[str, Any]) -> None:
        """Handle incoming ping events."""
        logger.info(f"Received ping with payload: {payload}")

    async def handle_shout(self, payload: Dict[str, Any]) -> None:
        """Handle incoming shout events."""
        logger.info(f"Received shout with payload: {payload}")

    async def handle_inhabitant_msg(self, payload: Dict[str, Any]) -> None:
        """Handle incoming inhabitant messages."""
        logger.info(f"Received inhabitant_msg with body: {payload.get('body')}")

    async def send_ping(self, message: Dict[str, Any]) -> None:
        """Send a ping message to the inhabitant lobby."""
        await self.send_broadcast("ping", message)

    async def send_shout(self, message: Dict[str, Any]) -> None:
        """Send a shout message to the inhabitant lobby."""
        await self.send_broadcast("shout", message)

    async def send_inhabitant_msg(self, message: Dict[str, Any]) -> None:
        """Send an inhabitant message to the inhabitant lobby."""
        await self.send_broadcast("inhabitant_msg", message)

    def _on_inhabitant_lobby_subscribe(
        self, status: RealtimeSubscribeStates, err: Optional[Exception] = None
    ) -> None:
        """Handle subscription status specifically for the inhabitant lobby."""
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            logger.info("Connected to inhabitant:lobby!")
        else:
            self._default_on_subscribe(status, err)


# Example usage
async def main() -> None:
    """Main function to run the inhabitant channel client."""
    async with InhabitantChannelClient("ws://localhost:4000/socket/websocket") as client:
        await client.create_channel("actor:lobby")
        await client.subscribe(client._on_inhabitant_lobby_subscribe)

        client.on_broadcast("ping", client.handle_ping)
        client.on_broadcast("shout", client.handle_shout)
        client.on_broadcast("inhabitant_msg", client.handle_inhabitant_msg)

        await client.send_ping({"hello": "Ping from client!"})
        await client.send_shout({"hello": "This is a shout message!"})
        await client.send_inhabitant_msg({"body": "This is an inhabitant message."})

        await client.listen()


if __name__ == "__main__":
    asyncio.run(main())
