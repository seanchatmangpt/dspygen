"""
This module defines Pydantic models for different types of flow objects commonly used in BPMN (Business Process Model and Notation) diagrams.
Flow objects represent work that is performed within a process and include tasks and subprocesses.

The flow object models defined in this module include:
- Task: Represents a task in BPMN, which is a unit of work that is performed within a process.
- SubProcess: Represents a subprocess in BPMN, which is a sequence of activities that is defined within a larger process.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    """
    Represents a task in BPMN, which is a unit of work that is performed within a process.
    """
    id: str = Field(..., description="Unique identifier for the task.")
    name: Optional[str] = Field(None, description="Name of the task, if any.")


class SubProcess(BaseModel):
    """
    Represents a subprocess in BPMN, which is a sequence of activities that is defined within a larger process.
    """
    id: str = Field(..., description="Unique identifier for the subprocess.")
    name: Optional[str] = Field(None, description="Name of the subprocess, if any.")
