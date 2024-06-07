"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class CustomerFeedbackClassifierModule(dspy.Module):
    """CustomerFeedbackClassifierModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, customer_feedback):
        pred = dspy.Predict("customer_feedback -> feedback_categories")
        self.output = pred(customer_feedback=customer_feedback).feedback_categories
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(customer_feedback):
    """CustomerFeedbackClassifierModule"""
    init_dspy()

    print(customer_feedback_classifier_call(customer_feedback=customer_feedback))



def customer_feedback_classifier_call(customer_feedback):
    customer_feedback_classifier = CustomerFeedbackClassifierModule()
    return customer_feedback_classifier.forward(customer_feedback=customer_feedback)



def main():
    init_dspy()
    customer_feedback = ""
    result = customer_feedback_classifier_call(customer_feedback=customer_feedback)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/customer_feedback_classifier/")
async def customer_feedback_classifier_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return customer_feedback_classifier_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("CustomerFeedbackClassifierModule Generator")
customer_feedback = st.text_input("Enter customer_feedback")

if st.button("Submit CustomerFeedbackClassifierModule"):
    init_dspy()

    result = customer_feedback_classifier_call(customer_feedback=customer_feedback)
    st.write(result)
"""

if __name__ == "__main__":
    main()
