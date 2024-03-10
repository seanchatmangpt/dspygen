"""
partner_links.py

This module defines Pydantic models for WS-BPEL 2.0 partner links. Partner links specify the concrete participants in the interactions
that a BPEL process defines. They establish the relationship between the process and the external services it interacts with, indicating
the roles played by each in the service interaction.

Included model:
- PartnerLink: Represents a partner link in a BPEL process, specifying the interaction between the process and a partner Web service.

"""
from typing import Optional

from pydantic import BaseModel, Field

class PartnerLink(BaseModel):
    """
    Represents a partner link in a BPEL process, specifying the interaction between the process and a partner Web service.
    Calculus notation: L ::= partnerLink(name, partnerLinkType, myRole?, partnerRole?) where name identifies the partner link,
    partnerLinkType specifies the WSDL port type used, myRole is the role played by the process, and partnerRole is the role played
    by the partner service.
    """
    id: str = Field(..., description="Unique identifier for the partner link.")
    name: str = Field(..., description="Name of the partner link.")
    partner_link_type: str = Field(..., description="Type of the partner link, referring to a WSDL port type.")
    my_role: Optional[str] = Field(None, description="Role played by the process in the service interaction.")
    partner_role: Optional[str] = Field(None, description="Role played by the partner service in the service interaction.")

# Note: Partner link types and roles are typically defined in the WSDL that describes the Web service interface. The 'partner_link_type'
# refers to the WSDL element that defines the set of operations (the portType in WSDL 1.1 or the interface in WSDL 2.0) that can be
# used in the interaction. 'my_role' and 'partner_role' correspond to the roles defined in the WSDL for the two parties in the communication.
