from enum import Enum, auto
from dspygen.mixin.fsm.fsm_mixin import FSMMixin, trigger


class InteractionState(Enum):
    """ Enum for states of the chatbot interaction. """
    ASKING_QUESTION = auto()
    AWAITING_ANSWER = auto()
    EVALUATING_ANSWER = auto()
    PROVIDING_FEEDBACK = auto()


class TeacherChatbot(FSMMixin):
    def __init__(self):
        super().setup_fsm(InteractionState, InteractionState.ASKING_QUESTION)

    @trigger(source=InteractionState.ASKING_QUESTION, dest=InteractionState.AWAITING_ANSWER)
    def question_asked(self):
        print("Question asked: What is the capital of France?")

    @trigger(source=InteractionState.AWAITING_ANSWER, dest=InteractionState.EVALUATING_ANSWER)
    def answer_received(self, answer):
        self.answer = answer
        print(f"Answer received: {answer}")

    @trigger(source=InteractionState.EVALUATING_ANSWER, dest=InteractionState.PROVIDING_FEEDBACK)
    def answer_evaluated(self, is_correct):
        self.is_correct = is_correct
        feedback = "Correct!" if is_correct else "That's not right, try again!"
        print(feedback)

    @trigger(source=InteractionState.PROVIDING_FEEDBACK, dest=InteractionState.ASKING_QUESTION)
    def feedback_given(self):
        print("Ready for the next question!")


def test_chatbot():
    """ Test function to simulate the chatbot interaction. """
    chatbot = TeacherChatbot()
    chatbot.question_asked()  # Transition to AWAITING_ANSWER
    chatbot.answer_received("Paris")  # Transition to EVALUATING_ANSWER
    chatbot.answer_evaluated(True)  # Transition to PROVIDING_FEEDBACK
    chatbot.feedback_given()  # Transition back to ASKING_QUESTION

    assert chatbot.state == InteractionState.ASKING_QUESTION.name

    print("Final state:", chatbot.state)
