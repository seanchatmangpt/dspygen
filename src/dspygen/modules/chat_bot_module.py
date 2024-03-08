"""
The source code imports the necessary libraries and defines a class for a chatbot module. The `forward` function takes in a message, history, and context and uses a `Predict` object to generate a response. The `chat_bot_call` function initializes the chatbot module and calls the `forward` function. The `call` function is used to call the chatbot module with user input. The `chat_bot_route` function is used to handle requests from a web API. The `main` function initializes the chatbot module and calls the `chat_bot_call` function with empty inputs.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class ChatBotModule(dspy.Module):
    """ChatBotModule"""

    def forward(self, message, history, context):
        pred = dspy.ChainOfThought("message, history, context -> response")
        result = pred(message=message, history=history, context=context).response
        return result


def chat_bot_call(message, history, context):
    chat_bot = ChatBotModule()
    return chat_bot.forward(message=message, history=history, context=context)


@app.command()
def call(message, history, context):
    """ChatBotModule"""
    init_dspy()
    
    print(chat_bot_call(message=message, history=history, context=context))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()


@router.post("/chat_bot/")
async def chat_bot_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return chat_bot_call(**data)


def main():
    init_dspy(max_tokens=3000)
    message = "How do I change my oil?"
    history = ""
    # API to get manual
    # context = "1965 mustang manual"
    context = "Just bought a 1965 mustang. I need a 25 point instruction guide."
    print(chat_bot_call(message=message, history=history, context=context))
    

if __name__ == "__main__":
    main()
