"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class USPConnectShipWebhookModule(dspy.Module):
    """USPConnectShipWebhookModule"""

    def forward(self, usp_input):
        pred = dspy.Predict("usp_input -> usp_xml")
        result = pred(usp_input=usp_input).usp_xml
        return result


from typer import Typer
app = Typer()


@app.command()
def call(usp_input):
    """USPConnectShipWebhookModule"""
    init_dspy()

    print(usp_connect_ship_webhook_call(usp_input=usp_input))



def usp_connect_ship_webhook_call(usp_input):
    usp_connect_ship_webhook = USPConnectShipWebhookModule()
    return usp_connect_ship_webhook.forward(usp_input=usp_input)



usp_input = """ {
    "origin": {
        "name": "John Doe",
        "address1": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
        "country": "US"
    },
    "destination": {
        "name": "Jane Smith",
        "address1": "456 Elm St",
        "city": "Othertown",
        "state": "NY",
        "zip": "67890",
        "country": "US"
    },
    "packages": [
        {
            "weight": 10,  # Weight of the package in pounds
            "dimensions": {
                "length": 12,  # Length of the package in inches
                "width": 8,    # Width of the package in inches
                "height": 6    # Height of the package in inches
            }
        },
        {
            "weight": 5,
            "dimensions": {
                "length": 10,
                "width": 6,
                "height": 4
            }
        }
    ]
}
"""


def main():
    init_dspy()
    print(usp_connect_ship_webhook_call(usp_input=usp_input))



from fastapi import APIRouter
router = APIRouter()

@router.post("/usp_connect_ship_webhook/")
async def usp_connect_ship_webhook_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return usp_connect_ship_webhook_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("USPConnectShipWebhookModule Generator")
usp_input = st.text_input("Enter usp_input")

if st.button("Submit USPConnectShipWebhookModule"):
    init_dspy()

    result = usp_connect_ship_webhook_call(usp_input=usp_input)
    st.write(result)
"""

if __name__ == "__main__":
    main()
