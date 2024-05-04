"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        

class SelectResearchSources(dspy.Signature):
    """
    Evaluate and select up to 5 sources from SERP API results that are most likely to help achieve the learning_objective.
    """
    serp_results = dspy.InputField(desc="List of search results from SERP API, including URL, title, and description of each result.")
    learning_objective = dspy.InputField(desc="Specific learning objective to guide the selection of research sources.")

    selected_sources = dspy.OutputField(desc="Up to 5 selected sources (URLs) considered most relevant for researching the learning objective.")

# How to format serp results for input
# How to parse selected_sources?


class SourceSelectorModule(dspy.Module):
    """SourceSelectorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, search_results):
        pred = dspy.Predict(SelectResearchSources)
        self.output = pred(search_results=search_results).selected_sources
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(search_results):
    """SourceSelectorModule"""
    init_dspy()

    print(source_selector_call(search_results=search_results))



def source_selector_call(search_results):
    source_selector = SourceSelectorModule()
    return source_selector.forward(search_results=search_results)



def main():
    init_dspy()
    search_results = ""
    result = source_selector_call(search_results=search_results)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/source_selector/")
async def source_selector_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return source_selector_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("SourceSelectorModule Generator")
search_results = st.text_input("Enter search_results")

if st.button("Submit SourceSelectorModule"):
    init_dspy()

    result = source_selector_call(search_results=search_results)
    st.write(result)
"""

if __name__ == "__main__":
    main()
