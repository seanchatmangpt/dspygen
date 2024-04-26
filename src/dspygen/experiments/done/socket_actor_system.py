import asyncio

from dspygen.rdddy.base_actor import BaseActor
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.actor_system import ActorSystem


class PrintActor(BaseActor):

    async def process_message(self, message:BaseCommand):
        print(f"{self.actor_id} received message: {message.content}")


class SimpleMessage(BaseCommand):
    pass


async def main():
    system1 = ActorSystem()
    system2 = ActorSystem()

    # Start each system's server on a different port
    await system1.start_server(host='localhost', port=8000)
    await system2.start_server(host='localhost', port=8001)

    # Add a print actor to each system
    actor1 = PrintActor(name="Actor1")
    actor2 = PrintActor(name="Actor2")

    # Assuming the process_message method in ActorSystem can route messages to the correct actor
    system1.actors[1] = actor1
    system2.actors[2] = actor2

    # Publish a message from each system to the other
    # For simplicity, we directly call send_message, assuming it handles message serialization
    message_to_system2 = SimpleMessage("Hello from System1 to System2").to_yaml()
    message_to_system1 = SimpleMessage("Hello from System2 to System1").to_yaml()

    await system1.send_message(message_to_system2, target_host='localhost', target_port=8001)
    await system2.send_message(message_to_system1, target_host='localhost', target_port=8000)

    # Give some time for messages to be processed
    await asyncio.sleep(1)

    # Clean up
    await system1.stop()
    await system2.stop()

if __name__ == "__main__":
    asyncio.run(main())
