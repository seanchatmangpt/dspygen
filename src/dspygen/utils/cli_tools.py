import dspy
import typer

from dspygen.utils.dspy_tools import init_dspy


class ChatbotAssistance(dspy.Signature):
    """
    Provides guidance and assistance to users in developing projects with DSPyGen,
    leveraging the integrated chatbot functionality.
    """
    # The question or query from the user.
    question = dspy.InputField(desc="The user's query or request for assistance.")

    # The context or background information necessary for the chatbot to provide relevant assistance.
    context = dspy.InputField(desc="Background information relevant to the user's query.")

    # The history of the conversation, to maintain context and continuity.
    conversation_history = dspy.InputField(desc="Previous exchanges between the user and the chatbot, if any.")

    # The answer or guidance provided by the chatbot.
    answer = dspy.OutputField(desc="The chatbot's response to the user's query.")


def chatbot(question, context, history=""):
    if not question:
        question = typer.prompt("How can I help you?")

    qa = dspy.ChainOfThought(ChatbotAssistance)
    response = qa(question=question, context=context, conversation_history=history).answer
    history += response
    print(f"Chatbot: {response}")
    confirmed = False
    while not confirmed:
        confirm = typer.prompt("Did this answer your question? [y/N]", default="N")

        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            want = typer.prompt("How can I help more?")

            response = qa(question=want, context=context, conversation_history=history).answer
            history += response
            print(f"Chatbot: {response}")

    return history
