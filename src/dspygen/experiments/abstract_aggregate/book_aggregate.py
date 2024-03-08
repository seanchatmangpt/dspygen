from dspygen.experiments.abstract_command.place_order import PlaceOrder
from dspygen.rdddy.abstract_aggregate import AbstractAggregate
from dspygen.rdddy.actor_system import ActorSystem


class BookAggregate(AbstractAggregate):
    """Generated class for BookAggregate, inheriting from AbstractAggregate."""

    async def handle_place_order(self, command: PlaceOrder):
        print(f"BookAggregate handle order: {command.content}")
        print(f"Check inventory")


async def main():
    asys = ActorSystem()
    await asys.actor_of(BookAggregate)
    await asys.publish(PlaceOrder(content="Hello World Book"))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())