"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class GeoCoordinatesToLocationModule(dspy.Module):
    """GeoCoordinatesToLocationModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, geo_coordinates):
        pred = dspy.Predict("geo_coordinates -> location_names")
        self.output = pred(geo_coordinates=geo_coordinates).location_names
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(geo_coordinates):
    """GeoCoordinatesToLocationModule"""
    init_dspy()

    print(geo_coordinates_to_location_call(geo_coordinates=geo_coordinates))



def geo_coordinates_to_location_call(geo_coordinates):
    geo_coordinates_to_location = GeoCoordinatesToLocationModule()
    return geo_coordinates_to_location.forward(geo_coordinates=geo_coordinates)



def main():
    init_dspy()
    geo_coordinates = ""
    result = geo_coordinates_to_location_call(geo_coordinates=geo_coordinates)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/geo_coordinates_to_location/")
async def geo_coordinates_to_location_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return geo_coordinates_to_location_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("GeoCoordinatesToLocationModule Generator")
geo_coordinates = st.text_input("Enter geo_coordinates")

if st.button("Submit GeoCoordinatesToLocationModule"):
    init_dspy()

    result = geo_coordinates_to_location_call(geo_coordinates=geo_coordinates)
    st.write(result)
"""

if __name__ == "__main__":
    main()
