"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class BinaryOutputModule(dspy.Module):
    """BinaryOutputModule"""

    def forward(self, requirements):
        pred = dspy.Predict("requirements -> binary_code")
        result = pred(requirements=requirements).binary_code
        return result


from typer import Typer
app = Typer()


@app.command()
def call(requirements):
    """BinaryOutputModule"""
    init_dspy()

    print(binary_output_call(requirements=requirements))



def binary_output_call(requirements):
    binary_output = BinaryOutputModule()
    return binary_output.forward(requirements=requirements)



def main():
    init_dspy()
    requirements = "C header file example"
    print(binary_output_call(requirements=requirements))



from fastapi import APIRouter
router = APIRouter()

@router.post("/binary_output/")
async def binary_output_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return binary_output_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("BinaryOutputModule Generator")
requirements = st.text_input("Enter requirements")

if st.button("Submit BinaryOutputModule"):
    init_dspy()

    result = binary_output_call(requirements=requirements)
    st.write(result)
"""

if __name__ == "__main__":
    main()
