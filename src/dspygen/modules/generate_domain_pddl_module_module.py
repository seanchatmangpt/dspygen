"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


class GenerateDomainPDDL(dspy.Signature):
    domain_content = dspy.InputField(
        desc="Content for the PDDL domain file.")
    domain_file = dspy.OutputField(
        desc="PDDL domain file path.",
        prefix="Here is the generated domain PDDL file path:\n\n")


class GenerateDomainPDDLModuleModule(dspy.Module):
    """GenerateDomainPDDLModuleModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, domain_content):
        pred = dspy.Predict(GenerateDomainPDDL)
        self.output = pred(domain_content=domain_content).domain_file
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(domain_content):
    """GenerateDomainPDDLModuleModule"""
    init_dspy()

    print(generate_domain_pddl_module_call(domain_content=domain_content))



def generate_domain_pddl_module_call(domain_content):
    generate_domain_pddl_module = GenerateDomainPDDLModuleModule()
    return generate_domain_pddl_module.forward(domain_content=domain_content)



def main():
    init_dspy()
    domain_content = ""
    result = generate_domain_pddl_module_call(domain_content=domain_content)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/generate_domain_pddl_module/")
async def generate_domain_pddl_module_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return generate_domain_pddl_module_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("GenerateDomainPDDLModuleModule Generator")
domain_content = st.text_input("Enter domain_content")

if st.button("Submit GenerateDomainPDDLModuleModule"):
    init_dspy()

    result = generate_domain_pddl_module_call(domain_content=domain_content)
    st.write(result)
"""

if __name__ == "__main__":
    main()
