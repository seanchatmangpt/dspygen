import asyncio

from dspygen.rdddy.base_inhabitant import BaseInhabitant
from dspygen.rdddy.service_colony import ServiceColony
from dspygen.rdddy.base_message import ExceptionMessage, TerminationMessage


class WorkerInhabitant(BaseInhabitant):
    async def start_working(self):
        try:
            # Simulate some work
            await asyncio.sleep(1)
            # Simulate an error
            raise RuntimeError("Worker encountered an error.")
        except Exception as e:
            await self.publish(ExceptionMessage(content=str(e)))
            await self.publish(
                TerminationMessage(content=str(e), inhabitant_id=self.inhabitant_id)
            )


class SupervisorInhabitant(BaseInhabitant):
    def __init__(self, service_colony, inhabitant_id=None):
        super().__init__(service_colony, inhabitant_id)
        self.worker_inhabitant= None
        self.restart_count = 0

    async def handle_exception(self, message: ExceptionMessage):
        # If an error message is received, restart the worker
        if "error" in message.content:
            self.restart_count += 1
            self.worker_inhabitant= await self.service_colony.inhabitant_of(WorkerInhabitant)

    async def start_worker(self):
        self.worker_inhabitant= await self.service_colony.inhabitant_of(WorkerInhabitant)
        await self.worker_inhabitant.start_working()


class RootSupervisorInhabitant(BaseInhabitant):
    def __init__(self, service_colony, inhabitant_id=None):
        super().__init__(service_colony, inhabitant_id)
        self.supervisor_inhabitant= None
        self.restart_count = 0

    async def handle_exception(self, message: ExceptionMessage):
        if "error" in message.content:
            self.restart_count += 1

    async def handle_termination(self, message: TerminationMessage):
        # Handle termination logic
        await self.service_colony.remove_inhabitant(message.inhabitant_id)

    async def start_supervisor(self):
        self.supervisor_inhabitant= await self.service_colony.inhabitant_of(SupervisorInhabitant)
        await self.supervisor_inhabitant.start_worker()


import pytest

from dspygen.rdddy.service_colony import ServiceColony


@pytest.fixture()
def service_colony(event_loop):
    return ServiceColony(event_loop)


@pytest.mark.skip
@pytest.mark.asyncio()
async def test_worker_restart(service_colony):
    root_supervisor = await service_colony.inhabitant_of(RootSupervisorInhabitant)
    await root_supervisor.start_supervisor()

    await asyncio.sleep(0)  # Give enough time for the hierarchy to react

    # Check if the supervisor has restarted the worker
    assert root_supervisor.restart_count > 0

    await asyncio.sleep(.1)

    await asyncio.sleep(0)
    # Check if the root supervisor has restarted the supervisor
