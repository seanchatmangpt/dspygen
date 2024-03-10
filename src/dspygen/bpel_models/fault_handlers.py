"""
fault_handlers.py

This module defines Pydantic models for WS-BPEL 2.0 fault handlers. Fault handlers in BPEL are mechanisms for specifying how to respond to various faults or exceptions that may occur during the execution of a process. They provide a way to define fault-specific handling logic to manage errors and maintain the integrity of the process execution.

The models defined in this module include:
- Catch: Represents a catch block designed to handle a specific fault within a BPEL process.
- CatchAll: Represents a generic catch block that handles any fault not explicitly caught by preceding catch blocks.
- CatchVariable: Represents a variable to store the fault data caught by a catch block.
- CatchMessageType: Represents a message type associated with a specific fault, to be caught by a catch block.
- CatchCondition: Represents a condition to be evaluated for catching a specific fault in a catch block.
- CompensationHandler: Represents a compensation handler for a scope or activity, defining logic to compensate for previously completed work.

"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Catch(BaseModel):
    """
    Represents a catch block designed to handle a specific fault within a BPEL process.
    Calculus notation: F ::= catch(faultName, faultVariable?, Activities) where faultName is the name of the fault to catch, faultVariable is an optional variable to store fault data, and Activities is a list of activities to execute in response to the fault.
    """
    id: str = Field(..., description="Unique identifier for the catch block.")
    fault_name: str = Field(..., description="Name of the fault that this catch block is designed to handle.")
    fault_variable: Optional[str] = Field(None, description="Variable to store fault data, if applicable.")
    activities: List[str] = Field(...,
                                  description="List of activity identifiers to be executed as part of fault handling.")


class CatchAll(BaseModel):
    """
    Represents a generic catch block that handles any fault not explicitly caught by preceding catch blocks.
    Calculus notation: F ::= catchAll(Activities) where Activities is a list of activities to execute in response to any uncaught fault.
    """
    id: str = Field(..., description="Unique identifier for the catchAll block.")
    activities: List[str] = Field(...,
                                  description="List of activity identifiers to be executed as part of generic fault handling.")


class CatchVariable(BaseModel):
    """
    Represents a variable to store the fault data caught by a catch block.
    Calculus notation: F ::= catch(faultName, faultVariable?, Activities) where faultVariable is an optional variable to store fault data.
    """
    id: str = Field(..., description="Unique identifier for the catch variable.")
    name: str = Field(..., description="Name of the variable to store fault data.")
    data_type: str = Field(..., description="Data type of the fault data to be stored.")


class CatchMessageType(BaseModel):
    """
    Represents a message type associated with a specific fault, to be caught by a catch block.
    Calculus notation: F ::= catch(faultName, messageType?, Activities) where messageType is an optional message type to match the fault.
    """
    id: str = Field(..., description="Unique identifier for the catch message type.")
    fault_name: str = Field(..., description="Name of the fault that this catch block is designed to handle.")
    message_type: Optional[str] = Field(None, description="Message type associated with the fault, if applicable.")
    activities: List[str] = Field(...,
                                  description="List of activity identifiers to be executed as part of fault handling.")


class CatchCondition(BaseModel):
    """
    Represents a condition to be evaluated for catching a specific fault in a catch block.
    Calculus notation: F ::= catch(faultName, condition?, Activities) where condition is an optional condition to evaluate for catching the fault.
    """
    id: str = Field(..., description="Unique identifier for the catch condition.")
    fault_name: str = Field(..., description="Name of the fault that this catch block is designed to handle.")
    condition: Optional[str] = Field(None, description="Condition to evaluate for catching the fault.")
    activities: List[str] = Field(...,
                                  description="List of activity identifiers to be executed as part of fault handling.")


class CompensationHandler(BaseModel):
    """
    Represents a compensation handler for a scope or activity, defining logic to compensate for previously completed work.
    Calculus notation: F ::= compensateHandler(Activities)
    """
    id: str = Field(..., description="Unique identifier for the compensation handler.")
    activities: List[str] = Field(..., description="List of activity identifiers to be executed as part of compensation.")
