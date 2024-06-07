"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ImageClassifierModule(dspy.Module):
    """ImageClassifierModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, image_data):
        pred = dspy.Predict("image_data -> classification_labels")
        self.output = pred(image_data=image_data).classification_labels
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(image_data):
    """ImageClassifierModule"""
    init_dspy()

    print(image_classifier_call(image_data=image_data))



def image_classifier_call(image_data):
    image_classifier = ImageClassifierModule()
    return image_classifier.forward(image_data=image_data)



def main():
    init_dspy()
    image_data = ""
    result = image_classifier_call(image_data=image_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/image_classifier/")
async def image_classifier_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return image_classifier_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("ImageClassifierModule Generator")
image_data = st.text_input("Enter image_data")

if st.button("Submit ImageClassifierModule"):
    init_dspy()

    result = image_classifier_call(image_data=image_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
