"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class SensorDataToInsightsModule(dspy.Module):
    """SensorDataToInsightsModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, sensor_data):
        pred = dspy.Predict("sensor_data -> actionable_insights")
        self.output = pred(sensor_data=sensor_data).actionable_insights
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(sensor_data):
    """SensorDataToInsightsModule"""
    init_dspy()

    print(sensor_data_to_insights_call(sensor_data=sensor_data))



def sensor_data_to_insights_call(sensor_data):
    sensor_data_to_insights = SensorDataToInsightsModule()
    return sensor_data_to_insights.forward(sensor_data=sensor_data)



def main():
    init_dspy()
    sensor_data = ""
    result = sensor_data_to_insights_call(sensor_data=sensor_data)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/sensor_data_to_insights/")
async def sensor_data_to_insights_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return sensor_data_to_insights_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("SensorDataToInsightsModule Generator")
sensor_data = st.text_input("Enter sensor_data")

if st.button("Submit SensorDataToInsightsModule"):
    init_dspy()

    result = sensor_data_to_insights_call(sensor_data=sensor_data)
    st.write(result)
"""

if __name__ == "__main__":
    main()
