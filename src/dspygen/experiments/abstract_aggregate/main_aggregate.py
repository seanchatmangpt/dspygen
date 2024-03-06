from dspygen.experiments.abstract_aggregate.book_aggregate import BookAggregate
from dspygen.experiments.abstract_aggregate.customer_aggregate import CustomerAggregate
from dspygen.experiments.abstract_aggregate.order_aggregate import OrderAggregate
from dspygen.experiments.abstract_command.place_order import PlaceOrder
from dspygen.rdddy.actor_system import ActorSystem


async def main():
    asys = ActorSystem()
    await asys.actors_of([BookAggregate, CustomerAggregate, OrderAggregate])

    while True:
        await asys.publish(PlaceOrder(content="Hello World Book"))
        await asyncio.sleep(1)

if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
