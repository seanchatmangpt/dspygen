"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class TranslateToASP(dspy.Signature):
    scenario_description = dspy.InputField(
        desc="Description of the user query.")
    prompt_template = dspy.InputField(
        desc="Template for the LLM prompt.")
    asp_representation = dspy.OutputField(
        desc="ASP representation of the user query.",
        prefix="Here is the translated ASP representation:\n\n")


class TranslateToASPModuleModule(dspy.Module):
    """TranslateToASPModuleModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, scenario_description, prompt_template):
        pred = dspy.Predict(TranslateToASP)
        self.output = pred(scenario_description=scenario_description, prompt_template=prompt_template).asp_representation
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(scenario_description, prompt_template):
    """TranslateToASPModuleModule"""
    init_dspy()

    print(translate_to_asp_module_call(scenario_description=scenario_description, prompt_template=prompt_template))



def translate_to_asp_module_call(scenario_description, prompt_template):
    translate_to_asp_module = TranslateToASPModuleModule()
    return translate_to_asp_module.forward(scenario_description=scenario_description, prompt_template=prompt_template)



def main():
    init_dspy()
    scenario_description = ""
    prompt_template = ""
    result = translate_to_asp_module_call(scenario_description=scenario_description, prompt_template=prompt_template)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/translate_to_asp_module/")
async def translate_to_asp_module_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return translate_to_asp_module_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("TranslateToASPModuleModule Generator")
scenario_description = st.text_input("Enter scenario_description")
prompt_template = st.text_input("Enter prompt_template")

if st.button("Submit TranslateToASPModuleModule"):
    init_dspy()

    result = translate_to_asp_module_call(scenario_description=scenario_description, prompt_template=prompt_template)
    st.write(result)
"""

if __name__ == "__main__":
    main()
