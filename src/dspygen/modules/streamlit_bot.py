"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


import dspy

class GenerateStreamlitComponents(dspy.Signature):
    """
    Generate Streamlit components source code based on project and page information.
    Do not return ```
    """
    project = dspy.InputField(desc="Information or context about the project.")
    page = dspy.InputField(desc="Specific details or requirements for the Streamlit page.")

    streamlit_components_source_code = dspy.OutputField(desc="Generated source code for Streamlit components to make the page functional.",
                                                        prefix="```python\n")



class StreamlitBotModule(dspy.Module):
    """StreamlitBotModule"""

    def forward(self, project, page):
        page += "\nProvide detailed streamlit components that would make the page functional"
        pred = dspy.ChainOfThought(GenerateStreamlitComponents)
        result = pred(project=project, page=page).streamlit_components_source_code
        return result


from typer import Typer
app = Typer()


@app.command()
def call(project, page):
    """StreamlitBotModule"""
    init_dspy()

    print(streamlit_bot_call(project=project, page=page))



def streamlit_bot_call(project, page):
    streamlit_bot = StreamlitBotModule()
    return streamlit_bot.forward(project=project, page=page)



def main():
    init_dspy()
    project = ""
    page = ""
    print(streamlit_bot_call(project=project, page=page))



from fastapi import APIRouter
router = APIRouter()

@router.post("/streamlit_bot/")
async def streamlit_bot_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return streamlit_bot_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("StreamlitBotModule Generator")
project = st.text_input("Enter project")
page = st.text_input("Enter page")

if st.button("Submit StreamlitBotModule"):
    init_dspy()

    result = streamlit_bot_call(project=project, page=page)
    st.write(result)
"""

if __name__ == "__main__":
    main()
