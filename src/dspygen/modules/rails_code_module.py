"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class RailsCodeModule(dspy.Module):
    """RailsCodeModule"""

    def forward(self, user_story):
        pred = dspy.Predict("user_story -> feature_code")
        result = pred(user_story=user_story).feature_code
        return result


from typer import Typer
app = Typer()


@app.command()
def call(user_story):
    """RailsCodeModule"""
    init_dspy()

    print(rails_code_call(user_story=user_story))



def rails_code_call(user_story):
    rails_code = RailsCodeModule()
    return rails_code.forward(user_story=user_story)



def main():
    init_dspy()
    user_story = ""
    print(rails_code_call(user_story=user_story))



from fastapi import APIRouter
router = APIRouter()

@router.post("/rails_code/")
async def rails_code_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return rails_code_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("RailsCodeModule Generator")
user_story = st.text_input("Enter user_story")

if st.button("Submit RailsCodeModule"):
    init_dspy()

    result = rails_code_call(user_story=user_story)
    st.write(result)
"""

if __name__ == "__main__":
    main()
