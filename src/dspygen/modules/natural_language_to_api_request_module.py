"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class NaturalLanguageToAPIRequestModule(dspy.Module):
    """NaturalLanguageToAPIRequestModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, natural_language, api_schema):
        pred = dspy.Predict("natural_language, api_schema -> api_request")
        self.output = pred(natural_language=natural_language, api_schema=api_schema).api_request
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(natural_language, api_schema):
    """NaturalLanguageToAPIRequestModule"""
    init_dspy()

    print(natural_language_to_api_request_call(natural_language=natural_language, api_schema=api_schema))



def natural_language_to_api_request_call(natural_language, api_schema):
    natural_language_to_api_request = NaturalLanguageToAPIRequestModule()
    return natural_language_to_api_request.forward(natural_language=natural_language, api_schema=api_schema)



def main():
    init_dspy()
    natural_language = ""
    api_schema = ""
    result = natural_language_to_api_request_call(natural_language=natural_language, api_schema=api_schema)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/natural_language_to_api_request/")
async def natural_language_to_api_request_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return natural_language_to_api_request_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("NaturalLanguageToAPIRequestModule Generator")
natural_language = st.text_input("Enter natural_language")
api_schema = st.text_input("Enter api_schema")

if st.button("Submit NaturalLanguageToAPIRequestModule"):
    init_dspy()

    result = natural_language_to_api_request_call(natural_language=natural_language, api_schema=api_schema)
    st.write(result)
"""

if __name__ == "__main__":
    main()
