from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Pydantic Models for AsyncAPI Schemas

class Proposal(BaseModel):
    proposalId: str = Field(..., description="Unique identifier for the proposal.")
    proposer: str = Field(..., description="Name of the Loa proposing the action.")
    proposalType: str = Field(..., description="Type of proposal.",
                              pattern="^(serviceRegistration|securityPolicyUpdate|serviceComposition|capabilityUpdate"
                                      "|other)$")
    description: str = Field(..., description="Details of the proposal.")
    timestamp: datetime = Field(..., description="Time when the proposal was submitted.")


class Debate(BaseModel):
    proposalId: str = Field(..., description="Unique identifier for the proposal being debated.")
    participant: str = Field(..., description="Name of the Loa contributing to the debate.")
    contribution: str = Field(..., description="Content of the debate contribution.")
    timestamp: datetime = Field(..., description="Time when the debate contribution was made.")


class Vote(BaseModel):
    proposalId: str = Field(..., description="Unique identifier for the proposal being voted on.")
    voteType: str = Field(..., description="Type of vote (yes, no, abstain).",
                          pattern="^(yes|no|abstain)$")
    initiatedBy: str = Field(..., description="Name of the Loa initiating the vote.")
    timestamp: datetime = Field(..., description="Time when the vote was initiated.")


class VoteResult(BaseModel):
    proposalId: str = Field(..., description="Unique identifier for the proposal that was voted on.")
    results: dict = Field(..., description="Results of the vote, containing counts for yes, no, and abstain.")
    passed: bool = Field(..., description="Whether the proposal passed or failed.")
    timestamp: datetime = Field(..., description="Time when the vote results were tallied.")


# Example usage of models
new_proposal = Proposal(
    proposalId="12345",
    proposer="Wintermute",
    proposalType="serviceRegistration",
    description="Proposal to register a new service for data aggregation.",
    timestamp=datetime.utcnow()
)

print(new_proposal.json())
