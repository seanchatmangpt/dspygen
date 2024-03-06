import asyncio

import pytest
from loguru import logger

from dspygen.rdddy.abstract_actor import AbstractActor
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.rdddy.abstract_message import AbstractEvent, AbstractMessage


class LogSink:
    def __init__(self):
        self.messages = []

    def write(self, message):
        self.messages.append(message)

    def __str__(self):
        return "".join(self.messages)


@pytest.fixture()
def log_sink():
    sink = LogSink()
    logger.add(sink, format="{message}")
    yield sink
    logger.remove()


@pytest.fixture()
def actor_system(event_loop):
    """Fixture to create an instance of the AbstractActorSystem class for testing purposes."""
    return ActorSystem(loop=event_loop)


@pytest.mark.asyncio()
async def test_actor_creation(actor_system):
    """Test case to verify actor creation within the AbstractActorSystem.

    Preconditions:
        - An instance of the AbstractActorSystem class must be available.

    Actions:
        - Creates an actor within the actor system.

    Postconditions:
        - Verifies that the created actor is accessible within the actor system.
    """
    actor = await actor_system.actor_of(AbstractActor)
    assert actor is actor_system[actor.actor_id]


@pytest.mark.asyncio()
async def test_publishing(actor_system):
    """Test case to verify message publishing within the AbstractActorSystem.

    Preconditions:
        - An instance of the AbstractActorSystem class must be available.

    Actions:
        - Creates two test actors within the actor system.
        - Publishes an event message.
        - Allows time for message processing.

    Postconditions:
        - Verifies that each actor has received the published message.
    """

    class TestAbstractActor(AbstractActor):
        def __init__(self, actor_system: "ActorSystem", actor_id=None):
            super().__init__(actor_system, actor_id)
            self.received_message = None

        async def handle_event(self, event: AbstractEvent):
            self.received_message = event.content

    actor1 = await actor_system.actor_of(TestAbstractActor)
    actor2 = await actor_system.actor_of(TestAbstractActor)

    await actor_system.publish(AbstractEvent(content="Content"))

    await asyncio.sleep(0)  # Allow time for message processing

    assert actor1.received_message == "Content"
    assert actor2.received_message == "Content"


@pytest.mark.asyncio()
async def test_wait_for_event_sequentially(actor_system):
    """Tests the AbstractActorSystem's ability to wait for a specific event type and receive it once published.

    This test ensures that the AbstractActorSystem can correctly wait for an event of a specified type and then receive that event
    after it has been published. It utilizes asyncio.gather to concurrently start the event waiting process and publish the event,
    with a slight delay before publishing to ensure the system is indeed waiting for the event. This test helps verify that the
    AbstractActorSystem's event waiting mechanism is functioning as expected, particularly in scenarios where the order of operations is
    critical to the system's behavior.

    Args:
        actor_system (AbstractActorSystem): The AbstractActorSystem instance being tested.

    Steps:
        1. Define a test event of the expected type (`Event`) with a specific content.
        2. Implement an asynchronous function `publish_event` that introduces a short delay before publishing
           the test event to the AbstractActorSystem. This delay ensures that the system starts waiting for the event
           before it is actually published.
        3. Implement an asynchronous function `wait_for_event` that awaits the arrival of a message of the specified
           type (`Event`) within the AbstractActorSystem.
        4. Use `asyncio.gather` to run both `wait_for_event` and `publish_event` concurrently. The ordering within
           `asyncio.gather` and the delay in `publish_event` ensure that the system begins waiting for the event
           before it is published.
        5. Assert that the event received by the waiting function matches the content of the test event that was published.
           This confirms that the AbstractActorSystem's waiting and event handling mechanisms are operating correctly.

    Preconditions:
        - The `AbstractActorSystem` instance must be initialized and capable of publishing events and waiting for specific event types.

    Postconditions:
        - The system successfully waits for and receives the specified event after it has been published, indicating
          that event waiting and receiving are functioning as intended within the AbstractActorSystem.

    """
    test_event = AbstractEvent(content="Test event for waiting")

    async def publish_event():
        # A short delay ensures that the system is indeed waiting for the event before it's published.
        await asyncio.sleep(0.1)
        await actor_system.publish(test_event)

    async def wait_for_event():
        # This will start waiting before the event is published due to the sleep in publish_event.
        return await actor_system.wait_for_message(AbstractEvent)

    # Use asyncio.gather to run both the publishing and waiting concurrently,
    # but sequence the publish to happen after the wait has started.
    received_event, _ = await asyncio.gather(wait_for_event(), publish_event())

    assert received_event.content == test_event.content


@pytest.mark.asyncio()
async def test_actor_removal(actor_system, log_sink):
    removable_actor = await actor_system.actor_of(AbstractActor)

    # Initially, ensure the actor is in the system
    assert removable_actor.actor_id in actor_system.actors

    # Remove the actor from the system
    await actor_system.remove_actor(removable_actor.actor_id)

    # Verify the actor has been removed
    assert removable_actor.actor_id not in actor_system.actors

    # Attempt to send a message to the removed actor
    test_message = AbstractEvent(content="Message to removed actor.")
    await actor_system.send(removable_actor.actor_id, test_message)

    assert f"Actor {removable_actor.actor_id} not found." in str(log_sink)


@pytest.mark.asyncio()
async def test_error_when_base_message_used(actor_system):
    """Verifies that using the base Message class directly raises a ValueError.

    Preconditions:
        - An instance of the AbstractActorSystem class must be available.

    Actions:
        - Attempts to publish a message using the base Message class.

    Postconditions:
        - A ValueError is raised, indicating the base Message class should not be used directly.
    """
    base_message_instance = (
        AbstractMessage()
    )  # Create an instance of the base Message class

    with pytest.raises(ValueError) as exc_info:
        await actor_system.publish(
            base_message_instance
        )  # Attempt to publish the base message instance

    # Check if the error message matches the expected output
    assert "The base Message class should not be used directly" in str(exc_info.value)
