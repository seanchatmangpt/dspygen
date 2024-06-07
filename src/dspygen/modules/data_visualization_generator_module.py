"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class DataVisualizationGeneratorModule(dspy.Module):
    """DataVisualizationGeneratorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, raw_data):
        pred = dspy.Predict("raw_data -> visualizations")
        self.output = pred(raw_data=raw_data).visualizations
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(raw_data):
    """DataVisualizationGeneratorModule"""
    init_dspy()

    print(data_visualization_generator_call(raw_data=raw_data))



def data_visualization_generator_call(raw_data):
    data_visualization_generator = DataVisualizationGeneratorModule()
    return data_visualization_generator.forward(raw_data=raw_data)



def main():
    init_dspy()
    raw_data = ""
    result = data_visualization_generator_call(raw_data=raw_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/data_visualization_generator/")
async def data_visualization_generator_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return data_visualization_generator_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("DataVisualizationGeneratorModule Generator")
raw_data = st.text_input("Enter raw_data")

if st.button("Submit DataVisualizationGeneratorModule"):
    init_dspy()

    result = data_visualization_generator_call(raw_data=raw_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
