import pytest
import inject
from unittest.mock import create_autospec
from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowContext, WorkflowActivityContext
from durabletask.task import OrchestrationContext, ActivityContext


@pytest.fixture(scope='session')
def mock_dapr_client():
    """Fixture to provide a mocked DaprClient."""
    return create_autospec(DaprClient, instance=True)


@pytest.fixture(scope='session')
def mock_workflow_runtime():
    """Fixture to provide a mocked WorkflowRuntime."""
    return create_autospec(WorkflowRuntime, instance=True)


@pytest.fixture(scope='session')
def configure_inject(mock_dapr_client, mock_workflow_runtime):
    """Configure inject to use mock dependencies for the duration of the test session."""

    def _configure(binder):
        binder.bind_to_provider(DaprClient, lambda: mock_dapr_client)
        binder.bind_to_provider(WorkflowRuntime, lambda: mock_workflow_runtime)

    # Clear existing configuration and reconfigure
    inject.clear_and_configure(_configure)

    yield

    # Optionally clear inject after the tests to clean up
    inject.clear()



@pytest.fixture
def mock_orchestration_context():
    """Fixture to provide a mocked OrchestrationContext."""
    return create_autospec(OrchestrationContext, instance=True)

@pytest.fixture
def mock_activity_context():
    """Fixture to provide a mocked ActivityContext."""
    return create_autospec(ActivityContext, instance=True)

@pytest.fixture
def dapr_workflow_context(mock_orchestration_context):
    """Fixture to create an instance of DaprWorkflowContext with a mocked OrchestrationContext."""
    return DaprWorkflowContext(ctx=mock_orchestration_context)

@pytest.fixture
def workflow_activity_context(mock_activity_context):
    """Fixture to create an instance of WorkflowActivityContext with a mocked ActivityContext."""
    return WorkflowActivityContext(ctx=mock_activity_context)
