"""
This module defines Pydantic models for different types of events commonly used in BPMN (Business Process Model and Notation) diagrams.
Events represent something that happens during the course of a process and can trigger the flow of control within a BPMN process.

The event models defined in this module include:
- Event: Represents a generic event in BPMN.
- BoundaryEvent: Represents an event attached to an activity boundary in a BPMN process.
- EscalationEvent: Represents an event triggered by an escalation in a BPMN process.
- CompensationEvent: Represents an event used to handle compensation activities in a BPMN process.
- TimerEvent: Represents an event triggered based on a predefined time or duration in a BPMN process.
- SignalEvent: Represents an event triggered by the sending or receiving of a signal in a BPMN process.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Event(BaseModel):
    """
    Represents a generic event in BPMN.
    """
    id: str = Field(..., description="Unique identifier for the event.")
    name: Optional[str] = Field(None, description="Name of the event, if any.")


class BoundaryEvent(Event):
    """
    Represents an event attached to an activity boundary in a BPMN process.
    """
    attached_to_ref: str = Field(..., description="ID of the activity to which the boundary event is attached.")


class EscalationEvent(Event):
    """
    Represents an event triggered by an escalation in a BPMN process.
    """
    escalation_code: str = Field(..., description="Code or identifier for the escalation triggering the event.")


class CompensationEvent(Event):
    """
    Represents an event used to handle compensation activities in a BPMN process.
    """
    compensation_code: str = Field(..., description="Code or identifier for the compensation triggering the event.")


class TimerEvent(Event):
    """
    Represents an event triggered based on a predefined time or duration in a BPMN process.
    """
    timer_expression: str = Field(..., description="Expression specifying the time or duration triggering the event.")


class SignalEvent(Event):
    """
    Represents an event triggered by the sending or receiving of a signal in a BPMN process.
    """
    signal_name: str = Field(..., description="Name or identifier of the signal triggering the event.")
