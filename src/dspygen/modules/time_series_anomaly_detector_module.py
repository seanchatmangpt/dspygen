"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class TimeSeriesAnomalyDetectorModule(dspy.Module):
    """TimeSeriesAnomalyDetectorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, time_series_data):
        pred = dspy.Predict("time_series_data -> anomalies")
        self.output = pred(time_series_data=time_series_data).anomalies
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(time_series_data):
    """TimeSeriesAnomalyDetectorModule"""
    init_dspy()

    print(time_series_anomaly_detector_call(time_series_data=time_series_data))



def time_series_anomaly_detector_call(time_series_data):
    time_series_anomaly_detector = TimeSeriesAnomalyDetectorModule()
    return time_series_anomaly_detector.forward(time_series_data=time_series_data)



def main():
    init_dspy()
    time_series_data = ""
    result = time_series_anomaly_detector_call(time_series_data=time_series_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/time_series_anomaly_detector/")
async def time_series_anomaly_detector_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return time_series_anomaly_detector_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("TimeSeriesAnomalyDetectorModule Generator")
time_series_data = st.text_input("Enter time_series_data")

if st.button("Submit TimeSeriesAnomalyDetectorModule"):
    init_dspy()

    result = time_series_anomaly_detector_call(time_series_data=time_series_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
