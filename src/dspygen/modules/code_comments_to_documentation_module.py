"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class CodeCommentsToDocumentationModule(dspy.Module):
    """CodeCommentsToDocumentationModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, code_comments):
        pred = dspy.Predict("code_comments -> documentation")
        self.output = pred(code_comments=code_comments).documentation
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(code_comments):
    """CodeCommentsToDocumentationModule"""
    init_dspy()

    print(code_comments_to_documentation_call(code_comments=code_comments))



def code_comments_to_documentation_call(code_comments):
    code_comments_to_documentation = CodeCommentsToDocumentationModule()
    return code_comments_to_documentation.forward(code_comments=code_comments)



def main():
    init_dspy()
    code_comments = ""
    result = code_comments_to_documentation_call(code_comments=code_comments)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/code_comments_to_documentation/")
async def code_comments_to_documentation_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return code_comments_to_documentation_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("CodeCommentsToDocumentationModule Generator")
code_comments = st.text_input("Enter code_comments")

if st.button("Submit CodeCommentsToDocumentationModule"):
    init_dspy()

    result = code_comments_to_documentation_call(code_comments=code_comments)
    st.write(result)
"""

if __name__ == "__main__":
    main()
