Reactive Domain-Driven Design (RDDDY)
======================================

DSPyGen's ``rdddy`` package provides a lightweight Reactive Domain-Driven Design (RDDDY) framework
that combines classical DDD building blocks with reactive event-driven programming and AI-powered
decision making via DSPy.

Overview
--------

Traditional Domain-Driven Design structures complex business domains using Aggregates, Value Objects,
Domain Events, and Services. RDDDY extends this model with:

- **Reactive message passing** — components communicate via immutable events and commands rather
  than direct method calls.
- **AI-augmented policies and sagas** — DSPy language models can evaluate conditions, generate
  commands, and drive long-running workflows.
- **Async-first architecture** — all inter-component communication is asynchronous, enabling
  high-throughput event-driven systems.

Core Concepts
-------------

Aggregates
~~~~~~~~~~

An Aggregate is the central consistency boundary in DDD. In RDDDY, aggregates receive commands,
validate business rules, and emit domain events:

.. code-block:: python

    from dspygen.rdddy.base_aggregate import BaseAggregate
    from dspygen.rdddy.base_command import BaseCommand
    from dspygen.rdddy.base_event import BaseEvent

    class CreateOrderCommand(BaseCommand):
        customer_id: str
        items: list[str]

    class OrderCreatedEvent(BaseEvent):
        order_id: str
        customer_id: str
        items: list[str]

    class OrderAggregate(BaseAggregate):
        async def handle_create_order(self, cmd: CreateOrderCommand) -> OrderCreatedEvent:
            # Business logic and validation here
            return OrderCreatedEvent(
                order_id=self.id,
                customer_id=cmd.customer_id,
                items=cmd.items,
            )

Commands
~~~~~~~~

Commands express intent — they ask the system to do something. Each command is an immutable
Pydantic model:

.. code-block:: python

    from dspygen.rdddy.base_command import BaseCommand

    class ShipOrderCommand(BaseCommand):
        order_id: str
        shipping_address: str
        carrier: str = "UPS"

Events
~~~~~~

Events record facts — something that has already happened. They are the source of truth in an
event-sourced system:

.. code-block:: python

    from dspygen.rdddy.base_event import BaseEvent

    class OrderShippedEvent(BaseEvent):
        order_id: str
        tracking_number: str
        estimated_delivery: str

Sagas
~~~~~

Sagas coordinate multi-step workflows that span multiple aggregates. They react to events and
emit commands:

.. code-block:: python

    from dspygen.rdddy.base_saga import BaseSaga

    class OrderFulfillmentSaga(BaseSaga):
        async def on_order_created(self, event: OrderCreatedEvent) -> None:
            # Trigger payment processing
            await self.publish(ChargeCustomerCommand(
                customer_id=event.customer_id,
                amount=self.calculate_total(event.items),
            ))

        async def on_payment_succeeded(self, event: PaymentSucceededEvent) -> None:
            # Trigger shipping
            await self.publish(ShipOrderCommand(
                order_id=event.order_id,
                shipping_address=event.shipping_address,
            ))

Policies
~~~~~~~~

Policies are stateless reactive rules that map a single domain event to zero or more commands.
They are ideal for simple cause-and-effect business rules:

.. code-block:: python

    from dspygen.rdddy.base_policy import BasePolicy

    class LowInventoryPolicy(BasePolicy):
        async def on_inventory_depleted(self, event: InventoryDepletedEvent):
            await self.publish(ReorderStockCommand(
                product_id=event.product_id,
                quantity=100,
            ))

The Actor System
----------------

All components run inside an actor system that manages message routing and lifecycle:

.. code-block:: python

    import asyncio
    from dspygen.rdddy.actor_system import ActorSystem

    async def main():
        system = ActorSystem()

        # Spawn an aggregate
        order = await system.actor_of(OrderAggregate)

        # Send a command
        await system.publish(CreateOrderCommand(
            customer_id="cust-123",
            items=["widget", "gadget"],
        ))

        # Allow events to propagate
        await asyncio.sleep(0.1)

    asyncio.run(main())

AI-Augmented Decision Making
-----------------------------

RDDDY integrates with DSPy so that policies and sagas can delegate complex decisions to language
models:

.. code-block:: python

    import dspy
    from dspygen.rdddy.base_policy import BasePolicy
    from dspygen.utils.dspy_tools import init_dspy

    init_dspy()

    class FraudDetectionSignature(dspy.Signature):
        """Evaluate whether a transaction is fraudulent."""
        transaction_details: str = dspy.InputField()
        is_fraud: bool = dspy.OutputField()
        reason: str = dspy.OutputField()

    class FraudDetectionPolicy(BasePolicy):
        def __init__(self):
            super().__init__()
            self.classifier = dspy.Predict(FraudDetectionSignature)

        async def on_transaction_submitted(self, event: TransactionSubmittedEvent):
            result = self.classifier(transaction_details=str(event))
            if result.is_fraud:
                await self.publish(BlockTransactionCommand(
                    transaction_id=event.transaction_id,
                    reason=result.reason,
                ))

Testing RDDDY Components
-------------------------

RDDDY components are designed for testability. Use ``pytest-asyncio`` for async tests:

.. code-block:: python

    import pytest
    from dspygen.rdddy.actor_system import ActorSystem

    @pytest.mark.asyncio
    async def test_order_creation():
        system = ActorSystem()
        order = await system.actor_of(OrderAggregate)

        await system.publish(CreateOrderCommand(
            customer_id="cust-001",
            items=["item-A"],
        ))

        # Assert the aggregate's state was updated
        assert order.state.status == "created"

API Reference
-------------

See :doc:`api/rdddy` for full API documentation.
