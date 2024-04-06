"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class PytsModule(dspy.Module):
    """PytsModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, python_code):
        pred = dspy.Predict("python_code -> typescript_code")
        self.output = pred(python_code=python_code).typescript_code
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(python_code):
    """PytsModule"""
    init_dspy()

    print(pyts_call(python_code=python_code))



def pyts_call(python_code):
    pyts = PytsModule()
    return pyts.forward(python_code=python_code)



def main():
    init_dspy()
    python_code = ""
    print(pyts_call(python_code=python_code))



from fastapi import APIRouter
router = APIRouter()

@router.post("/pyts/")
async def pyts_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return pyts_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("PytsModule Generator")
python_code = st.text_input("Enter python_code")

if st.button("Submit PytsModule"):
    init_dspy()

    result = pyts_call(python_code=python_code)
    st.write(result)
"""

if __name__ == "__main__":
    main()
