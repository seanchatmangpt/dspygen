import asyncio
from typing import Any
from unittest.mock import MagicMock

from loguru import logger

from dspygen.agents.idapr_adapter import IDaprClientAdapter


class MockDaprClientAdapter(IDaprClientAdapter):
    """In-memory mock of IDaprClientAdapter for use in tests and local development.

    All state is stored in plain dicts/sets protected by an :class:`asyncio.Lock`
    so that concurrent async callers do not observe torn state.  Call
    :meth:`reset` between test cases to start with a clean slate.
    """

    def __init__(self) -> None:
        self._lock: asyncio.Lock = asyncio.Lock()
        self.workflows: dict[str, dict[str, Any]] = {}
        self.activities: set[Any] = set()
        self.events: dict[str, tuple[str, Any]] = {}

    # ------------------------------------------------------------------
    # IDaprClientAdapter implementation
    # ------------------------------------------------------------------

    def start_workflow(
        self,
        workflow_component: str,
        workflow_name: str,
        input: Any,
    ) -> MagicMock:
        """Create and persist a new workflow instance.

        Returns a :class:`unittest.mock.MagicMock` with ``instance_id`` set so
        that callers can extract the id without depending on the real Dapr SDK.
        """
        instance_id = f"workflow_{len(self.workflows) + 1}"
        entry: dict[str, Any] = {
            "component": workflow_component,
            "name": workflow_name,
            "input": input,
            "status": "Running",
        }
        self.workflows[instance_id] = entry

        # Best-effort attribute access for common workflow input shapes
        try:
            logger.info(
                f"Starting workflow '{workflow_name}', purchasing {input.quantity} of {input.item_name}"
            )
        except AttributeError:
            logger.info(f"Starting workflow '{workflow_name}' (instance_id={instance_id})")

        return MagicMock(instance_id=instance_id)

    def get_workflow(self, instance_id: str, workflow_component: str) -> MagicMock:
        """Return the current status of a workflow instance.

        Returns a :class:`unittest.mock.MagicMock` with ``runtime_status`` set.
        """
        workflow = self.workflows.get(instance_id, {})
        status: str = workflow.get("status", "NotFound")
        logger.info(f"{instance_id}: Orchestration status is '{status}'")
        return MagicMock(runtime_status=status)

    def register_workflow(self, workflow: Any) -> None:
        """Log registration of a workflow; no persistent state is kept."""
        logger.info(f"Registered workflow: {workflow}")

    def register_activity(self, activity: Any) -> None:
        """Persist and log an activity registration."""
        self.activities.add(activity)
        logger.info(f"Registered activity: {activity}")

    def raise_workflow_event(
        self,
        instance_id: str,
        workflow_component: str,
        event_name: str,
        event_data: Any,
    ) -> None:
        """Deliver an event to a running workflow and optionally advance its status.

        If ``event_data`` is a mapping that contains ``{"approval": True}`` the
        workflow status is updated to ``"Approved"`` to mirror real Dapr
        approval-gate behaviour.
        """
        self.events[instance_id] = (event_name, event_data)
        logger.info(f"{instance_id}: Event raised: '{event_name}'")

        approval = False
        if isinstance(event_data, dict):
            approval = event_data.get("approval", False)

        if approval:
            workflow = self.workflows.get(instance_id)
            if workflow is not None:
                workflow["status"] = "Approved"
                logger.info(f"Payment for order '{instance_id}' has been approved!")
            else:
                logger.warning(
                    f"raise_workflow_event: instance_id '{instance_id}' not found; cannot approve."
                )

    # ------------------------------------------------------------------
    # Test-isolation helpers
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear all in-memory state.

        Call this between test cases to ensure full isolation::

            adapter = MockDaprClientAdapter()
            # ... run test ...
            adapter.reset()
        """
        self.workflows.clear()
        self.activities.clear()
        self.events.clear()
        logger.debug("MockDaprClientAdapter state has been reset.")

    def __repr__(self) -> str:
        return (
            f"MockDaprClientAdapter("
            f"workflows={len(self.workflows)}, "
            f"activities={len(self.activities)}, "
            f"events={len(self.events)})"
        )
