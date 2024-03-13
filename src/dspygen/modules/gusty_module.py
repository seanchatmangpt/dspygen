"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class GustyModule(dspy.Module):
    """GustyModule"""

    def forward(self, tasks):
        pred = dspy.Predict("tasks -> dsl_yaml")
        result = pred(tasks=tasks).dsl_yaml
        return result


from typer import Typer
app = Typer()


@app.command()
def call(tasks):
    """GustyModule"""
    init_dspy()

    print(gusty_call(tasks=tasks))



def gusty_call(tasks):
    gusty = GustyModule()
    return gusty.forward(tasks=tasks)



def main():
    init_dspy()
    tasks = ""
    print(gusty_call(tasks=tasks))



from fastapi import APIRouter
router = APIRouter()

@router.post("/gusty/")
async def gusty_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return gusty_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("GustyModule Generator")
tasks = st.text_input("Enter tasks")

if st.button("Submit GustyModule"):
    init_dspy()

    result = gusty_call(tasks=tasks)
    st.write(result)
"""

if __name__ == "__main__":
    main()
