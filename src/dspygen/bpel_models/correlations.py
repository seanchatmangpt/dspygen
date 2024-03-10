"""
correlations.py

This module defines Pydantic models for WS-BPEL 2.0 correlation sets and correlation properties. Correlations are crucial for managing
the association of messages to the correct process instances in BPEL processes, particularly in scenarios involving asynchronous message exchanges.

Included models:
- CorrelationProperty: Represents a single property used to correlate messages with process instances.
- CorrelationSet: Represents a set of correlation properties that together define the criteria for correlating messages with process instances.
- CorrelationKey: Represents a combination of values for correlation properties, used to uniquely identify a process instance.
- Subscription: Represents a subscription to a specific correlation set, defining the criteria for receiving messages.
- Initiate: Represents an initiation of a correlation set with a specific correlation key, typically used to start a new process instance.


Correlations ensure that inbound and outbound messages are correctly associated with the process instances that should handle them, based on the values of specified properties.
"""

from pydantic import BaseModel, Field
from typing import List, Dict


class CorrelationProperty(BaseModel):
    """
    Represents a single property used to correlate messages with process instances.
    Calculus notation: CP ::= correlationProperty(name, type) where name is the identifier of the property and type denotes the data type of the property.
    """
    name: str = Field(..., description="The name of the correlation property.")
    type: str = Field(..., description="The data type of the correlation property.")


class CorrelationSet(BaseModel):
    """
    Represents a set of correlation properties that together define the criteria for correlating messages with process instances.
    Calculus notation: CS ::= correlationSet(properties) where properties is a dictionary mapping property names to values for correlation.
    Each set defines how messages are correlated to a particular process instance based on the values of the properties contained within the set.
    """
    id: str = Field(..., description="Unique identifier for the correlation set.")
    properties: Dict[str, CorrelationProperty] = Field(...,
                                                       description="A dictionary of correlation properties that form this set.")


class CorrelationKey(BaseModel):
    """
    Represents a combination of values for correlation properties, used to uniquely identify a process instance.
    Calculus notation: CK ::= correlationKey(propertyValues) where propertyValues is a dictionary mapping property names to their values.
    """
    id: str = Field(..., description="Unique identifier for the correlation key.")
    property_values: Dict[str, str] = Field(..., description="A dictionary mapping property names to their values.")


class Subscription(BaseModel):
    """
    Represents a subscription to a specific correlation set, defining the criteria for receiving messages.
    Calculus notation: S ::= subscription(correlationSetName, correlationKey) where correlationSetName is the name of the correlation set being subscribed to,
    and correlationKey is the value used to filter incoming messages based on correlation properties.
    """
    id: str = Field(..., description="Unique identifier for the subscription.")
    correlation_set_name: str = Field(..., description="Name of the correlation set being subscribed to.")
    correlation_key: CorrelationKey = Field(..., description="Value used to filter incoming messages.")


class Initiate(BaseModel):
    """
    Represents an initiation of a correlation set with a specific correlation key, typically used to start a new process instance.
    Calculus notation: I ::= initiate(correlationSetName, correlationKey) where correlationSetName is the name of the correlation set being initiated,
    and correlationKey is the value used to initialize the correlation properties.
    """
    id: str = Field(..., description="Unique identifier for the initiate action.")
    correlation_set_name: str = Field(..., description="Name of the correlation set being initiated.")
    correlation_key: CorrelationKey = Field(..., description="Value used to initialize the correlation properties.")
