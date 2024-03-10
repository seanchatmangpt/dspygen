"""
This module defines Pydantic models for connecting objects commonly used in BPMN (Business Process Model and Notation) diagrams.
Connecting objects represent the flow of control, data, or messages between different elements within a BPMN diagram.

The connecting objects defined in this module include:
- SequenceFlow: Represents the flow of control between two flow objects in a BPMN process.
- MessageFlow: Represents the flow of messages between two participants in a BPMN collaboration.
- Association: Represents a relationship between two elements in a BPMN diagram, such as between an artifact and a flow object.
- DataAssociation: Represents the flow of data between two elements in a BPMN process, such as between a data object and an activity.
"""

from pydantic import BaseModel, Field


class SequenceFlow(BaseModel):
    """
    Represents the flow of control between two flow objects in a BPMN process.
    """
    id: str = Field(..., description="Unique identifier for the sequence flow.")
    source_ref: str = Field(..., description="ID of the source flow object.")
    target_ref: str = Field(..., description="ID of the target flow object.")


class MessageFlow(BaseModel):
    """
    Represents the flow of messages between two participants in a BPMN collaboration.
    """
    id: str = Field(..., description="Unique identifier for the message flow.")
    source_ref: str = Field(..., description="ID of the source participant.")
    target_ref: str = Field(..., description="ID of the target participant.")


class Association(BaseModel):
    """
    Represents a relationship between two elements in a BPMN diagram.
    """
    id: str = Field(..., description="Unique identifier for the association.")
    source_ref: str = Field(..., description="ID of the source element.")
    target_ref: str = Field(..., description="ID of the target element.")


class DataAssociation(BaseModel):
    """
    Represents the flow of data between two elements in a BPMN process.
    """
    id: str = Field(..., description="Unique identifier for the data association.")
    source_ref: str = Field(..., description="ID of the source element.")
    target_ref: str = Field(..., description="ID of the target element.")
