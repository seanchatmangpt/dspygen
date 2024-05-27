import asyncio
import pytest
import pytest_asyncio
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.rdddy.base_message import BaseMessage

class BaseEvent(BaseMessage):
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f"BaseEvent(content={self.content})"


class TestBaseActor:
    def __init__(self, system, actor_id=None):
        self.system = system
        self.actor_id = actor_id or id(self)
        self.mailbox = asyncio.Queue()
        self.received_message = None

    async def start(self, scheduler):
        asyncio.create_task(self._process_messages())

    async def _process_messages(self):
        while True:
            message = await self.mailbox.get()
            await self.handle_event(message)

    async def handle_event(self, message):
        self.received_message = message.content


@pytest_asyncio.fixture
async def actor_system():
    system = ActorSystem()
    yield system
    await system.shutdown()


@pytest.fixture
def log_sink():
    class LogSink:
        def __init__(self):
            self.messages = []

        def write(self, message):
            self.messages.append(message)

    return LogSink()


@pytest.mark.asyncio
async def test_publishing(actor_system, log_sink):
    actor1 = await actor_system.actor_of(TestBaseActor)
    actor2 = await actor_system.actor_of(TestBaseActor)

    logger.info(f"Publishing event to actors: {actor1.actor_id}, {actor2.actor_id}")
    await actor_system.publish(BaseEvent(content="Content"))

    await asyncio.sleep(0.1)  # Allow time for message processing

    logger.info(f"Actor 1 received message: {actor1.received_message}")
    logger.info(f"Actor 2 received message: {actor2.received_message}")

    assert actor1.received_message == "Content", f"Actor {actor1.actor_id} did not receive the message"
    assert actor2.received_message == "Content", f"Actor {actor2.actor_id} did not receive the message"


def main():
    import sys
    import pytest
    sys.exit(pytest.main([__file__]))

if __name__ == "__main__":
    main()