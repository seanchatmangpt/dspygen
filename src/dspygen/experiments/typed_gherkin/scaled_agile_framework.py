from dspygen.utils.dspy_tools import init_dspy
from dspygen.lm.cerebras_lm import Cerebras
import dspy
from pydantic import BaseModel, Field
from typing import List, Optional, Type, Any

class Capability(BaseModel):
    """
    Represents a capability in the SAFe framework.

    FAANG Enterprise Architect Quality: Ensure capabilities are aligned with strategic themes and provide measurable business value.
    Length Restriction: Keep capability descriptions concise, typically 2-3 sentences.
    """
    name: str = Field(description="Name of the capability")
    description: str = Field(description="Description of the capability")

class Feature(BaseModel):
    """
    Represents a feature in the SAFe framework.

    FAANG Enterprise Architect Quality: Features should be specific, measurable, and tied to business outcomes.
    Length Restriction: Feature descriptions should be 1-2 sentences, with 3-5 acceptance criteria.
    """
    name: str = Field(description="Name of the feature")
    description: str = Field(description="Description of the feature")
    acceptance_criteria: List[str] = Field(description="Acceptance criteria for the feature min_length=3")
    story_points: int = Field(description="Estimated story points for the feature")

class Epic(BaseModel):
    """
    Represents an epic in the SAFe framework.

    FAANG Enterprise Architect Quality: Epics should represent significant initiatives that deliver substantial business value.
    Length Restriction: Epic descriptions should be 3-5 sentences, containing 3-7 features.
    """
    name: str = Field(description="Name of the epic")
    description: str = Field(description="Description of the epic")
    features: List[Feature] = Field(description="List of features in the epic min_length=3")

class ProgramIncrement(BaseModel):
    """
    Represents a program increment in the SAFe framework.

    FAANG Enterprise Architect Quality: Program Increments should have clear, measurable objectives aligned with strategic goals.
    Length Restriction: PI objectives should be 3-5 bullet points, containing 3-5 epics.
    """
    name: str = Field(description="Name of the program increment")
    objectives: List[str] = Field(description="Objectives for the program increment", min_length=3)
    epics: List[Epic] = Field(description="List of epics in the program increment", min_length=3)

class ValueStream(BaseModel):
    """
    Represents a value stream in the SAFe framework.

    FAANG Enterprise Architect Quality: Value Streams should represent end-to-end flow of value to customers, with clear capabilities and measurable outcomes.
    Length Restriction: Value Stream descriptions should be 3-5 sentences, containing 3-5 capabilities and 3-5 program increments.
    """
    name: str = Field(description="Name of the value stream")
    description: str = Field(description="Description of the value stream")
    capabilities: List[Capability] = Field(description="List of capabilities in the value stream")
    program_increments: List[ProgramIncrement] = Field(description="List of program increments in the value stream", min_length=3)

class SAFePortfolio(BaseModel):
    """
    Represents a SAFe portfolio.

    FAANG Enterprise Architect Quality: The portfolio should align with enterprise strategy, balancing short-term opportunities with long-term architectural initiatives.
    Length Restriction: Portfolio description should be 5-7 sentences, containing 3-5 value streams.
    """
    name: str = Field(description="Name of the SAFe portfolio")
    description: str = Field(description="Description of the SAFe portfolio")
    value_streams: List[ValueStream] = Field(description="List of value streams in the portfolio", min_length=3)


def generate_safe_portfolio(business_objective: str) -> SAFePortfolio:
    init_dspy(max_tokens=8000, temperature=0.0)


def main():
    business_objective = "Develop a cloud-native, AI-powered e-commerce platform that revolutionizes online shopping experience"
    safe_portfolio = generate_safe_portfolio(business_objective)

    print(f"SAFe Portfolio: {safe_portfolio.name}")
    print(f"Description: {safe_portfolio.description}")
    print("\nValue Streams:")
    for vs in safe_portfolio.value_streams:
        print(f"- {vs.name}")
        print(f"  Description: {vs.description}")
        print("  Capabilities:")
        for cap in vs.capabilities:
            print(f"  - {cap.name}")
        print("  Program Increments:")
        for pi in vs.program_increments:
            print(f"  - {pi.name}")
            print("    Epics:")
            for epic in pi.epics:
                print(f"    - {epic.name}")

    with open("safe_portfolio.json", "w") as f:
        f.write(safe_portfolio.model_dump_json(indent=2))


if __name__ == '__main__':
    main()