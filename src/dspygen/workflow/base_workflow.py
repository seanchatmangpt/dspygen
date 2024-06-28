"""
This module defines a BaseWorkflow class that serves as a reference implementation of the DaprWorkflowMixin.
The BaseWorkflow class encapsulates common functionality and provides a foundation for more specific workflows.
"""

from datetime import timedelta
import inject
from dapr.ext.workflow import DaprWorkflowContext, WorkflowActivityContext

from dspygen.workflow.workflow_mixin import DaprWorkflowMixin, register_workflow, register_activity


class BaseWorkflow(DaprWorkflowMixin):
    def __init__(self, instance_id, workflow_name, input_data, workflow_options, auto_start=True):
        super().__init__(instance_id=instance_id, 
                         workflow_name=workflow_name, 
                         input_data=input_data, 
                         workflow_options=workflow_options, 
                         auto_start=auto_start)
        self.counter = 0
        self.retry_count = 0
        self.child_orchestrator_count = 0
        self.child_orchestrator_string = ''
        self.child_act_retry_count = 0
        self.child_instance_id = 'childInstanceID'
        self.event_name = 'event1'
        self.event_data = 'eventData'
        self.non_existent_id_error = 'no such instance exists'

    @register_workflow
    def hello_world_wf(self, ctx: DaprWorkflowContext, wf_input):
        print(f'{wf_input}')
        yield ctx.call_activity(self.hello_act, input=1)
        yield ctx.call_activity(self.hello_act, input=10)
        yield ctx.call_activity(self.hello_retryable_act, retry_policy=self.retry_policy)
        yield ctx.call_child_workflow(self.child_retryable_wf, retry_policy=self.retry_policy)
        yield ctx.call_child_workflow(self.child_wf, instance_id=self.child_instance_id)
        yield ctx.call_activity(self.hello_act, input=100)
        yield ctx.call_activity(self.hello_act, input=1000)

    @register_workflow
    def child_wf(self, ctx: DaprWorkflowContext):
        yield ctx.wait_for_external_event(self.event_name)

    @register_activity
    def hello_act(self, ctx: WorkflowActivityContext, wf_input):
        self.counter += wf_input
        print(f'New counter value is: {self.counter}!', flush=True)

    @register_activity
    def hello_retryable_act(self, ctx: WorkflowActivityContext):
        if (self.retry_count % 2) == 0:
            print(f'Retry count value is: {self.retry_count}!', flush=True)
            self.retry_count += 1
            raise ValueError('Retryable Error')
        print(f'Retry count value is: {self.retry_count}! This print statement verifies retry', flush=True)
        self.retry_count += 1

    @register_workflow
    def child_retryable_wf(self, ctx: DaprWorkflowContext):
        if not ctx.is_replaying:
            self.child_orchestrator_count += 1
            print(f'Appending {self.child_orchestrator_count} to child_orchestrator_string!', flush=True)
            self.child_orchestrator_string += str(self.child_orchestrator_count)
        yield ctx.call_activity(
            self.act_for_child_wf, input=self.child_orchestrator_count, retry_policy=self.retry_policy
        )
        if self.child_orchestrator_count < 3:
            raise ValueError('Retryable Error')

    @register_activity
    def act_for_child_wf(self, ctx: WorkflowActivityContext, inp):
        inp_char = chr(96 + inp)
        print(f'Appending {inp_char} to child_orchestrator_string!', flush=True)
        self.child_orchestrator_string += inp_char
        if self.child_act_retry_count % 2 == 0:
            self.child_act_retry_count += 1
            raise ValueError('Retryable Error')
        self.child_act_retry_count += 1


# Main function to run the workflow
def main():
    from datetime import timedelta
    from time import sleep
    from dapr.ext.workflow import (
        WorkflowRuntime,
        DaprWorkflowContext,
        WorkflowActivityContext,
        RetryPolicy,
    )
    from dapr.conf import Settings
    from dapr.clients import DaprClient
    from dapr.clients.exceptions import DaprInternalError

    workflow = BaseWorkflow(
        instance_id='exampleInstanceID',
        workflow_name='hello_world_wf',
        input_data='Hi Counter!',
        workflow_options={'task_queue': 'testQueue'}
    )

    sleep(12)
    assert workflow.counter == 11
    assert workflow.retry_count == 2
    assert workflow.child_orchestrator_string == '1aa2bb3cc'
    print("All assertions passed.")

    workflow.pause_workflow()
    response = workflow.get_workflow()
    print(f'Get response from hello_world_wf after pause call: {response.runtime_status}')

    workflow.resume_workflow()
    response = workflow.get_workflow()
    print(f'Get response from hello_world')


if __name__ == '__main__':
    main()
