"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ExtractMetricsFromLogsModule(dspy.Module):
    """ExtractMetricsFromLogsModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, log_files):
        pred = dspy.Predict("log_files -> key_metrics")
        self.output = pred(log_files=log_files).key_metrics
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(log_files):
    """ExtractMetricsFromLogsModule"""
    init_dspy()

    print(extract_metrics_from_logs_call(log_files=log_files))



def extract_metrics_from_logs_call(log_files):
    extract_metrics_from_logs = ExtractMetricsFromLogsModule()
    return extract_metrics_from_logs.forward(log_files=log_files)



def main():
    init_dspy()
    log_files = ""
    result = extract_metrics_from_logs_call(log_files=log_files)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/extract_metrics_from_logs/")
async def extract_metrics_from_logs_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return extract_metrics_from_logs_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("ExtractMetricsFromLogsModule Generator")
log_files = st.text_input("Enter log_files")

if st.button("Submit ExtractMetricsFromLogsModule"):
    init_dspy()

    result = extract_metrics_from_logs_call(log_files=log_files)
    st.write(result)
"""

if __name__ == "__main__":
    main()
