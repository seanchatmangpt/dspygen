"""
activities.py

This module defines Pydantic models for WS-BPEL 2.0 activities. Activities are the fundamental building blocks of BPEL processes,
defining the business logic and the sequence of operations that are executed within a process.

Included models:
- InvokeActivity: Represents an activity to invoke an operation on a partner Web service.
- ReceiveActivity: Represents an activity that waits for a message from an external partner.
- AssignActivity: Represents an activity for assigning values to variables within the process.
- WaitActivity: Represents an activity that pauses the process execution for a specified duration.
- SequenceActivity: Represents a structured activity that executes a series of activities in a sequential order.
- FlowActivity: Represents a structured activity that allows for concurrent execution of activities.
- PickActivity: Represents a structured activity that waits for one out of several possible events to occur.
- IfActivity: Represents a structured activity that executes one set of activities if a condition is true, and another set if false.
- WhileActivity: Represents a structured activity that repeatedly executes a set of activities while a condition is true.
- RepeatUntilActivity: Represents a structured activity that repeatedly executes a set of activities until a condition becomes true.
- CompensateActivity: Represents an activity that triggers compensation logic for previously executed activities within a scope.
- ThrowActivity: Represents an activity that explicitly throws a fault, causing the process to terminate with a faulted state.
- TerminateActivity: Represents an activity that abruptly terminates the process instance.
- ValidateActivity: Represents an activity that performs validation on a specified variable or data.
- RethrowActivity: Represents an activity that rethrows a caught fault, propagating it to the parent scope for handling.
- CompensateScopeActivity: Represents an activity that triggers compensation logic for the entire scope in which it is defined.
- EmptyActivity: Represents an empty activity, which has no effect on the process execution.
- ScopeActivity: Represents a scoped group of activities with its own local context, including variables, fault handlers, and more.
- ForLoopActivity: Represents a loop activity with a defined start, end, and increment, iterating over a block of activities.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Activity(BaseModel):
    """Placeholder for Activities"""


class InvokeActivity(Activity):
    """
    Represents an activity to invoke an operation on a partner Web service.
    Calculus notation: A ::= invoke(L, operation, inputVariable?, outputVariable?) where L is the partnerLink,
    operation is the operation to be invoked, and inputVariable/outputVariable are the optional variables for the invocation.
    """
    id: str = Field(..., description="Unique identifier for the invoke activity.")
    partner_link: str = Field(..., description="Partner link used for the invocation.")
    operation: str = Field(..., description="Operation to invoke on the partner service.")
    input_variable: Optional[str] = Field(None, description="Variable containing data to send.")
    output_variable: Optional[str] = Field(None, description="Variable to store the response from the invocation.")


class ReceiveActivity(Activity):
    """
    Represents an activity that waits for a message from an external partner.
    Calculus notation: A ::= receive(L, operation, variable, createInstance?) where L is the partnerLink,
    operation is the operation associated with the message, variable is where the message should be stored,
    and createInstance is an optional boolean that indicates if this receive activity should create a new process instance.
    """
    id: str = Field(..., description="Unique identifier for the receive activity.")
    partner_link: str = Field(..., description="Partner link expecting a message.")
    operation: str = Field(..., description="Operation associated with the expected message.")
    variable: str = Field(..., description="Variable to store the received message.")
    create_instance: Optional[bool] = Field(None,
                                            description="Whether this activity should initiate a new process instance.")


class AssignActivity(Activity):
    """
    Represents an activity for assigning values to variables within the process.
    Calculus notation: A ::= assign(from, to) where from is an expression or variable value to be assigned,
    and to is the variable or part of a variable that will receive the value.
    """
    id: str = Field(..., description="Unique identifier for the assign activity.")
    from_expression: str = Field(..., description="Expression or variable value to assign from.")
    to_variable: str = Field(..., description="Variable or variable part to assign to.")


class WaitActivity(Activity):
    """
    Represents an activity that pauses the process execution for a specified duration or until a certain condition is met.
    Calculus notation: A ::= wait(for|until) where 'for' is a duration and 'until' is a deadline expression.
    """
    id: str = Field(..., description="Unique identifier for the wait activity.")
    for_: Optional[str] = Field(None, description="Duration to wait for.")
    until: Optional[str] = Field(None, description="Deadline expression to wait until.")


class SequenceActivity(Activity):
    """
    Represents a structured activity that executes a series of activities in a sequential order.
    Calculus notation: A ::= sequence(Activities) where Activities is a list of activities to be executed in order.
    """
    id: str = Field(..., description="Unique identifier for the sequence activity.")
    activities: List[str] = Field(..., description="List of activity identifiers to be executed in sequence.")


class FlowActivity(Activity):
    """
    Represents a structured activity that allows for concurrent execution of activities.
    Calculus notation: A ::= flow(Activities) where Activities is a list of activities that may execute concurrently.
    """
    id: str = Field(..., description="Unique identifier for the flow activity.")
    activities: List[str] = Field(..., description="List of activity identifiers to be executed concurrently.")


class PickActivity(Activity):
    """
    Represents a structured activity that waits for one out of several possible events to occur.
    Calculus notation: A ::= pick(OnMessage | OnAlarm) where OnMessage is a list of message-based branches and
    OnAlarm is a list of time-based branches.
    """
    id: str = Field(..., description="Unique identifier for the pick activity.")
    on_message: Optional[List[str]] = Field(None, description="List of message-based branches.")
    on_alarm: Optional[List[str]] = Field(None, description="List of time-based branches.")


class IfActivity(Activity):
    """
    Represents a structured activity that executes one set of activities if a condition is true, and another set if false.
    Calculus notation: A ::= if(condition) then {Activities} else {Activities}
    """
    id: str = Field(..., description="Unique identifier for the if activity.")
    condition: str = Field(..., description="Condition to evaluate.")
    activities_true: List[str] = Field(..., description="List of activities to execute if the condition is true.")
    activities_false: List[str] = Field(..., description="List of activities to execute if the condition is false.")


class WhileActivity(Activity):
    """
    Represents a structured activity that repeatedly executes a set of activities while a condition is true.
    Calculus notation: A ::= while(condition) {Activities}
    """
    id: str = Field(..., description="Unique identifier for the while activity.")
    condition: str = Field(..., description="Condition to evaluate for each iteration.")
    activities: List[str] = Field(..., description="List of activities to execute in each iteration.")


class RepeatUntilActivity(Activity):
    """
    Represents a structured activity that repeatedly executes a set of activities until a condition becomes true.
    Calculus notation: A ::= repeat {Activities} until (condition)
    """
    id: str = Field(..., description="Unique identifier for the repeat-until activity.")
    activities: List[str] = Field(..., description="List of activities to execute in each iteration.")
    condition: str = Field(..., description="Condition to evaluate after each iteration.")


class CompensateActivity(Activity):
    """
    Represents an activity that triggers compensation logic for previously executed activities within a scope.
    Calculus notation: A ::= compensate
    """
    id: str = Field(..., description="Unique identifier for the compensate activity.")


class ThrowActivity(Activity):
    """
    Represents an activity that explicitly throws a fault, causing the process to terminate with a faulted state.
    Calculus notation: A ::= throw faultName
    """
    id: str = Field(..., description="Unique identifier for the throw activity.")
    fault_name: str = Field(..., description="Name of the fault to throw.")


class TerminateActivity(Activity):
    """
    Represents an activity that abruptly terminates the process instance.
    Calculus notation: A ::= terminate
    """
    id: str = Field(..., description="Unique identifier for the terminate activity.")


class ValidateActivity(Activity):
    """
    Represents an activity that performs validation on a specified variable or data.
    Calculus notation: A ::= validate(variable)
    """
    id: str = Field(..., description="Unique identifier for the validate activity.")
    variable: str = Field(..., description="Variable or data to be validated.")


class RethrowActivity(Activity):
    """
    Represents an activity that rethrows a caught fault, propagating it to the parent scope for handling.
    Calculus notation: A ::= rethrow
    """
    id: str = Field(..., description="Unique identifier for the rethrow activity.")


class CompensateScopeActivity(Activity):
    """
    Represents an activity that triggers compensation logic for the entire scope in which it is defined.
    Calculus notation: A ::= compensateScope
    """
    id: str = Field(..., description="Unique identifier for the compensateScope activity.")


class EmptyActivity(Activity):
    """
    Represents an empty activity, which has no effect on the process execution.
    Calculus notation: A ::= empty
    """
    id: str = Field(..., description="Unique identifier for the empty activity.")


class ScopeActivity(Activity):
    """
    Represents a scoped group of activities with its own local context, including variables, fault handlers, and more.
    Calculus notation: A ::= scope {Activities, Variables, FaultHandlers, CompensationHandlers, EventHandlers}
    """
    id: str = Field(..., description="Unique identifier for the scope activity.")
    activities: List[str] = Field(..., description="List of activity identifiers contained within the scope.")
    variables: List[str] = Field([], description="List of local variable identifiers declared in the scope.")
    fault_handlers: List[str] = Field([], description="List of fault handler identifiers associated with the scope.")
    compensation_handlers: List[str] = Field([], description="List of compensation handler identifiers for the scope.")
    event_handlers: List[str] = Field([], description="List of event handler identifiers for the scope.")


class ForLoopActivity(Activity):
    """
    Represents a loop activity with a defined start, end, and increment, iterating over a block of activities.
    Note: This is an extension for convenience and not part of the standard BPEL model.
    """
    id: str = Field(..., description="Unique identifier for the for loop activity.")
    start_expression: str = Field(..., description="Expression defining the loop's start value.")
    end_expression: str = Field(..., description="Expression defining the loop's end value.")
    increment_expression: str = Field(..., description="Expression defining the loop's increment.")
    activities: List[str] = Field(...,
                                  description="List of activity identifiers to be executed in each loop iteration.")
