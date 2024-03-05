"""
This code imports the necessary libraries and creates a Typer app. It also defines a class for a JSXModule and a function for calling it. The code also includes a streamlit component and a router for a FastAPI endpoint. Finally, it initializes the dspy library and calls the JSXModule function with a given story.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        

class GeneratePureJSX(dspy.Signature):
    """
    Generate clean JSX code based on the provided context and requirements,
    ensuring compatibility with react-live environments.
    """
    context = dspy.InputField(desc="A brief description of the desired component and its functionality.")
    requirements = dspy.InputField(desc="Specific requirements or features the JSX should include.")

    pure_jsx = dspy.OutputField(desc="Clean JSX code without {}, ready for react-live.")



class JSXModule(dspy.Module):
    """JSXModule"""

    def forward(self, story):
        context = "JSX without script tags or bindings, ready for react-live"
        pred = dspy.ChainOfThought(GeneratePureJSX)
        result = pred(requirements=story,context=context).pure_jsx
        return result


def jsx_call(story):
    jsx = JSXModule()
    return jsx.forward(story=story)


@app.command()
def call(story):
    """JSXModule"""
    init_dspy()
    
    print(jsx_call(story=story))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/jsx/")
async def jsx_route(data: dict):
    # Your code generation logic here
    init_dspy(max_tokens=3000)
    
    return jsx_call(**data)


def main():
    init_dspy()
    story = "Tax form input"
    print(jsx_call(story=story))
    

if __name__ == "__main__":
    main()
