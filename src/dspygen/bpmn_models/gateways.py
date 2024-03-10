"""
This module defines Pydantic models for different types of gateways commonly used in BPMN (Business Process Model and Notation) diagrams.
Gateways represent decision points or branching points within a process flow, where the flow of control can diverge or converge.

The gateway models defined in this module include:
- Gateway: Represents a generic gateway in BPMN.
"""

from pydantic import BaseModel, Field
from typing import Optional

class Gateway(BaseModel):
    """
    Represents a generic gateway in BPMN.
    """
    id: str = Field(..., description="Unique identifier for the gateway.")
    name: Optional[str] = Field(None, description="Name of the gateway, if any.")
    gateway_type: str = Field(..., description="Type of the gateway, such as 'exclusive', 'inclusive', 'parallel', etc.")
