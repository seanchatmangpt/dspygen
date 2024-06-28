"""
This module defines a DaprWorkflowMixin for managing Dapr workflows and activities.
The mixin provides decorators to register workflows and activities, and encapsulates
the setup and execution logic to create a reusable and maintainable workflow management system.
"""
from datetime import timedelta
from typing import Any, Callable, Dict, Optional
from functools import wraps
import inject
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowContext, WorkflowActivityContext, RetryPolicy, WorkflowOptions
from dapr.clients import DaprClient
from dapr.clients.exceptions import DaprInternalError
from dapr.ext.workflow.workflow_engine import WorkflowInstanceStatus


# Settings for the example
retry = RetryPolicy(
    first_retry_interval=timedelta(seconds=1),
    max_number_of_attempts=3,
    backoff_coefficient=2,
    max_retry_interval=timedelta(seconds=10),
    retry_timeout=timedelta(seconds=100),
)


def register_workflow(workflow_func: Callable) -> Callable:
    """
    Decorator to mark a method as a workflow to be registered with the Dapr runtime.
    """
    workflow_func._is_workflow = True
    return workflow_func


def register_activity(activity_func: Callable) -> Callable:
    """
    Decorator to mark a method as an activity to be registered with the Dapr runtime.
    """
    activity_func._is_activity = True
    return activity_func


class DaprWorkflowMixin:
    @inject.autoparams()
    def __init__(
        self,
        d_client: DaprClient,
        wf_runtime: WorkflowRuntime,
        instance_id: str,
        workflow_name: str,
        input_data: Any,
        workflow_options: WorkflowOptions,
        auto_start: bool = True,
        retry_policy: RetryPolicy = retry
    ) -> None:
        self.instance_id = instance_id
        self.workflow_name = workflow_name
        self.input_data = input_data
        self.workflow_options = workflow_options
        self.d_client = d_client
        self.workflow_runtime = wf_runtime
        self.retry_policy = retry_policy
        self.auto_start = auto_start
        self._register_workflows_and_activities()

        if auto_start:
            self.start_workflow()

    def _register_workflows_and_activities(self) -> None:
        """
        Registers all methods decorated as workflows or activities with the Dapr runtime.
        """
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr):
                if hasattr(attr, '_is_workflow'):
                    self.workflow_runtime.register_workflow(attr)
                elif hasattr(attr, '_is_activity'):
                    self.workflow_runtime.register_activity(attr)

    def start_workflow(self) -> str:
        """
        Starts a workflow instance.
        """
        start_resp = self.d_client.start_workflow(
            instance_id=self.instance_id,
            workflow_component='dapr',
            workflow_name=self.workflow_name,
            input=self.input_data,
            workflow_options=self.workflow_options
        )
        print(f'Started workflow {self.workflow_name} with instance ID {start_resp.instance_id}')
        return start_resp.instance_id

    def pause_workflow(self) -> None:
        """
        Pauses a workflow instance.
        """
        self.d_client.pause_workflow(instance_id=self.instance_id, workflow_component='dapr')

    def resume_workflow(self) -> None:
        """
        Resumes a workflow instance.
        """
        self.d_client.resume_workflow(instance_id=self.instance_id, workflow_component='dapr')

    def get_workflow(self) -> WorkflowInstanceStatus:
        """
        Gets the status of a workflow instance.
        """
        return self.d_client.get_workflow(instance_id=self.instance_id, workflow_component='dapr')

    def raise_workflow_event(self, event_name: str, event_data: Any) -> None:
        """
        Raises an event for a workflow instance.
        """
        self.d_client.raise_workflow_event(
            instance_id=self.instance_id,
            workflow_component='dapr',
            event_name=event_name,
            event_data=event_data
        )

    def purge_workflow(self) -> None:
        """
        Purges a workflow instance.
        """
        self.d_client.purge_workflow(instance_id=self.instance_id, workflow_component='dapr')

    def terminate_workflow(self) -> None:
        """
        Terminates a workflow instance.
        """
        self.d_client.terminate_workflow(instance_id=self.instance_id, workflow_component='dapr')
