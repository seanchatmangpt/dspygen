"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class JsonToStructuredReportModule(dspy.Module):
    """JsonToStructuredReportModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, json_data):
        pred = dspy.Predict("json_data -> structured_report")
        self.output = pred(json_data=json_data).structured_report
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(json_data):
    """JsonToStructuredReportModule"""
    init_dspy()

    print(json_to_structured_report_call(json_data=json_data))



def json_to_structured_report_call(json_data):
    json_to_structured_report = JsonToStructuredReportModule()
    return json_to_structured_report.forward(json_data=json_data)



def main():
    init_dspy()
    json_data = ""
    result = json_to_structured_report_call(json_data=json_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/json_to_structured_report/")
async def json_to_structured_report_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return json_to_structured_report_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("JsonToStructuredReportModule Generator")
json_data = st.text_input("Enter json_data")

if st.button("Submit JsonToStructuredReportModule"):
    init_dspy()

    result = json_to_structured_report_call(json_data=json_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
