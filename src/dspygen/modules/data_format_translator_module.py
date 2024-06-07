"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class DataFormatTranslatorModule(dspy.Module):
    """DataFormatTranslatorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, source_data):
        pred = dspy.Predict("source_data -> target_data_format")
        self.output = pred(source_data=source_data).target_data_format
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(source_data):
    """DataFormatTranslatorModule"""
    init_dspy()

    print(data_format_translator_call(source_data=source_data))



def data_format_translator_call(source_data):
    data_format_translator = DataFormatTranslatorModule()
    return data_format_translator.forward(source_data=source_data)



def main():
    init_dspy()
    source_data = ""
    result = data_format_translator_call(source_data=source_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/data_format_translator/")
async def data_format_translator_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return data_format_translator_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("DataFormatTranslatorModule Generator")
source_data = st.text_input("Enter source_data")

if st.button("Submit DataFormatTranslatorModule"):
    init_dspy()

    result = data_format_translator_call(source_data=source_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
