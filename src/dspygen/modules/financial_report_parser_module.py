"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class FinancialReportParserModule(dspy.Module):
    """FinancialReportParserModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, financial_report):
        pred = dspy.Predict("financial_report -> parsed_data")
        self.output = pred(financial_report=financial_report).parsed_data
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(financial_report):
    """FinancialReportParserModule"""
    init_dspy()

    print(financial_report_parser_call(financial_report=financial_report))



def financial_report_parser_call(financial_report):
    financial_report_parser = FinancialReportParserModule()
    return financial_report_parser.forward(financial_report=financial_report)



def main():
    init_dspy()
    financial_report = ""
    result = financial_report_parser_call(financial_report=financial_report)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/financial_report_parser/")
async def financial_report_parser_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return financial_report_parser_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("FinancialReportParserModule Generator")
financial_report = st.text_input("Enter financial_report")

if st.button("Submit FinancialReportParserModule"):
    init_dspy()

    result = financial_report_parser_call(financial_report=financial_report)
    st.write(result)
"""

if __name__ == "__main__":
    main()
