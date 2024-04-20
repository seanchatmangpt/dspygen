"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class FAANGModule(dspy.Module):
    """FAANGModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, job_interview_take_home_project):
        pred = dspy.Predict("job_interview_take_home_project -> ideal_candidate_source_code")
        self.output = pred(job_interview_take_home_project=job_interview_take_home_project).ideal_candidate_source_code
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(job_interview_take_home_project):
    """FAANGModule"""
    init_dspy()

    print(faang_call(job_interview_take_home_project=job_interview_take_home_project))



def faang_call(job_interview_take_home_project):
    faang = FAANGModule()
    return faang.forward(job_interview_take_home_project=job_interview_take_home_project)



def main():
    init_dspy()
    job_interview_take_home_project = ""
    print(faang_call(job_interview_take_home_project=job_interview_take_home_project))



from fastapi import APIRouter
router = APIRouter()

@router.post("/faang/")
async def faang_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return faang_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("FAANGModule Generator")
job_interview_take_home_project = st.text_input("Enter job_interview_take_home_project")

if st.button("Submit FAANGModule"):
    init_dspy()

    result = faang_call(job_interview_take_home_project=job_interview_take_home_project)
    st.write(result)
"""

if __name__ == "__main__":
    main()
