"""
This code imports the necessary libraries and creates a Typer app. It also defines a ProductBotModule class that inherits from dspy.Module and has a forward method that takes in a message, history, and context and returns a response. The product_bot_call function creates an instance of the ProductBotModule and calls its forward method. The code also defines a streamlit component and an API route for the product bot. Finally, the main function initializes dspy and calls the product_bot_call function with empty message, history, and context parameters.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class ProductBotModule(dspy.Module):
    """ProductBotModule"""

    def forward(self, message, history, context):
        pred = dspy.Predict("message, history, context -> response")
        result = pred(message=message, history=history, context=context).response
        return result


def product_bot_call(message, history, context):
    product_bot = ProductBotModule()
    return product_bot.forward(message=message, history=history, context=context)


@app.command()
def call(message, history, context):
    """ProductBotModule"""
    init_dspy()
    
    print(product_bot_call(message=message, history=history, context=context))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/product_bot/")
async def product_bot_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return product_bot_call(**data)


def main():
    init_dspy()
    message = ""
    history = ""
    context = ""
    print(product_bot_call(message=message, history=history, context=context))
    

if __name__ == "__main__":
    main()
