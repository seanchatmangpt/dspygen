"""
This module defines Pydantic models for artifacts commonly used in BPMN (Business Process Model and Notation) diagrams.
Artifacts are supplementary elements used to provide additional information or context within a BPMN diagram.

The artifacts defined in this module include:
- DataObject: Represents a data object in BPMN, which is used to model data used or produced by activities within a process.
- Group: Represents a group in BPMN, which is used to visually group related elements within a BPMN diagram.
- TextAnnotation: Represents a text annotation in BPMN, which is used to provide additional information or context within a BPMN diagram.
"""

from pydantic import BaseModel, Field
from typing import Optional


class DataObject(BaseModel):
    """
    Represents a data object in BPMN, which is used to model data used or produced by activities within a process.
    """
    id: str = Field(..., description="Unique identifier for the data object.")
    name: Optional[str] = Field(None, description="Name of the data object, if any.")


class Group(BaseModel):
    """
    Represents a group in BPMN, which is used to visually group related elements within a BPMN diagram.
    """
    id: str = Field(..., description="Unique identifier for the group.")
    name: Optional[str] = Field(None, description="Name of the group, if any.")


class TextAnnotation(BaseModel):
    """
    Represents a text annotation in BPMN, which is used to provide additional information or context within a BPMN diagram.
    """
    id: str = Field(..., description="Unique identifier for the text annotation.")
    text: str = Field(..., description="Text content of the annotation.")
