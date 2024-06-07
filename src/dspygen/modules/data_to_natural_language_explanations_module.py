"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class DataToNaturalLanguageExplanationsModule(dspy.Module):
    """DataToNaturalLanguageExplanationsModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, data_points):
        pred = dspy.Predict("data_points -> explanations")
        self.output = pred(data_points=data_points).explanations
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(data_points):
    """DataToNaturalLanguageExplanationsModule"""
    init_dspy()

    print(data_to_natural_language_explanations_call(data_points=data_points))



def data_to_natural_language_explanations_call(data_points):
    data_to_natural_language_explanations = DataToNaturalLanguageExplanationsModule()
    return data_to_natural_language_explanations.forward(data_points=data_points)



def main():
    init_dspy()
    data_points = ""
    result = data_to_natural_language_explanations_call(data_points=data_points)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/data_to_natural_language_explanations/")
async def data_to_natural_language_explanations_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return data_to_natural_language_explanations_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("DataToNaturalLanguageExplanationsModule Generator")
data_points = st.text_input("Enter data_points")

if st.button("Submit DataToNaturalLanguageExplanationsModule"):
    init_dspy()

    result = data_to_natural_language_explanations_call(data_points=data_points)
    st.write(result)
"""

if __name__ == "__main__":
    main()
