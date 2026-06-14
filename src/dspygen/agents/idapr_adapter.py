import abc
from typing import Any


class IDaprClientAdapter(abc.ABC):
    """Interface for adapting the Dapr client operations.

    Implementors provide a concrete backend (real Dapr SDK, mock, etc.) behind
    a stable interface so that application code never imports Dapr directly.
    """

    @abc.abstractmethod
    def start_workflow(
        self,
        workflow_component: str,
        workflow_name: str,
        input: Any,
    ) -> Any:
        """Start a new workflow instance.

        Args:
            workflow_component: The name of the Dapr workflow component to use.
            workflow_name: The registered name of the workflow to start.
            input: Arbitrary input payload passed to the workflow on start.

        Returns:
            An object with at minimum an ``instance_id`` attribute that
            identifies the newly created workflow instance.
        """

    @abc.abstractmethod
    def get_workflow(self, instance_id: str, workflow_component: str) -> Any:
        """Retrieve the current state of an existing workflow instance.

        Args:
            instance_id: The unique identifier of the workflow instance.
            workflow_component: The Dapr workflow component that owns the instance.

        Returns:
            An object with at minimum a ``runtime_status`` attribute describing
            the current state of the workflow (e.g. "Running", "Completed").
        """

    @abc.abstractmethod
    def register_workflow(self, workflow: Any) -> None:
        """Register a workflow class or callable with the runtime.

        Args:
            workflow: The workflow class or callable to register.  The exact
                type depends on the underlying Dapr SDK being wrapped.
        """

    @abc.abstractmethod
    def register_activity(self, activity: Any) -> None:
        """Register an activity class or callable with the runtime.

        Args:
            activity: The activity class or callable to register.  Activities
                are the individual units of work composed by workflows.
        """

    @abc.abstractmethod
    def raise_workflow_event(
        self,
        instance_id: str,
        workflow_component: str,
        event_name: str,
        event_data: Any,
    ) -> None:
        """Send an external event to a running workflow instance.

        Args:
            instance_id: The unique identifier of the target workflow instance.
            workflow_component: The Dapr workflow component that owns the instance.
            event_name: A string label identifying the event type.
            event_data: Arbitrary payload delivered with the event.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
