"""
This is a simple documentation for the given source code. The code imports the necessary libraries and creates a Typer app. It also defines a class for an HTML module and a function for calling the module. The code also includes a streamlit component and an API router for handling requests. Finally, the code initializes the dspy library and calls the HTML module with a user input.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class HTMLModule(dspy.Module):
    """HTMLModule"""

    def forward(self, user_input):
        pred = dspy.ChainOfThought("user_input -> verbose_html_code")
        result = pred(user_input=user_input).verbose_html_code
        return result


def html_call(user_input):
    html = HTMLModule()
    return html.forward(user_input=user_input)


@app.command()
def call(user_input):
    """HTMLModule"""
    init_dspy()
    
    print(html_call(user_input=user_input))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/html/")
async def html_route(data: dict):
    # Your code generation logic here
    init_dspy(max_tokens=3000)
    
    print(data)
    return html_call(**data)


def main():
    init_dspy()
    user_input = "Quickbooks style input fields with document upload"
    print(html_call(user_input=user_input))
    

if __name__ == "__main__":
    main()
