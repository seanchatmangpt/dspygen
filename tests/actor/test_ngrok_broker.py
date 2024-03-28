import asyncio

import pytest

from dspygen.rdddy.abstract_actor import AbstractActor
from dspygen.rdddy.abstract_command import AbstractCommand
from dspygen.rdddy.abstract_event import AbstractEvent
from dspygen.rdddy.actor_system import ActorSystem


class TestAbstractActor(AbstractActor):
    def __init__(self, actor_system: "ActorSystem", actor_id=None):
        super().__init__(actor_system, actor_id)
        self.received_message = None

    async def handle_event(self, event: AbstractEvent):
        self.received_message = event.content

    async def handle_event(self, command: AbstractCommand):
        self.received_message = command.content


@pytest.fixture()
def actor_system(event_loop):
    """Fixture to create an instance of the AbstractActorSystem class for testing purposes."""
    return ActorSystem(loop=event_loop, mqtt_broker="9.tcp.ngrok.io", mqtt_port=24651)


@pytest.mark.asyncio()
async def test_send_message(actor_system):
    # Check if client connected
    print(actor_system.mqtt_client)
    await asyncio.sleep(0.25)
    assert actor_system.mqtt_client.is_connected()
