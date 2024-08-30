import os
import pytest
from dspygen.workflow.workflow_models import Workflow, DateTrigger
from dspygen.workflow.workflow_executor import execute_workflow, schedule_workflow
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time
from loguru import logger

# Add this at the beginning of the file to set up verbose logging
logger.add("test_workflow_integration.log", level="DEBUG", rotation="1 MB")

@pytest.fixture
def workflow_yaml(tmp_path):
    output_file = tmp_path / "test_output.txt"
    logger.debug(f"Creating workflow YAML with output file: {output_file}")
    return f"""
name: TestWorkflow
triggers:
  - type: date
    run_date: now
jobs:
  - name: TestJob
    runner: python
    steps:
      - name: TestAction
        code: |
          print("hello world")
          with open('{output_file}', 'w') as f:
            f.write('Integration test successful')
    """

@pytest.fixture(scope="module")
def scheduler():
    logger.debug("Creating BackgroundScheduler")
    scheduler = BackgroundScheduler()
    scheduler.start()
    yield scheduler
    logger.debug("Shutting down BackgroundScheduler")
    scheduler.shutdown()

def test_workflow_execution_from_yaml(workflow_yaml, tmp_path):
    logger.info("Starting test_workflow_execution_from_yaml")
    yaml_path = tmp_path / "test_workflow.yaml"
    with open(yaml_path, "w") as f:
        f.write(workflow_yaml)
    logger.debug(f"Saved workflow YAML to: {yaml_path}")

    workflow = Workflow.from_yaml(str(yaml_path))
    logger.debug(f"Created workflow object: {workflow}")
    execute_workflow(workflow)

    output_file = tmp_path / "test_output.txt"
    logger.debug(f"Checking output file: {output_file}")
    with open(output_file, "r") as f:
        content = f.read()
    logger.info(f"Output file content: {content}")
    assert content == "Integration test successful"
    logger.info("test_workflow_execution_from_yaml completed successfully")

