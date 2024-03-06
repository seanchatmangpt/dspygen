from dspygen.modules.insight_tweet_module import insight_tweet_call
from dspygen.rdddy.abstract_actor import AbstractActor
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.rdddy.abstract_message import *
from dspygen.utils.dspy_tools import init_dspy


class StatusQuery(AbstractQuery):
    """Find out the status of the workflow engine."""


class StartCommand(AbstractCommand):
    """Start the workflow."""


class StopCommand(AbstractCommand):
    """Stop the workflow."""


class StatusEvent(AbstractEvent):
    """Status has changed."""


class JobCommand(AbstractCommand):
    tasks: list[str]


class TweetEvent(AbstractEvent):
    """Tweets has been generated."""


class WorkflowEngine(AbstractActor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        self.status = "idle"

    async def handle_status(self, query: StatusQuery):
        print(f"Status: {self.status}")

    async def handle_start(self, command: StartCommand):
        self.status = "waiting"
        print("Starting workflow engine...")
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
            text = insight_tweet_call(task)
            await self.publish(TweetEvent(content=f"twitter-cli tweet='{text}'"))

        print("Tasks done.")
        await self.publish(StopCommand())




async def main():
    asys = ActorSystem()
    engine = await asys.actor_of(WorkflowEngine)

    await asys.publish(StartCommand())
    # await asys.publish(StatusQuery())
    await asys.publish(JobCommand(tasks=["Elon Musk is a Lizard Person, prove me wrong?",
                                         "I am the smartest all time. Thomas Edison Quote"]))

    while True:
        await asyncio.sleep(5)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
