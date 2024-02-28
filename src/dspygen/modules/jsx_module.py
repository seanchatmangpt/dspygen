"""
This code imports the necessary libraries and creates a Typer app. It also defines a class for a JSXModule and a function for calling it. The code also includes a streamlit component and a router for a FastAPI endpoint. Finally, it initializes the dspy library and calls the JSXModule function with a given story.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class JSXModule(dspy.Module):
    """JSXModule"""

    def forward(self, story):
        pred = dspy.Predict("story -> react_tailwind_tsx")
        result = pred(story=story).react_tailwind_tsx
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
    init_dspy()
    
    print(data)
    return jsx_call(**data)


def main():
    init_dspy()
    story = ""
    print(jsx_call(story=story))
    

if __name__ == "__main__":
    main()
