"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        

class EvaluateInformationSufficiency(dspy.Signature):
    """
    Assess whether the information scraped from various sources is sufficient to meet a specified learning objective.
    """
    sources_info = dspy.InputField(desc="Dictionary or list of pairs containing URLs of sources and the corresponding information scraped from these sources.")
    learning_objective = dspy.InputField(desc="Specific learning objective used to evaluate the sufficiency of the information.")

    decision = dspy.OutputField(desc="Boolean value indicating whether the information is sufficient for the learning objective. Must be a 0 or a 1, where 1 is sufficient and 0 is insufficient.", prefix="```decision")



class ConditionSufficientInfoModule(dspy.Module):
    """ConditionSufficientInfoModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, refined_information):
        pred = dspy.Predict(EvaluateInformationSufficiency)
        self.output = pred(refined_information=refined_information).decision
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(refined_information):
    """ConditionSufficientInfoModule"""
    init_dspy()

    print(condition_sufficient_info_call(refined_information=refined_information))



def condition_sufficient_info_call(refined_information):
    condition_sufficient_info = ConditionSufficientInfoModule()
    return condition_sufficient_info.forward(refined_information=refined_information)



def main():
    init_dspy()
    refined_information = ""
    result = condition_sufficient_info_call(refined_information=refined_information)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/condition_sufficient_info/")
async def condition_sufficient_info_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return condition_sufficient_info_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("ConditionSufficientInfoModule Generator")
refined_information = st.text_input("Enter refined_information")

if st.button("Submit ConditionSufficientInfoModule"):
    init_dspy()

    result = condition_sufficient_info_call(refined_information=refined_information)
    st.write(result)
"""

if __name__ == "__main__":
    main()
