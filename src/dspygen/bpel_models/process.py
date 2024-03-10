"""
process.py

This module defines Pydantic models for the WS-BPEL 2.0 process definition. The process model is the top-level element in a BPEL document, defining the executable business process's flow, interactions, and behavior.

The models defined in this module include:
- BPELProcess: Represents the entire BPEL process, including its activities, partner links, variables, fault handlers, and more.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

from .activities import Activity
from .correlations import CorrelationSet
from .partner_links import PartnerLink
from .fault_handlers import Catch, CatchAll
from .links import Link
from .variables import Variable


class BPELProcess(BaseModel):
    """
    Represents the entire BPEL process, including its activities, partner links, variables, fault handlers, and more.
    Calculus notation: P ::= process {Activities, PartnerLinks, Variables, FaultHandlers, Links} encapsulating the elements of a BPEL process.
    """
    id: str = Field(..., description="Unique identifier for the BPEL process.")
    name: Optional[str] = Field(None, description="Name of the BPEL process.")
    activities: List[Activity] = Field(..., description="List of activities defined within the process.")
    partner_links: List[PartnerLink] = Field(..., description="List of partner links used within the process.")
    variables: List[Variable] = Field(..., description="List of variables available within the process.")
    fault_handlers: List[Catch] = Field([], description="List of fault handlers (Catch blocks) defined within the process.")
    catch_all: Optional[CatchAll] = Field(None, description="Optional generic fault handler (CatchAll) for the process.")
    links: List[Link] = Field([], description="List of links defining execution dependencies between activities within the process.")
    correlation_sets: List[CorrelationSet] = Field([], description="List of correlation sets used within the process.")
    completion_condition: Optional[str] = Field(None, description="Condition that determines when the process is considered complete.")
