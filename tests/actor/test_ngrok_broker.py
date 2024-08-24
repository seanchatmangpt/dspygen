import asyncio

import pytest

from dspygen.rdddy.base_inhabitant import BaseInhabitant
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.base_event import BaseEvent
from dspygen.rdddy.service_colony import ServiceColony


class TestBaseInhabitant(BaseInhabitant):
    def __init__(self, service_colony: "ServiceColony", inhabitant_id=None):
        super().__init__(service_colony, inhabitant_id)
        self.received_message = None

    async def handle_event(self, event: BaseEvent):
        self.received_message = event.content

    async def handle_event(self, command: BaseCommand):
        self.received_message = command.content


@pytest.fixture()
def service_colony(event_loop):
    """Fixture to create an instance of the AbstractServiceColony class for testing purposes."""
    return ServiceColony(loop=event_loop, mqtt_broker="9.tcp.ngrok.io", mqtt_port=24651)


# @pytest.mark.asyncio()
# async def test_send_message(service_colony):
#     # Check if client connected
#     print(service_colony.mqtt_client)
#     await asyncio.sleep(0.25)
#     assert service_colony.mqtt_client.is_connected()
