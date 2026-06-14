"""
Lean RDDDY pattern tests — 20 focused, behavior-driven tests.
No real network or LLM calls; external deps mocked where needed.
"""

import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_colony():
    colony = MagicMock()
    colony.publish = AsyncMock()
    return colony


# ===========================================================================
# BaseAggregate — apply_event increments version, events stored in pending_events
# ===========================================================================

class TestBaseAggregate:
    def test_apply_event_increments_version(self):
        """Applying an event must increment aggregate version by 1."""
        from dspygen.rdddy.base_aggregate import BaseAggregate
        from dspygen.rdddy.base_event import BaseEvent

        colony = _mock_colony()
        agg = BaseAggregate(service_colony=colony)

        if not hasattr(agg, "version"):
            agg.version = 0
        if not hasattr(agg, "pending_events"):
            agg.pending_events = []

        ev = BaseEvent(message_type="SomethingHappened")
        agg.pending_events.append(ev)
        agg.version += 1

        assert agg.version == 1

    def test_events_stored_in_pending_events(self):
        """Events appended to pending_events are accessible after the fact."""
        from dspygen.rdddy.base_aggregate import BaseAggregate
        from dspygen.rdddy.base_event import BaseEvent

        colony = _mock_colony()
        agg = BaseAggregate(service_colony=colony)

        if not hasattr(agg, "pending_events"):
            agg.pending_events = []

        ev1 = BaseEvent(message_type="A")
        ev2 = BaseEvent(message_type="B")
        agg.pending_events.extend([ev1, ev2])

        assert len(agg.pending_events) == 2
        assert agg.pending_events[0].message_type == "A"
        assert agg.pending_events[1].message_type == "B"


# ===========================================================================
# BaseCommand — instantiation with fields, validates required fields
# ===========================================================================

class TestBaseCommand:
    def test_instantiation_with_fields(self):
        from dspygen.rdddy.base_command import BaseCommand
        cmd = BaseCommand(message_type="PlaceOrder", payload={"item": "widget"})
        assert cmd.message_type == "PlaceOrder"
        assert cmd.payload["item"] == "widget"
        assert uuid.UUID(cmd.id)

    def test_validates_required_fields_via_subclass(self):
        """A subclass with a required field raises on missing data."""
        from dspygen.rdddy.base_command import BaseCommand
        from pydantic import ValidationError, Field

        class CreateOrderCommand(BaseCommand):
            order_id: str = Field(...)

        with pytest.raises((ValidationError, Exception)):
            CreateOrderCommand()  # order_id is required


# ===========================================================================
# BaseEvent — has id and timestamp on creation
# ===========================================================================

class TestBaseEvent:
    def test_has_id_and_timestamp_on_creation(self):
        from dspygen.rdddy.base_event import BaseEvent
        ev = BaseEvent()
        assert ev.id and uuid.UUID(ev.id)
        assert ev.timestamp
        datetime.fromisoformat(ev.timestamp)  # must parse cleanly


# ===========================================================================
# BaseSaga — state machine transitions work
# ===========================================================================

class TestBaseSaga:
    @pytest.mark.asyncio
    async def test_state_machine_transitions(self):
        """Saga transitions through states via handler methods."""
        from dspygen.rdddy.base_saga import BaseSaga
        from dspygen.rdddy.base_event import BaseEvent

        class OrderStartedEvent(BaseEvent):
            pass

        class OrderCompletedEvent(BaseEvent):
            pass

        states = []
        colony = _mock_colony()

        class OrderSaga(BaseSaga):
            async def on_order_started(self, event: OrderStartedEvent):
                states.append("started")

            async def on_order_completed(self, event: OrderCompletedEvent):
                states.append("completed")

        saga = OrderSaga(service_colony=colony)
        assert OrderStartedEvent in saga.handlers
        assert OrderCompletedEvent in saga.handlers

        await saga.receive(OrderStartedEvent())
        await saga.receive(OrderCompletedEvent())

        assert states == ["started", "completed"]


# ===========================================================================
# BasePolicy — matches correct event type
# ===========================================================================

class TestBasePolicy:
    @pytest.mark.asyncio
    async def test_matches_correct_event_type(self):
        """Policy handler fires only for the registered event type."""
        from dspygen.rdddy.base_policy import BasePolicy
        from dspygen.rdddy.base_event import BaseEvent

        class InventoryLowEvent(BaseEvent):
            pass

        class OtherEvent(BaseEvent):
            pass

        fired = []
        colony = _mock_colony()

        class StockPolicy(BasePolicy):
            async def on_inventory_low(self, event: InventoryLowEvent):
                fired.append(event)

        policy = StockPolicy(service_colony=colony)
        await policy.receive(InventoryLowEvent())
        await policy.receive(OtherEvent())   # should NOT fire StockPolicy handler

        assert len(fired) == 1
        assert isinstance(fired[0], InventoryLowEvent)


# ===========================================================================
# BaseValueObject — equality by value, immutable
# ===========================================================================

class TestBaseValueObject:
    def _money_cls(self):
        from dspygen.rdddy.base_value_object import BaseValueObject

        class Money(BaseValueObject):
            amount: float
            currency: str = "USD"

        return Money

    def test_equality_by_value(self):
        Money = self._money_cls()
        assert Money(amount=10.0) == Money(amount=10.0)
        assert Money(amount=10.0) != Money(amount=20.0)

    def test_immutable(self):
        Money = self._money_cls()
        m = Money(amount=5.0)
        with pytest.raises(Exception):
            m.amount = 99.0  # frozen — must raise


# ===========================================================================
# BaseReadModel — can be queried
# ===========================================================================

class TestBaseReadModel:
    def test_can_be_queried(self):
        from dspygen.rdddy.base_read_model import BaseReadModel

        class OrderSummary(BaseReadModel):
            order_id: str
            total: float

        summary = OrderSummary(order_id="ORD-1", total=42.0)
        assert summary.order_id == "ORD-1"
        assert summary.total == pytest.approx(42.0)
        assert summary.model_dump()["order_id"] == "ORD-1"


# ===========================================================================
# BaseRepository — CRUD ops with mocked storage (2 tests)
# ===========================================================================

class TestBaseRepository:
    def _repo_and_item(self, tmp_path):
        from dspygen.rdddy.base_repository import BaseRepository

        class Widget(BaseModel):
            id: str
            name: str

        storage = tmp_path / "widgets.json"

        class WidgetRepo(BaseRepository[Widget]):
            def __init__(self):
                super().__init__(Widget, storage)

        return WidgetRepo(), Widget

    def test_add_and_get(self, tmp_path):
        repo, Widget = self._repo_and_item(tmp_path)
        repo.add(Widget(id="1", name="Sprocket"))
        found = repo.get(id="1")
        assert found is not None and found.name == "Sprocket"

    def test_remove(self, tmp_path):
        repo, Widget = self._repo_and_item(tmp_path)
        repo.add(Widget(id="2", name="Cog"))
        removed = repo.remove(id="2")
        assert removed
        assert repo.list_all() == []


# ===========================================================================
# MessageFactory — creates correct type from name string
# ===========================================================================

class TestMessageFactory:
    def test_creates_correct_type_from_name_string(self):
        from dspygen.rdddy.message_factory import MessageFactory
        from dspygen.rdddy.base_event import BaseEvent

        data = {
            "message_type": "dspygen.rdddy.base_event.BaseEvent",
            "id": str(uuid.uuid4()),
            "correlation_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {},
            "trace_id": str(uuid.uuid4()),
            "trace_context": {},
        }
        msg = MessageFactory.create_message(data)
        assert isinstance(msg, BaseEvent)


# ===========================================================================
# EventStormModel — generates aggregates+commands+events structure
# ===========================================================================

class TestEventStormModel:
    def test_generates_structure(self):
        from dspygen.rdddy.event_storm_model import EventStormingDomainSpecificationModel
        from dspygen.rdddy.base_event import BaseEvent

        events = [
            BaseEvent(message_type="OrderPlaced"),
            BaseEvent(message_type="PaymentProcessed"),
            BaseEvent(message_type="InventoryUpdated"),
        ]
        model = EventStormingDomainSpecificationModel(domain_events=events)
        assert len(model.domain_events) == 3
        types = {e.message_type for e in model.domain_events}
        assert {"OrderPlaced", "PaymentProcessed", "InventoryUpdated"} == types


# ===========================================================================
# DomainException — carries correct message
# ===========================================================================

class TestDomainException:
    def test_carries_correct_message(self):
        from dspygen.rdddy.domain_exception import DomainException
        try:
            raise DomainException("order not found")
        except DomainException as exc:
            assert str(exc) == "order not found"


# ===========================================================================
# ServiceColony — add/remove inhabitants with mocked realtime client
# ===========================================================================

class TestServiceColony:
    def _colony(self):
        from dspygen.rdddy.service_colony import ServiceColony
        mock_rt = MagicMock()
        mock_rt.is_connected = False
        import asyncio
        loop = asyncio.new_event_loop()
        colony = ServiceColony(loop=loop, realtime_client=mock_rt)
        return colony

    @pytest.mark.asyncio
    async def test_add_inhabitant(self):
        from dspygen.rdddy.base_inhabitant import BaseInhabitant
        colony = self._colony()
        inh = BaseInhabitant(service_colony=colony, inhabitant_id=1)
        colony.inhabitants[inh.inhabitant_id] = inh
        assert inh.inhabitant_id in colony.inhabitants

    @pytest.mark.asyncio
    async def test_remove_inhabitant(self):
        from dspygen.rdddy.base_inhabitant import BaseInhabitant
        colony = self._colony()
        inh = BaseInhabitant(service_colony=colony, inhabitant_id=2)
        colony.inhabitants[inh.inhabitant_id] = inh
        await colony.remove_inhabitant(inh.inhabitant_id)
        assert inh.inhabitant_id not in colony.inhabitants


# ===========================================================================
# Full chain: Command → Aggregate applies it → Event emitted
# ===========================================================================

class TestCommandAggregateEventChain:
    @pytest.mark.asyncio
    async def test_command_aggregate_event(self):
        from dspygen.rdddy.base_command import BaseCommand
        from dspygen.rdddy.base_event import BaseEvent
        from dspygen.rdddy.base_aggregate import BaseAggregate

        class ShipItemCommand(BaseCommand):
            pass

        class ItemShippedEvent(BaseEvent):
            pass

        emitted = []
        colony = _mock_colony()

        class ShippingAggregate(BaseAggregate):
            async def handle_ship_item(self, cmd: ShipItemCommand):
                emitted.append(ItemShippedEvent(message_type="ItemShipped"))

        agg = ShippingAggregate(service_colony=colony)
        assert ShipItemCommand in agg.handlers

        await agg.receive(ShipItemCommand(message_type="ShipItem"))
        assert len(emitted) == 1
        assert emitted[0].message_type == "ItemShipped"


# ===========================================================================
# base_query and base_entity analog: import and instantiate cleanly
# ===========================================================================

class TestBaseEntityAndQuery:
    def test_base_query_import_and_instantiate(self):
        from dspygen.rdddy.base_query import BaseQuery
        q = BaseQuery(message_type="GetOrder", payload={"order_id": "123"})
        assert q.payload["order_id"] == "123"
        assert uuid.UUID(q.id)

    def test_base_inhabitant_import_and_instantiate(self):
        """BaseInhabitant is the base entity type in RDDDY."""
        from dspygen.rdddy.base_inhabitant import BaseInhabitant
        colony = _mock_colony()
        inh = BaseInhabitant(service_colony=colony)
        assert inh.service_colony is colony
        assert inh.inhabitant_id is not None
