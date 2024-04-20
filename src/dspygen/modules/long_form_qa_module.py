"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class LongFormQAModule(dspy.Module):
    """LongFormQAModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, context, question):
        pred = dspy.Predict("context, question -> query")
        self.output = pred(context=context, question=question).query
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(context, question):
    """LongFormQAModule"""
    init_dspy()

    print(long_form_qa_call(context=context, question=question))



def long_form_qa_call(context, question):
    long_form_qa = LongFormQAModule()
    return long_form_qa.forward(context=context, question=question)



def main():
    init_dspy()
    context = ""
    question = ""
    print(long_form_qa_call(context=context, question=question))



from fastapi import APIRouter
router = APIRouter()

@router.post("/long_form_qa/")
async def long_form_qa_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return long_form_qa_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("LongFormQAModule Generator")
context = st.text_input("Enter context")
question = st.text_input("Enter question")

if st.button("Submit LongFormQAModule"):
    init_dspy()

    result = long_form_qa_call(context=context, question=question)
    st.write(result)
"""

if __name__ == "__main__":
    main()
