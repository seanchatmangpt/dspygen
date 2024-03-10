"""
links.py

This module defines Pydantic models for WS-BPEL 2.0 links. Links in BPEL are used to establish relationships and dependencies between activities, particularly within structured activities that allow for parallel execution. They are crucial for controlling the execution order and conditions under which activities are started.

The models defined in this module include:
- Link: Represents a link between two activities, specifying the source and target of the link.
- Condition: Represents a condition associated with a link, determining whether the link is followed.
- LinkSource: Represents a source activity for a link, specifying the activity from which the link originates.
- LinkTarget: Represents a target activity for a link, specifying the activity where the link ends.
- LinkCondition: Represents a condition associated with a link, determining whether the link is followed.

"""

from pydantic import BaseModel, Field
from typing import Optional


class Link(BaseModel):
    """
    Represents a link between two activities, specifying the source and target of the link.
    Calculus notation: L ::= link(sourceActivity, targetActivity) where sourceActivity is the ID of the activity where the link originates, and targetActivity is the ID of the activity where the link ends.
    """
    id: str = Field(..., description="Unique identifier for the link.")
    source_activity: str = Field(..., description="Identifier of the source activity for the link.")
    target_activity: str = Field(..., description="Identifier of the target activity for the link.")
    transition_condition: Optional[str] = Field(None,
                                                description="Optional condition that determines whether the link is followed.")


class Condition(BaseModel):
    """
    Represents a condition associated with a link, determining whether the link is followed.
    This model simplifies the representation by directly associating conditions with links, but in a comprehensive BPEL model, conditions could be more complex and involve various expressions.
    """
    id: str = Field(..., description="Unique identifier for the condition.")
    expression: str = Field(..., description="Boolean expression representing the condition.")
    link_id: str = Field(..., description="Identifier of the link this condition is associated with.")


class LinkSource(BaseModel):
    """
    Represents a source activity for a link, specifying the activity from which the link originates.
    Calculus notation: L ::= link(sourceActivity, targetActivity) where sourceActivity is the ID of the activity where the link originates.
    """
    id: str = Field(..., description="Unique identifier for the link source.")
    activity_id: str = Field(..., description="Identifier of the activity where the link originates.")


class LinkTarget(BaseModel):
    """
    Represents a target activity for a link, specifying the activity where the link ends.
    Calculus notation: L ::= link(sourceActivity, targetActivity) where targetActivity is the ID of the activity where the link ends.
    """
    id: str = Field(..., description="Unique identifier for the link target.")
    activity_id: str = Field(..., description="Identifier of the activity where the link ends.")


class LinkCondition(BaseModel):
    """
    Represents a condition associated with a link, determining whether the link is followed.
    This model allows for more complex conditions involving various expressions.
    """
    id: str = Field(..., description="Unique identifier for the link condition.")
    expression: str = Field(..., description="Expression representing the condition.")
    link_id: str = Field(..., description="Identifier of the link this condition is associated with.")
