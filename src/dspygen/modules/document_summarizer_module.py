"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class DocumentSummarizerModule(dspy.Module):
    """DocumentSummarizerModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, long_document):
        pred = dspy.Predict("long_document -> summary")
        self.output = pred(long_document=long_document).summary
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(long_document):
    """DocumentSummarizerModule"""
    init_dspy()

    print(document_summarizer_call(long_document=long_document))



def document_summarizer_call(long_document):
    document_summarizer = DocumentSummarizerModule()
    return document_summarizer.forward(long_document=long_document)



def main():
    init_dspy()
    long_document = ""
    result = document_summarizer_call(long_document=long_document)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/document_summarizer/")
async def document_summarizer_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return document_summarizer_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("DocumentSummarizerModule Generator")
long_document = st.text_input("Enter long_document")

if st.button("Submit DocumentSummarizerModule"):
    init_dspy()

    result = document_summarizer_call(long_document=long_document)
    st.write(result)
"""

if __name__ == "__main__":
    main()
