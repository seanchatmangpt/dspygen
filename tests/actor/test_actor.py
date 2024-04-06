import asyncio

import pytest

from dspygen.rdddy.abstract_actor import AbstractActor
from dspygen.rdddy.abstract_query import AbstractQuery
from dspygen.rdddy.actor_system import ActorSystem


@pytest.fixture()
def actor_system(event_loop):
    # Provide the event loop to the actor system
    return ActorSystem(event_loop)


@pytest.mark.asyncio()
async def test_handler(actor_system):
    class DummyActor(AbstractActor):
        def __init__(self, actor_system, actor_id=None):
            super().__init__(actor_system, actor_id)
            self.processed_query = None

        async def handle_query(self, query: AbstractQuery):
            self.processed_query = query

    actor = await actor_system.actor_of(DummyActor)

    query = AbstractQuery(actor_id=actor.actor_id, content="Query1")

    await asyncio.sleep(0)

    await actor_system.publish(query)

    await asyncio.sleep(0)

    # assert actor.processed_query.actor_id == actor.actor_id
