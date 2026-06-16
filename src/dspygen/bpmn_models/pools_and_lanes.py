"""
This module defines Pydantic models for pools and lanes commonly used in BPMN (Business Process Model and Notation) diagrams.
Pools and lanes are used to visually organize and categorize elements within a BPMN diagram.

The models defined in this module include:
- Pool: Represents a pool in BPMN, which is a graphical container for grouping related elements within a BPMN diagram.
- Lane: Represents a lane in BPMN, which is a sub-division of a pool used to group and organize elements within a BPMN diagram.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class Pool(BaseModel):
    """
    Represents a pool in BPMN, which is a graphical container for grouping related elements within a BPMN diagram.
    """
    id: str = Field(..., description="Unique identifier for the pool.")
    name: str | None = Field(None, description="Name of the pool, if any.")
    participants: list[str] = Field(..., description="List of participants represented by the pool.")


class Lane(BaseModel):
    """
    Represents a lane in BPMN, which is a sub-division of a pool used to group and organize elements within a BPMN diagram.
    """
    id: str = Field(..., description="Unique identifier for the lane.")
    name: str | None = Field(None, description="Name of the lane, if any.")
    pool_ref: str = Field(..., description="ID of the pool to which the lane belongs.")
    flow_objects: list[str] = Field(..., description="List of flow objects contained within the lane.")
