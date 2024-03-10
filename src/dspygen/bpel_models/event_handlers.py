"""
event_handlers.py

This module defines Pydantic models for WS-BPEL 2.0 event handlers. In BPEL, event handlers are used to specify
how a process should respond to various types of events (e.g., message reception, timeouts) that occur asynchronously
during the execution of a process.

Included models:
- EventHandler: Represents a container for all event handlers within a process, encapsulating both onMessage and onAlarm handlers.
- OnMessageHandler: Defines an event handler for receiving messages during process execution.
- OnAlarmHandler: Defines an event handler for dealing with timeouts or scheduled events.

Event handlers enhance the reactivity of business processes to internal or external events, contributing to the robustness
and flexibility of service orchestration.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class OnMessageHandler(BaseModel):
    """
    Defines an event handler for receiving messages during process execution.
    Calculus notation: E ::= onMessage(partnerLink, operation, variable) where E represents an event handler definition,
    capturing an incoming message from a specified partnerLink and operation, and storing it in a variable.
    """
    partner_link: str = Field(..., description="Partner link from which the message is received.")
    operation: str = Field(..., description="Operation associated with the incoming message.")
    variable: str = Field(..., description="Variable where the message data is stored.")

class OnAlarmHandler(BaseModel):
    """
    Defines an event handler for dealing with timeouts or scheduled events.
    Calculus notation: E ::= onAlarm(for|until, activity) where E represents an event handler for alarms,
    executing an activity after a certain duration (for) or at a specific point in time (until).
    """
    for_: Optional[str] = Field(None, description="Duration after which the event handler is triggered.")
    until: Optional[str] = Field(None, description="Specific point in time when the event handler is triggered.")
    activity: str = Field(..., description="Identifier of the activity to be executed by the event handler.")

class EventHandler(BaseModel):
    """
    Represents a container for all event handlers within a process, encapsulating both onMessage and onAlarm handlers.
    Calculus notation: EH ::= {E1, E2, ..., En} where EH represents the set of all event handlers defined in the process,
    and E1 through En are individual event handler definitions, either onMessage or onAlarm.
    """
    on_message_handlers: List[OnMessageHandler] = Field([], description="List of onMessage event handlers.")
    on_alarm_handlers: List[OnAlarmHandler] = Field([], description="List of onAlarm event handlers.")

# The EventHandler model can be used to encapsulate multiple onMessage and onAlarm handlers within a BPEL process,
# providing a structured approach to defining how the process should respond to asynchronous events.
