"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy

from enum import Enum


class MermaidDiagramType(Enum):
    FLOWCHART = "flowchart"
    SEQUENCE_DIAGRAM = "sequenceDiagram"
    CLASS_DIAGRAM = "classDiagram"
    STATE_DIAGRAM = "stateDiagram-v2"
    ENTITY_RELATIONSHIP_DIAGRAM = "erDiagram"
    USER_JOURNEY = "journey"
    GANTT = "gantt"
    PIE_CHART = "pie"
    QUADRANT_CHART = "quadrantChart"
    REQUIREMENT_DIAGRAM = "requirementDiagram"
    GITGRAPH = "gitGraph"
    MINDMAP = "mindmap"
    TIMELINE = "timeline"
    SANKEY = "sankey"


diagram_desc = """Type of Mermaid diagram. E.g., flowchart, sequenceDiagram, 
classDiagram, stateDiagram-v2, erDiagram, journey, gantt, pie, 
quadrantChart, requirementDiagram, gitGraph, mindmap, timeline"""


class MermaidSignature(dspy.Signature):
    """
    Generate MermaidJS code.
    """
    # Input fields
    prompt = dspy.InputField(desc="Detailed description or instructions")
    mermaid_type = dspy.InputField(desc=diagram_desc)

    # Output fields
    documentation = dspy.OutputField(desc="Documentation for the code.")
    mermaid_js_code = dspy.OutputField(desc="Generated MermaidJS code matching the prompt and mermaid_type.",
                                       prefix="```mermaid\n")


class MermaidJSModule(dspy.Module):
    """MermaidJSModule"""

    def forward(self, prompt, mermaid_type=MermaidDiagramType.FLOWCHART):
        pred = dspy.Predict(MermaidSignature)
        result = pred(prompt=prompt, mermaid_type=mermaid_type.value)
        output = result.mermaid_js_code.rstrip('```')
        return output


from typer import Typer

app = Typer()


@app.command()
def call(prompt):
    """MermaidJSModule"""
    init_dspy()

    print(mermaid_js_call(prompt=prompt))


def mermaid_js_call(prompt, mermaid_type=MermaidDiagramType.FLOWCHART):
    mermaid_js = MermaidJSModule()
    return mermaid_js.forward(prompt=prompt, mermaid_type=mermaid_type)


def main():
    init_dspy()
    # init_dspy(model="gpt-4")
    prompt = "Example sales video chart for Camunda of Ticket Booking with gRPC, AMQP, and REST APIs."
    print(mermaid_js_call(prompt=prompt, mermaid_type=MermaidDiagramType.FLOWCHART))


from fastapi import APIRouter

router = APIRouter()


@router.post("/mermaid_js/")
async def mermaid_js_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return mermaid_js_call(**data)


"""
import streamlit as st


# Streamlit form and display
st.title("MermaidJSModule Generator")
prompt = st.text_input("Enter prompt")

if st.button("Submit MermaidJSModule"):
    init_dspy()

    result = mermaid_js_call(prompt=prompt)
    st.write(result)
"""

if __name__ == "__main__":
    main()
