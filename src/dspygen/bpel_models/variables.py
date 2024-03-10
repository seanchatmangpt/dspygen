"""
variables.py

This module defines Pydantic models for WS-BPEL 2.0 variables. Variables in BPEL are used to hold data that activities within a process can produce or consume.
They can store simple data types, complex data structures, or even messages received from or sent to partner links.

The models defined in this module include:
- SimpleVariable: Represents a variable that holds a simple data type value (e.g., string, integer).
- MessageVariable: Represents a variable that holds a message, typically associated with interactions with partner services.
- ComplexVariable: Represents a variable that holds complex data structures, allowing for the representation of structured data within a process.
- XMLSchemaVariable: Represents a variable that holds data conforming to an XML schema definition.
- ArrayVariable: Represents a variable that holds an array or list of values.
- RecordVariable: Represents a variable that holds a record or structured data type.
- ExternalVariable: Represents a variable that is defined externally to the BPEL process, such as in an external system.
- ExpressionVariable: Represents a variable that holds the result of an expression evaluation.

"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Variable(BaseModel):
    """Placeholder for Variables"""


class SimpleVariable(Variable):
    """
    Represents a variable that holds a simple data type value (e.g., string, integer).
    Calculus notation: V ::= simpleVariable(type, initialValue?) where type is the data type of the variable and initialValue is an optional value to initialize the variable.
    """
    id: str = Field(..., description="Unique identifier for the simple variable.")
    data_type: str = Field(..., description="Data type of the variable (e.g., 'string', 'integer').")
    initial_value: Optional[str] = Field(None, description="Initial value of the variable, if any.")


class MessageVariable(Variable):
    """
    Represents a variable that holds a message, typically associated with interactions with partner services.
    Calculus notation: V ::= messageVariable(messageType) where messageType is the type of the message that the variable can hold.
    """
    id: str = Field(..., description="Unique identifier for the message variable.")
    message_type: str = Field(..., description="Type of the message that the variable can hold.")


class ComplexVariable(Variable):
    """
    Represents a variable that holds complex data structures, allowing for the representation of structured data within a process.
    Calculus notation: V ::= complexVariable(type, structure) where type indicates the complex data type and structure defines the data structure held by the variable.
    """
    id: str = Field(..., description="Unique identifier for the complex variable.")
    data_type: str = Field(..., description="Complex data type of the variable.")
    structure: Dict[str, Any] = Field(..., description="Data structure of the variable, represented as a dictionary.")


class XMLSchemaVariable(Variable):
    """
    Represents a variable that holds data conforming to an XML schema definition.
    Calculus notation: V ::= xmlSchemaVariable(schema) where schema is the XML schema definition associated with the variable.
    """
    id: str = Field(..., description="Unique identifier for the XML schema variable.")
    schema: str = Field(..., description="XML schema definition associated with the variable.")


class ArrayVariable(Variable):
    """
    Represents a variable that holds an array or list of values.
    Calculus notation: V ::= arrayVariable(elementType) where elementType is the data type of the elements in the array.
    """
    id: str = Field(..., description="Unique identifier for the array variable.")
    element_type: str = Field(..., description="Data type of the elements in the array.")


class RecordVariable(Variable):
    """
    Represents a variable that holds a record or structured data type.
    Calculus notation: V ::= recordVariable(fields) where fields is a dictionary defining the structure of the record.
    """
    id: str = Field(..., description="Unique identifier for the record variable.")
    fields: Dict[str, str] = Field(...,
                                   description="Dictionary defining the fields and their data types in the record.")


class ExternalVariable(Variable):
    """
    Represents a variable that is defined externally to the BPEL process, such as in an external system.
    Calculus notation: V ::= externalVariable(reference) where reference is the reference to the external variable.
    """
    id: str = Field(..., description="Unique identifier for the external variable.")
    reference: str = Field(..., description="Reference to the external variable.")


class ExpressionVariable(Variable):
    """
    Represents a variable that holds the result of an expression evaluation.
    Calculus notation: V ::= expressionVariable(expression) where expression is the expression that produces the variable value.
    """
    id: str = Field(..., description="Unique identifier for the expression variable.")
    expression: str = Field(..., description="Expression that produces the variable value.")
