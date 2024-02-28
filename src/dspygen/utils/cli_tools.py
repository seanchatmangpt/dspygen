import dspy
import typer

from dspygen.utils.dspy_tools import init_dspy


def chatbot(question, context, history=""):
    init_dspy(max_tokens=3000)

    qa = dspy.ChainOfThought("question, context -> answer")
    response = qa(question=question, context=context).answer
    history += response
    print(f"Chatbot: {response}")
    confirmed = False
    while not confirmed:
        confirm = typer.prompt("Did this answer your question? [y/N]", default="N")

        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            want = typer.prompt("How can I help more?")

            question = f"{history}\n{want}"
            question = question[-1000:]

            response = qa(question=question, context=context).answer
            history += response
            print(f"Chatbot: {response}")

    return history