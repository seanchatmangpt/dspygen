from dspygen.experiments.abstract_command.place_order import PlaceOrder
from dspygen.rdddy.abstract_aggregate import AbstractAggregate
from dspygen.rdddy.actor_system import ActorSystem


class OrderAggregate(AbstractAggregate):
    """Generated class for OrderAggregate, inheriting from AbstractAggregate."""

    async def handle_place_order(self, command: PlaceOrder):
        print(f"OrderAggregate handle order: {command.content}")
        print(f"Print shipping label")


async def main():
    asys = ActorSystem()
    await asys.actor_of(OrderAggregate)
    await asys.publish(PlaceOrder(content="Hello World Book"))


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
