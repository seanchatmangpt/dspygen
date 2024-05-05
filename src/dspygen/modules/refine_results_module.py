"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        
class RefineWebScrapedInformation(dspy.Signature):
    """
    Refine raw information scraped from a website to match a specific learning objective,
    discarding irrelevant or unhelpful content.
    """
    raw_info = dspy.InputField(desc="Raw data or text scraped from a website.")
    learning_objective = dspy.InputField(desc="Specific learning objective to guide the refinement of information.")

    refined_info = dspy.OutputField(desc="Information refined to be relevant and helpful towards the learning objective.", prefix="```refined_info")



class RefineResultsModuleModule(dspy.Module):
    """RefineResultsModuleModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, scraped_information):
        pred = dspy.Predict(RefineWebScrapedInformation)
        self.output = pred(scraped_information=scraped_information).refined_info
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(scraped_information):
    """RefineResultsModuleModule"""
    init_dspy()

    print(refine_results_module_call(scraped_information=scraped_information))



def refine_results_module_call(scraped_information):
    refine_results_module = RefineResultsModuleModule()
    return refine_results_module.forward(scraped_information=scraped_information)



def main():
    init_dspy()
    scraped_information = ""
    result = refine_results_module_call(scraped_information=scraped_information)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/refine_results_module/")
async def refine_results_module_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return refine_results_module_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("RefineResultsModuleModule Generator")
scraped_information = st.text_input("Enter scraped_information")

if st.button("Submit RefineResultsModuleModule"):
    init_dspy()

    result = refine_results_module_call(scraped_information=scraped_information)
    st.write(result)
"""

if __name__ == "__main__":
    main()
