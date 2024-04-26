import asyncio
from transitions import Machine
from transitions.extensions.states import add_state_features, Tags
from enum import Enum, auto

from dspygen.rdddy.base_actor import BaseActor
from dspygen.rdddy.base_command import BaseCommand
from dspygen.rdddy.base_event import BaseEvent
from dspygen.rdddy.actor_system import ActorSystem
from dspygen.utils.dspy_tools import init_dspy


# Enhancing state features for more complex state behavior
@add_state_features(Tags)
class CustomStateMachine(Machine):
    pass


# Enum for Dialogue States
class SocratesState(Enum):
    IDLE = auto()
    ASKING_QUESTION = auto()
    EVALUATING_RESPONSE = auto()
    CHALLENGING = auto()
    FOLLOW_UP = auto()
    CONCLUDING = auto()


class StudentState(Enum):
    IDLE = auto()
    RESPONDING = auto()
    CONSIDERING_FOLLOW_UP = auto()
    REVIEWING_FEEDBACK = auto()


# Commands
class AskQuestionCommand(BaseCommand):
    """Socrates asks a question."""


class AnswerCommand(BaseCommand):
    """Student provides an answer."""


class EvaluateResponseCommand(BaseCommand):
    """Evaluate the student's response."""


class ChallengeCommand(BaseCommand):
    """Issue a challenge based on the response."""


class FollowUpQuestionCommand(BaseCommand):
    """Ask a follow-up question."""


class ConcludeDialogueCommand(BaseCommand):
    """Conclude the dialogue positively."""


# Events
class QuestionAskedEvent(BaseEvent):
    """Question has been asked."""


class AnswerReceivedEvent(BaseEvent):
    """Answer has been received from the student."""


class ResponseEvaluatedEvent(BaseEvent):
    """Response has been evaluated."""


class ChallengeIssuedEvent(BaseEvent):
    """Challenge has been issued to the student."""


class FollowUpAskedEvent(BaseEvent):
    """Follow-up question has been asked."""


class ConcludeDialogueEvent(BaseEvent):
    """Dialogue has been concluded."""


class SocratesActor(BaseActor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine = CustomStateMachine(model=self, states=SocratesState, initial=SocratesState.IDLE)
        self.machine.add_transition(trigger='ask_question', source=SocratesState.IDLE, dest=SocratesState.ASKING_QUESTION)
        self.machine.add_transition(trigger='evaluate_response', source=SocratesState.ASKING_QUESTION, dest=SocratesState.EVALUATING_RESPONSE)
        self.machine.add_transition(trigger='issue_challenge', source=SocratesState.EVALUATING_RESPONSE, dest=SocratesState.CHALLENGING)
        self.machine.add_transition(trigger='ask_follow_up', source=SocratesState.CHALLENGING, dest=SocratesState.FOLLOW_UP)
        self.machine.add_transition(trigger='conclude_dialogue', source=SocratesState.FOLLOW_UP, dest=SocratesState.CONCLUDING)

    async def handle_AskQuestionCommand(self, message: AskQuestionCommand):
        question = "What led you to this conclusion about unchanged prices?"
        await self.publish(QuestionAskedEvent(content=question))

    async def handle_EvaluateResponseCommand(self, message: EvaluateResponseCommand):
        evaluation = "Evaluating the student's response..."
        await self.publish(ResponseEvaluatedEvent(content=evaluation))

    async def handle_ChallengeCommand(self, message: ChallengeCommand):
        challenge = "How do you reconcile your view with data on local climate effects?"
        await self.publish(ChallengeIssuedEvent(content=challenge))

    async def handle_FollowUpQuestionCommand(self, message: FollowUpQuestionCommand):
        follow_up = "Considering your response, how would different climates affect the issue?"
        await self.publish(FollowUpAskedEvent(content=follow_up))

    async def handle_ConcludeDialogueCommand(self, message: ConcludeDialogueCommand):
        conclusion = "Excellent discussion today! You've navigated through the complexities adeptly."
        await self.publish(ConcludeDialogueEvent(content=conclusion))


class StudentActor(BaseActor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine = CustomStateMachine(model=self, states=StudentState, initial=StudentState.IDLE)
        self.machine.add_transition(trigger='respond', source=StudentState.IDLE, dest=StudentState.RESPONDING)
        self.machine.add_transition(trigger='consider_follow_up', source=StudentState.RESPONDING, dest=StudentState.CONSIDERING_FOLLOW_UP)
        self.machine.add_transition(trigger='review_feedback', source=[StudentState.CONSIDERING_FOLLOW_UP, StudentState.RESPONDING], dest=StudentState.REVIEWING_FEEDBACK)

    async def handle_AnswerCommand(self, message: AnswerCommand):
        response = "If prices don't change despite the parasites, maybe the impact isn’t as severe."
        await self.publish(AnswerReceivedEvent(content=response))

    async def handle_FollowUpQuestionCommand(self, message: FollowUpQuestionCommand):
        consideration = "Perhaps the environment or climate could be different?"
        await self.publish(FollowUpAskedEvent(content=consideration))


def state_transition_possibilities(actor):
    transition_dict = {}
    for event in actor.machine.events:
        if event.startswith('to_'):
            continue

        # Check if a transition to this state is possible
        transition_possible = getattr(actor.machine.model, f'may_{event}')()
        if transition_possible:
            transition_dict[event] = transition_possible
    return transition_dict


async def main():
    init_dspy()

    actor_system = ActorSystem()
    socrates_actor = await actor_system.actor_of(SocratesActor)
    student_actor = await actor_system.actor_of(StudentActor)

    # Socrates starts the dialogue
    await actor_system.publish(AskQuestionCommand(content="You suggest that the expectation of unchanged prices in Mississippi next year, despite the ongoing issues, weakens the prediction about the parasite's impact outside Mississippi. What led you to this conclusion?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Student responds
    await actor_system.publish(AnswerCommand(content="I thought if prices don't change despite the parasites, maybe the impact isn’t as severe, so the same might happen outside Mississippi."))
    await asyncio.sleep(1)  # Simulate processing time

    # Socrates dives deeper
    await actor_system.publish(FollowUpQuestionCommand(content="Interesting thought. Let's explore further—what factors could potentially influence the severity of the parasite attack outside Mississippi, distinct from what's happening in Mississippi?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Student speculates on environmental factors
    await actor_system.publish(AnswerCommand(content="Maybe the environment or climate could be different?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Socrates pushes for more detailed analysis
    await actor_system.publish(FollowUpQuestionCommand(content="Indeed, environmental differences can greatly affect such situations. Given this, what else might differ in an environment that could influence the impact of parasites?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Student considers biological interactions
    await actor_system.publish(AnswerCommand(content="Could it be something like different plants or maybe animals that interact with the parasites?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Socrates confirms and extends the discussion
    await actor_system.publish(FollowUpQuestionCommand(content="Precisely, interactions with local flora and fauna can indeed play a significant role. How might the presence of certain animals affect the situation with parasites outside Mississippi?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Student acknowledges the role of natural controls
    await actor_system.publish(AnswerCommand(content="If there are animals that eat or control these parasites, they could reduce the damage?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Socrates clarifies and concludes
    await actor_system.publish(FollowUpQuestionCommand(content="Exactly. So, if such a natural control exists outside Mississippi, might that change your view on how the unchanged prices in Mississippi relate to the broader impact of parasites?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Student realizes the implications
    await actor_system.publish(AnswerCommand(content="Yes, I see now. If there are natural controls outside Mississippi, the unchanged prices in Mississippi might not really tell us what could happen elsewhere."))
    await asyncio.sleep(1)  # Simulate processing time

    # Socrates concludes with a reflection
    await actor_system.publish(ConcludeDialogueCommand(content="Very well reasoned! Considering these natural differences, how do you think this knowledge could help us better prepare or adjust agricultural strategies?"))
    await asyncio.sleep(1)  # Simulate processing time

    # Student offers a final insight
    await actor_system.publish(AnswerCommand(content="It seems like understanding and possibly enhancing these natural controls could be important for managing the parasites better."))
    await asyncio.sleep(1)  # Simulate processing time

    # Socrates praises the discussion
    await actor_system.publish(ConcludeDialogueCommand(content="Excellent discussion today! You've adeptly navigated through the complexities of agricultural impacts and the role of local ecological conditions. Your ability to reconsider your initial assumptions when presented with new information shows a strong critical thinking capability. Very well done."))

    print("Dialogue completed.")


if __name__ == '__main__':
    asyncio.run(main())
