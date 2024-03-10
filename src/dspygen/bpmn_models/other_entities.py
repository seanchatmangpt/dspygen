"""
This module defines Pydantic models for other entities commonly used in BPMN (Business Process Model and Notation) diagrams.
These entities include elements such as conversations, choreography tasks, global tasks, and data stores.

The models defined in this module include:
- Conversation: Represents a conversation in BPMN, which is a series of message exchanges between participants.
- ChoreographyTask: Represents a choreography task in BPMN, which is a task performed by multiple participants in a BPMN collaboration.
- GlobalTask: Represents a global task in BPMN, which is a task performed outside the scope of any specific process instance.
- DataStore: Represents a data store in BPMN, which is a repository for storing data used or produced by activities within a process.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class Conversation(BaseModel):
    """
    Represents a conversation in BPMN, which is a series of message exchanges between participants.
    """
    id: str = Field(..., description="Unique identifier for the conversation.")
    name: Optional[str] = Field(None, description="Name of the conversation, if any.")
    participants: List[str] = Field(..., description="List of participants involved in the conversation.")


class ChoreographyTask(BaseModel):
    """
    Represents a choreography task in BPMN, which is a task performed by multiple participants in a BPMN collaboration.
    """
    id: str = Field(..., description="Unique identifier for the choreography task.")
    name: Optional[str] = Field(None, description="Name of the choreography task, if any.")
    initiating_participant_ref: Optional[str] = Field(None,
                                                      description="ID of the participant initiating the choreography task, if any.")
    participants: List[str] = Field(..., description="List of participants involved in the choreography task.")


class GlobalTask(BaseModel):
    """
    Represents a global task in BPMN, which is a task performed outside the scope of any specific process instance.
    """
    id: str = Field(..., description="Unique identifier for the global task.")
    name: Optional[str] = Field(None, description="Name of the global task, if any.")


class DataStore(BaseModel):
    """
    Represents a data store in BPMN, which is a repository for storing data used or produced by activities within a process.
    """
    id: str = Field(..., description="Unique identifier for the data store.")
    name: Optional[str] = Field(None, description="Name of the data store, if any.")
