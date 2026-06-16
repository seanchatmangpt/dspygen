"""
This module defines Pydantic models for subprocesses commonly used in BPMN (Business Process Model and Notation) diagrams.
Subprocesses represent a sequence of activities that is defined within a larger process.

The models defined in this module include:
- SubProcess: Represents a subprocess in BPMN.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class SubProcess(BaseModel):
    """
    Represents a subprocess in BPMN, which is a sequence of activities that is defined within a larger process.
    """
    id: str = Field(..., description="Unique identifier for the subprocess.")
    name: str | None = Field(None, description="Name of the subprocess, if any.")
    flow_objects: list[str] = Field(..., description="List of flow objects contained within the subprocess.")
