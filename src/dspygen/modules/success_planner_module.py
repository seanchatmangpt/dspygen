"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class SuccessPlannerModule(dspy.Module):
    """SuccessPlannerModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, bio):
        pred = dspy.Predict("bio -> success_path")
        self.output = pred(bio=bio).success_path
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(bio):
    """SuccessPlannerModule"""
    init_dspy()

    print(success_planner_call(bio=bio))



def success_planner_call(bio):
    success_planner = SuccessPlannerModule()
    return success_planner.forward(bio=bio)



def main():
    init_dspy()
    bio = ""
    print(success_planner_call(bio=bio))



from fastapi import APIRouter
router = APIRouter()

@router.post("/success_planner/")
async def success_planner_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return success_planner_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("SuccessPlannerModule Generator")
bio = st.text_input("Enter bio")

if st.button("Submit SuccessPlannerModule"):
    init_dspy()

    result = success_planner_call(bio=bio)
    st.write(result)
"""

if __name__ == "__main__":
    main()
