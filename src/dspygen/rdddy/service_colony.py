import asyncio
from typing import TYPE_CHECKING, Optional, TypeVar, cast

import inject
import reactivex as rx
from loguru import logger
from reactivex import operators as ops
from reactivex.scheduler.eventloop import AsyncIOScheduler

from realtime import RealtimeSubscribeStates

from dspygen.rdddy.async_realtime_client import AsyncRealtimeClient
from dspygen.rdddy.base_message import BaseMessage
from dspygen.rdddy.message_factory import MessageFactory

if TYPE_CHECKING:
    from dspygen.rdddy.base_inhabitant import BaseInhabitant

T = TypeVar("T", bound="BaseInhabitant")


class ServiceColony:
    """Orchestrates inhabitant lifecycle management, message passing, and system-wide coordination within
    the RDDDY framework."""
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None, realtime_client: AsyncRealtimeClient = None):
        """Initializes the ServiceColony with a real-time client connection."""
        self.realtime_client = inject.instance(AsyncRealtimeClient) if realtime_client is None else realtime_client
        self.channel = None
        self.inhabitants: dict[int, "BaseInhabitant"] = {}
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.scheduler = AsyncIOScheduler(loop=self.loop)
        self.event_stream = rx.subject.Subject()

    async def connect(self):
        """Connect to the WebSocket and join the main channel."""
        await self.realtime_client.connect()

        # Create and join the channel (e.g., "service_colony:lobby")

        await self.channel.subscribe(self._on_channel_subscribe)
        logger.info(f"Joined channel 'service_colony:lobby'")

        # Listen for incoming messages
        self.channel.on_broadcast("message", self._on_message_received)

    def _on_channel_subscribe(self, status: RealtimeSubscribeStates, err: Optional[Exception]):
        """Handle subscription status."""
        if status == RealtimeSubscribeStates.SUBSCRIBED:
            logger.info('Successfully subscribed to the channel.')
        else:
            logger.error(f'Error subscribing to channel: {err}')

    def _on_message_received(self, payload: dict):
        """Callback for handling incoming messages."""
        message = MessageFactory.create_message(payload)
        asyncio.run_coroutine_threadsafe(self.distribute_message(message), self.loop)

    async def distribute_message(self, message):
        """Distributes a message within the inhabitant system."""
        self.event_stream.on_next(message)
        for inhabitant in list(self.inhabitants.values()):
            await self.send(inhabitant.inhabitant_id, message)

    async def inhabitant_of(self, inhabitant_class, **kwargs) -> T:
        """Creates a new inhabitant instance and starts its mailbox processing loop."""
        inhabitant = inhabitant_class(self, **kwargs)
        self.inhabitants[inhabitant.inhabitant_id] = inhabitant
        await inhabitant.start(self.scheduler)
        logger.info(f"Inhabitant {inhabitant.inhabitant_id} started")
        return inhabitant

    async def inhabitants_of(self, inhabitant_classes, **kwargs) -> list[T]:
        """Creates multiple inhabitant instances of different types and starts their mailbox processing loops."""
        return [await self.inhabitant_of(cls, **kwargs) for cls in inhabitant_classes]

    async def publish(self, message: "BaseMessage"):
        """Publishes a message to the inhabitant system for distribution."""
        logger.debug(f"Publishing message: {message}")
        if type(message) is BaseMessage:
            raise ValueError("The base Message class should not be used directly. Please use a subclass of Message.")

        # Send message via the real-time channel
        await self.channel.send_broadcast("message", message.model_dump_json())
        self.event_stream.on_next(message)

        for inhabitant in list(self.inhabitants.values()):
            await self.send(inhabitant.inhabitant_id, message)

    async def remove_inhabitant(self, inhabitant_id):
        """Removes an inhabitant from the inhabitant system."""
        inhabitant = self.inhabitants.pop(inhabitant_id, None)
        if inhabitant:
            logger.debug(f"Removing inhabitant {inhabitant_id}")
        else:
            logger.debug(f"Inhabitant {inhabitant_id} not found for removal")
        logger.debug(f"Current inhabitants count: {len(self.inhabitants)}")

    async def send(self, inhabitant_id: int, message: "BaseMessage"):
        """Sends a message to a specific inhabitant within the inhabitant system."""
        inhabitant = self.inhabitants.get(inhabitant_id)
        if inhabitant:
            inhabitant.mailbox.on_next(message)
            await asyncio.sleep(0)
        else:
            logger.debug(f"Inhabitant {inhabitant_id} not found.")

    async def wait_for_message(self, message_type: type) -> "BaseMessage":
        """Waits for a message of a specific type to be published to the inhabitant system."""
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def on_next(msg):
            if isinstance(msg, message_type):
                future.set_result(msg)
                subscription.dispose()

        subscription = self.event_stream.pipe(
            ops.filter(lambda msg: isinstance(msg, message_type))
        ).subscribe(on_next)

        return await future

    def __getitem__(self, inhabitant_id) -> T:
        """Retrieves an inhabitant by its ID from the inhabitant system."""
        return cast(T, self.inhabitants.get(inhabitant_id))

    async def shutdown(self):
        """Shuts down the inhabitant system and terminates all inhabitants."""
        try:
            if self.channel:
                await self.channel.unsubscribe()
            if self.realtime_client.is_connected:
                await self.realtime_client.close()
            logger.debug("Inhabitant system shutdown complete.")
        except RuntimeError as e:
            # Event loop already closed
            pass

