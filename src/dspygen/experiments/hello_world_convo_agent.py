import asyncio

import dspy

from dspygen.rdddy.abstract_actor import AbstractActor
from dspygen.rdddy.abstract_command import AbstractCommand
from dspygen.rdddy.abstract_event import AbstractEvent
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.utils.dspy_tools import init_dspy


class AskQuestionCommand(AbstractCommand):
    """Command for asking a question."""


class AnswerQuestionCommand(AbstractCommand):
    """Command for answering a question."""


class QuestionAskedEvent(AbstractEvent):
    """Event for when a question has been asked."""


class AnswerProvidedEvent(AbstractEvent):
    """Event for when an answer has been provided."""


class SocraticTeacherActor(AbstractActor):
    async def handle_cmd(self, command: AskQuestionCommand):
        # Logic to formulate a question
        pred = dspy.ChainOfThought("ask -> question")
        question = pred(ask=command.content).question
        print(f"Student asks: {command.content}, Teacher asks: {question}")
        await self.publish(QuestionAskedEvent(content=question))

    async def handle_evt(self, event: AnswerProvidedEvent):
        # React to the student's answer and potentially ask a follow-up question
        pred = dspy.ChainOfThought("answer -> follow_up_question")
        follow_up_question = pred(answer=event.content).follow_up_question
        print(f"Student answers: {event.content}, Teacher asks: {follow_up_question}")
        await self.publish(AskQuestionCommand(content=follow_up_question))


class StudentActor(AbstractActor):
    async def handle_cmd(self, command: AnswerQuestionCommand):
        # The student processes the question and provides an answer
        pred = dspy.ChainOfThought("question -> answer")
        answer = pred(question=command.content).answer
        print(f"Teacher asks: {command.content}, Student answers: {answer}")
        await self.publish(AnswerProvidedEvent(content=answer))

    async def handle_evt(self, event: QuestionAskedEvent):
        print(f"Teacher asks: {event.content}")
        # Student thinks and then responds
        pred = dspy.ChainOfThought("thought -> response")
        response = pred(thought=event.content).response
        print(f"Student thinks: {event.content}, Student responds: {response}")
        await self.publish(AnswerQuestionCommand(content=response))


async def main():
    init_dspy()
    actor_system = ActorSystem()
    teacher_actor = await actor_system.actor_of(SocraticTeacherActor)
    student_actor = await actor_system.actor_of(StudentActor)

    # Start the dialogue with an initial question
    await actor_system.publish(AskQuestionCommand(content="the significance of learning."))

    # The loop continues based on the actors' responses and the system's design
    # For demonstration, let's simulate a short delay to see the conversation unfold
    await asyncio.sleep(10)

    print("Dialogue completed.")


if __name__ == '__main__':
    asyncio.run(main())
