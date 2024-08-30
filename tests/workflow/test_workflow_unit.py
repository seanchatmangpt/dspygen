import pytest
from dspygen.workflow.workflow_models import Workflow, Job, Action, CronTrigger
from dspygen.workflow.workflow_executor import execute_workflow, execute_job, execute_action

def test_workflow_creation():
    workflow = Workflow(
        name="TestWorkflow",
        triggers=[CronTrigger(cron="0 0 * * *")],
        jobs=[
            Job(
                name="TestJob",
                runner="python",
                steps=[
                    Action(
                        name="TestAction",
                        code="print('Hello, World!')"
                    )
                ]
            )
        ]
    )
    assert workflow.name == "TestWorkflow"
    assert len(workflow.triggers) == 1
    assert isinstance(workflow.triggers[0], CronTrigger)
    assert workflow.triggers[0].cron == "0 0 * * *"
    assert len(workflow.jobs) == 1

def test_execute_action(capsys):
    action = Action(
        name="TestAction",
        code="print('Hello, World!')"
    )
    context = {}
    new_context = execute_action(action, context)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!"
    assert new_context == {}

def test_execute_job(capsys):
    job = Job(
        name="TestJob",
        runner="python",
        steps=[
            Action(
                name="TestAction1",
                code="print('Action 1')"
            ),
            Action(
                name="TestAction2",
                code="print('Action 2')"
            )
        ]
    )
    context = {}
    new_context = execute_job(job, context)
    captured = capsys.readouterr()
    assert "Action 1" in captured.out
    assert "Action 2" in captured.out
    assert new_context == {}

def test_execute_workflow(capsys):
    workflow = Workflow(
        name="TestWorkflow",
        triggers=[CronTrigger(cron="0 0 * * *")],
        jobs=[
            Job(
                name="TestJob1",
                runner="python",
                steps=[
                    Action(
                        name="TestAction1",
                        code="print('Job 1, Action 1')"
                    )
                ]
            ),
            Job(
                name="TestJob2",
                runner="python",
                steps=[
                    Action(
                        name="TestAction2",
                        code="print('Job 2, Action 1')"
                    )
                ]
            )
        ]
    )
    execute_workflow(workflow)
    captured = capsys.readouterr()
    assert "Job 1, Action 1" in captured.out
    assert "Job 2, Action 1" in captured.out
