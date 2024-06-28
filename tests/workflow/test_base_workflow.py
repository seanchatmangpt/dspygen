# test_base_workflow.py
import pytest
from unittest.mock import MagicMock, call
import inject

from dspygen.workflow.base_workflow import BaseWorkflow


@pytest.fixture
def base_workflow(mock_dapr_client, mock_workflow_runtime, configure_inject):
    """Fixture to create an instance of BaseWorkflow with mocked dependencies."""
    return BaseWorkflow(
        instance_id='testInstanceID',
        workflow_name='hello_world_wf',
        input_data='Hi Counter!',
        workflow_options={'task_queue': 'testQueue'},
        auto_start=False
    )

def test_workflow_initialization(base_workflow):
    """Test the initialization of the BaseWorkflow class."""
    assert base_workflow.instance_id == 'testInstanceID'
    assert base_workflow.workflow_name == 'hello_world_wf'
    assert base_workflow.input_data == 'Hi Counter!'
    assert not base_workflow.auto_start
    assert base_workflow.counter == 0

def test_start_workflow(base_workflow, mock_dapr_client):
    """Test starting a workflow."""
    mock_dapr_client.start_workflow.return_value = MagicMock(instance_id='testInstanceID')
    instance_id = base_workflow.start_workflow()

    mock_dapr_client.start_workflow.assert_called_once_with(
        instance_id='testInstanceID',
        workflow_component='dapr',
        workflow_name='hello_world_wf',
        input='Hi Counter!',
        workflow_options={'task_queue': 'testQueue'}
    )
    assert instance_id == 'testInstanceID'

def test_pause_and_resume_workflow(base_workflow, mock_dapr_client):
    """Test pausing and resuming a workflow."""
    base_workflow.pause_workflow()
    base_workflow.resume_workflow()

    mock_dapr_client.pause_workflow.assert_called_once_with(
        instance_id='testInstanceID',
        workflow_component='dapr'
    )
    mock_dapr_client.resume_workflow.assert_called_once_with(
        instance_id='testInstanceID',
        workflow_component='dapr'
    )

def test_raise_event(base_workflow, mock_dapr_client):
    """Test raising an event in a workflow."""
    event_name = "testEvent"
    event_data = {"key": "value"}
    base_workflow.raise_workflow_event(event_name, event_data)

    mock_dapr_client.raise_workflow_event.assert_called_once_with(
        instance_id='testInstanceID',
        workflow_component='dapr',
        event_name=event_name,
        event_data=event_data
    )

def test_workflow_activity_handling(base_workflow):
    """Test the handling of workflow activities and error handling in retryable activities."""
    base_workflow.hello_act(None, 10)
    assert base_workflow.counter == 10

    # Simulate a retry scenario
    with pytest.raises(ValueError):
        base_workflow.hello_retryable_act(None)
    assert base_workflow.retry_count == 1  # Retry count should increase after the error

def test_child_workflow_handling(base_workflow, mock_dapr_client):
    """Test the handling of child workflows and the orchestration of activities within them."""
    # Mock the necessary parts
    ctx = MagicMock()
    ctx.is_replaying = False
    base_workflow.child_retryable_wf(ctx)

    expected_calls = [
        call.call_activity(
            base_workflow.act_for_child_wf, input=1, retry_policy=base_workflow.retry_policy
        )
    ]
    assert ctx.mock_calls[:1] == expected_calls
    assert base_workflow.child_orchestrator_string == '1'