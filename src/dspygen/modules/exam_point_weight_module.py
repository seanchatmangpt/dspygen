"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ExamPointWeightModule(dspy.Module):
    """ExamPointWeightModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, student_question):
        pred = dspy.Predict("student_question -> exam_score")
        self.output = pred(student_question=student_question).exam_score
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(student_question):
    """ExamPointWeightModule"""
    init_dspy()

    print(exam_point_weight_call(student_question=student_question))



def exam_point_weight_call(student_question):
    exam_point_weight = ExamPointWeightModule()
    return exam_point_weight.forward(student_question=student_question)



def main():
    init_dspy()
    student_question = ""
    print(exam_point_weight_call(student_question=student_question))



from fastapi import APIRouter
router = APIRouter()

@router.post("/exam_point_weight/")
async def exam_point_weight_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return exam_point_weight_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("ExamPointWeightModule Generator")
student_question = st.text_input("Enter student_question")

if st.button("Submit ExamPointWeightModule"):
    init_dspy()

    result = exam_point_weight_call(student_question=student_question)
    st.write(result)
"""

if __name__ == "__main__":
    main()
