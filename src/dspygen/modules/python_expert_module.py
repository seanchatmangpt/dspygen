"""
This code imports the necessary libraries and creates a Typer app. It also defines a class for a PythonExpertModule and a function for calling it. The code also includes a streamlit component and a FastAPI router for generating code. Finally, the main function initializes the necessary libraries and calls the PythonExpertModule function.
"""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()        


class PythonExpertModule(dspy.Module):
    """PythonExpertModule"""

    def forward(self, user_story, skill_level, has_comments):
        pred = dspy.Predict("user_story, skill_level, has_comments -> python_source_code")
        result = pred(user_story=user_story, skill_level=skill_level, has_comments=has_comments).python_source_code
        return result


def python_expert_call(user_story, skill_level, has_comments: bool):
    python_expert = PythonExpertModule()
    return python_expert.forward(user_story=user_story, skill_level=skill_level, has_comments=str(has_comments))


@app.command()
def call(user_story, skill_level, has_comments):
    """PythonExpertModule"""
    init_dspy()
    
    print(python_expert_call(user_story=user_story, skill_level=skill_level, has_comments=has_comments))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/python_expert/")
async def python_expert_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return python_expert_call(**data)


def main():
    init_dspy()
    user_story = ""
    skill_level = ""
    has_comments = ""
    print(python_expert_call(user_story=user_story, skill_level=skill_level, has_comments=has_comments))
    

if __name__ == "__main__":
    main()
