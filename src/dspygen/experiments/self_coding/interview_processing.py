import dspy

from dspygen.lm.groq_lm import Groq
from dspygen.utils.dspy_tools import init_dspy

class ContextEstablishment(dspy.Signature):
    """Sets the stage for the interaction, providing necessary background."""
    story = dspy.InputField(desc="The narrative story or scenario.")
    context = dspy.OutputField(desc="The context for the interaction.")

class ChallengePresentation(dspy.Signature):
    """Presents a challenge to be addressed by the Interviewee."""
    context = dspy.InputField(desc="Background and details of the current challenge.")
    challenge = dspy.OutputField(desc="The specific challenge to be addressed.")

class ModuleSelection(dspy.Signature):
    """Selects a DSPy module to address the presented challenge."""
    challenge = dspy.InputField(desc="The challenge needing resolution.")
    selected_module = dspy.OutputField(desc="The DSPy module selected to solve the challenge.")

class AssertionAndSuggestionEvaluation(dspy.Signature):
    """Evaluates the selected module against Assertions and Suggestions."""
    selected_module = dspy.InputField(desc="The module selected for the challenge.")
    evaluation_result = dspy.OutputField(desc="Outcome of the evaluation against Assertions and Suggestions.")

class FeedbackAndRetry(dspy.Signature):
    """Provides feedback on the module selection and handles the Retry mechanism."""
    evaluation_result = dspy.InputField(desc="The outcome of the evaluation.")
    retry_decision = dspy.OutputField(desc="Decision on whether to retry with a different module or refine the approach.")




def main2():
    """Main function"""
    init_dspy(Groq, max_tokens=1000, model="llama3-70b-8192") # for Groq you must pass the Groq existing model

    story = ("You are a software engineer preparing for a technical interview. "
             "You have been given a coding challenge to solve. The challenge involves a NuxtJS frontend with a Convex API backend. ")

    # Establish the context for the interaction
    context = dspy.ChainOfThought(ContextEstablishment)(story=story).context

    # Present the challenge to the Interviewee
    challenge = dspy.ChainOfThought(ChallengePresentation)(context=context).challenge

    # Select a DSPy module to address the challenge
    selected_module = dspy.ChainOfThought(ModuleSelection)(challenge=challenge).selected_module

    # Evaluate the selected module against Assertions and Suggestions
    evaluation_result = dspy.ChainOfThought(AssertionAndSuggestionEvaluation)(selected_module=selected_module).evaluation_result

    # Provide feedback and handle the Retry mechanism
    retry_decision = dspy.ChainOfThought(FeedbackAndRetry)(evaluation_result=evaluation_result).retry_decision

    print(f"Context: {context}")
    print(f"Challenge: {challenge}")
    print(f"Selected Module: {selected_module}")
    print(f"Evaluation Result: {evaluation_result}")
    print(f"Retry Decision: {retry_decision}")


def main():
    """"""
    dspy.Suggest
    dspy.Assert


if __name__ == '__main__':
    #main()
    main2()
