import asyncio
from transitions import Machine
from enum import Enum, auto

import dspy

from dspygen.rdddy.base_inhabitant import BaseInhabitant
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.base_event import BaseEvent
from dspygen.rdddy.service_colony import ServiceColony
from dspygen.utils.dspy_tools import init_dspy


class AskQuestionCommand(BaseCommand):
    """Command for asking a question."""


class AnswerQuestionCommand(BaseCommand):
    """Command for answering a question."""


class QuestionAskedEvent(BaseEvent):
    """Event for when a question has been asked."""


class AnswerProvidedEvent(BaseEvent):
    """Event for when an answer has been provided."""


class SocraticTeacherInhabitant(BaseInhabitant):
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


class StudentInhabitant(BaseInhabitant):
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


async def main2():
    init_dspy()
    service_colony = ServiceColony()
    teacher_inhabitant= await service_colony.inhabitant_of(SocraticTeacherInhabitant)
    student_inhabitant= await service_colony.inhabitant_of(StudentInhabitant)

    # Start the dialogue with an initial question
    await service_colony.publish(AskQuestionCommand(content="the significance of learning."))

    # The loop continues based on the inhabitants' responses and the system's design
    # For demonstration, let's simulate a short delay to see the conversation unfold
    await asyncio.sleep(10)

    print("Dialogue completed.")


class TeacherState(Enum):
    IDLE = auto()
    ASKING = auto()
    WAITING_FOR_ANSWER = auto()


class StudentState(Enum):
    IDLE = auto()
    THINKING = auto()
    ANSWERING = auto()


class StateInhabitant(BaseInhabitant):
    states = [state.name for state in TeacherState]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine = Machine(model=self, states=StateInhabitant.states, initial=TeacherState.IDLE)
        self.machine.add_transition(trigger='ask', source=TeacherState.IDLE, dest=TeacherState.ASKING)
        self.machine.add_transition(trigger='receive_answer', source=TeacherState.ASKING,
                                    dest=TeacherState.WAITING_FOR_ANSWER)
        # Add other transitions as necessary

    async def handle_cmd(self, command: AskQuestionCommand):
        # State-based logic for asking a question
        # print(str(self.__dict__))
        # with open("state_inhabitant.txt", "a") as f:
        #     f.write(str(self.__dict__))
        print(f"State transition possibilities: {state_transition_possibilities(self)}")
        assert not self.may_receive_answer()  # not ready yet :(

        # Logic to formulate a question


def state_transition_possibilities(inhabitant):
    transition_dict = {}
    for event in inhabitant.machine.events:
        if event.startswith('to_'):
            continue

        # Check if a transition to this state is possible
        transition_possible = getattr(inhabitant.machine.model, f'may_{event}')()
        transition_dict[event] = transition_possible
    return transition_dict


async def main():
    init_dspy()

    service_colony = ServiceColony()
    teacher_inhabitant= await service_colony.inhabitant_of(StateInhabitant)

    # Start the dialogue with an initial question
    await service_colony.publish(AskQuestionCommand(content="the significance of learning."))

    # The loop continues based on the inhabitants' responses and the system's design
    # For demonstration, let's simulate a short delay to see the conversation unfold
    await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
