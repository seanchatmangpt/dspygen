"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class TextSummarizerModule(dspy.Module):
    """TextSummarizerModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, text):
        pred = dspy.Predict("text -> summary")
        self.output = pred(text=text).summary
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(text):
    """TextSummarizerModule"""
    init_dspy()

    print(text_summarizer_call(text=text))



def text_summarizer_call(text):
    text_summarizer = TextSummarizerModule()
    return text_summarizer.forward(text=text)



def main():
    init_dspy()
    text = ""
    result = text_summarizer_call(text=text)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/text_summarizer/")
async def text_summarizer_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return text_summarizer_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("TextSummarizerModule Generator")
text = st.text_input("Enter text")

if st.button("Submit TextSummarizerModule"):
    init_dspy()

    result = text_summarizer_call(text=text)
    st.write(result)
"""

if __name__ == "__main__":
    main()
