import asyncio

import pytest

from dspygen.rdddy.base_actor import BaseActor
from dspygen.rdddy.base_query import BaseQuery
from dspygen.rdddy.actor_system import ActorSystem


@pytest.fixture()
def actor_system(event_loop):
    # Provide the event loop to the actor system
    return ActorSystem(event_loop)


class DummyActor(BaseActor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        self.processed_query = None

    async def handle_query(self, query: BaseQuery):
        self.processed_query = query


@pytest.mark.asyncio()
async def test_handler(actor_system):
    actor = await actor_system.actor_of(DummyActor)

    query = BaseQuery(content="Query1")

    await asyncio.sleep(0)

    await actor_system.publish(query)
