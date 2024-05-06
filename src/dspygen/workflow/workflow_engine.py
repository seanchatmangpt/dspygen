from pydantic import Field

from dspygen.rdddy.base_actor import BaseActor
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.base_event import BaseEvent
from dspygen.rdddy.base_query import BaseQuery
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.utils.dspy_tools import init_dspy
from dspygen.workflow.workflow_executor import execute_workflow
from dspygen.workflow.workflow_models import Workflow

from loguru import logger

class StatusQuery(BaseQuery):
    """Find out the status of the workflow engine."""


class StartCommand(BaseCommand):
    """Start the workflow."""
    wf_path: str = Field(..., description="Path to the workflow YAML file.")


class StopCommand(BaseCommand):
    """Stop the workflow."""


class StatusEvent(BaseEvent):
    """Status has changed."""


class JobCommand(BaseCommand):
    tasks: list[str]


class WorkflowEngine(BaseActor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        self.status = "idle"

    async def handle_status(self, query: StatusQuery):
        print(f"Status: {self.status}")

    async def handle_start(self, command: StartCommand):
        if self.status != "idle":
            print("Workflow engine is not idle.")
            return

        self.status = "loading"
        print("Loading workflow from YAML...")
        try:
            await self.publish(StatusEvent(content=self.status))
            print("Workflow is running...")
            wf = Workflow.from_yaml(command.wf_path)
            context = execute_workflow(wf)

            await self.publish(StatusEvent(content=self.status))

            # Optionally, use the context for further actions or status updates
        except Exception as e:
            logger.error(f"Failed to load or execute workflow: {e}")
            self.status = "error"

        await self.publish(StatusEvent(content=self.status))

    async def handle_stop(self, command: StopCommand):
        self.status = "idle"
        print("Stop workflow engine...")
        await self.publish(StatusEvent(content=self.status))

    async def handle_job(self, command: JobCommand):
        init_dspy()

        if self.status != "waiting":
            print("Not ready.")
            return

        for task in command.tasks:
            print(task)

        print("Tasks done.")
        await self.publish(StopCommand())


async def main():
    asys = ActorSystem()
    engine = await asys.actor_of(WorkflowEngine)

    wf_path = "/Users/sac/dev/dspygen/src/dspygen/workflow/data_analysis_workflow.yaml"
    await asys.publish(StartCommand(wf_path=wf_path))

    while True:
        await asyncio.sleep(5)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
