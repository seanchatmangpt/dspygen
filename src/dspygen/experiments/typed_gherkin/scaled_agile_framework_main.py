from typing import List
from pydantic import BaseModel, Field
import dspy

# Define Pydantic models
class Capability(BaseModel):
    name: str = Field(description="Name of the capability")
    description: str = Field(description="Description of the capability")

class Feature(BaseModel):
    name: str = Field(description="Name of the feature")
    description: str = Field(description="Description of the feature")
    acceptance_criteria: List[str] = Field(description="Acceptance criteria for the feature", min_length=3)
    story_points: int = Field(description="Estimated story points for the feature")

class Epic(BaseModel):
    name: str = Field(description="Name of the epic")
    description: str = Field(description="Description of the epic")
    features: List[Feature] = Field(description="List of features in the epic", min_length=3)

class ProgramIncrement(BaseModel):
    name: str = Field(description="Name of the program increment")
    objectives: List[str] = Field(description="Objectives for the program increment", min_length=3)
    epics: List[Epic] = Field(description="List of epics in the program increment", min_length=3)

class ValueStream(BaseModel):
    name: str = Field(description="Name of the value stream")
    description: str = Field(description="Description of the value stream")
    capabilities: List[Capability] = Field(description="List of capabilities in the value stream")
    program_increments: List[ProgramIncrement] = Field(description="List of program increments in the value stream", min_length=3)

class SAFePortfolio(BaseModel):
    name: str = Field(description="Name of the SAFe portfolio")
    description: str = Field(description="Description of the SAFe portfolio")
    value_streams: List[ValueStream] = Field(description="List of value streams in the portfolio", min_length=3)

# Initialize DSPy
lm = dspy.OpenAI(model='gpt-4', max_tokens=8000, temperature=0.0)
dspy.settings.configure(lm=lm)

# Define Signatures and TypedPredictors
class CapabilitySignature(dspy.Signature):
    """Generate a Capability aligned with the given Value Stream.

    FAANG Enterprise Architect Quality: Ensure capabilities are aligned with strategic themes and provide measurable business value.
    Length Restriction: Keep capability descriptions concise, typically 2-3 sentences.
    """

    value_stream_name: str = dspy.InputField(description="Name of the Value Stream")
    capability: Capability = dspy.OutputField(description="Generated Capability")


class FeatureSignature(dspy.Signature):
    """Generate a Feature for the given Epic.

    FAANG Enterprise Architect Quality: Features should be specific, measurable, and tied to business outcomes.
    Length Restriction: Feature descriptions should be 1-2 sentences, with 3-5 acceptance criteria.
    """

    epic_name: str = dspy.InputField(description="Name of the Epic")
    feature: Feature = dspy.OutputField(description="Generated Feature")


class EpicSignature(dspy.Signature):
    """Generate an Epic for the given Program Increment.

    FAANG Enterprise Architect Quality: Epics should represent significant initiatives that deliver substantial business value.
    Length Restriction: Epic descriptions should be 3-5 sentences, containing 3-7 features.
    """

    program_increment_name: str = dspy.InputField(description="Name of the Program Increment")
    epic: Epic = dspy.OutputField(description="Generated Epic")


class ProgramIncrementSignature(dspy.Signature):
    """Generate a Program Increment for the given Value Stream.

    FAANG Enterprise Architect Quality: Program Increments should have clear, measurable objectives aligned with strategic goals.
    Length Restriction: PI objectives should be 3-5 bullet points, containing 3-5 epics.
    """

    value_stream_name: str = dspy.InputField(description="Name of the Value Stream")
    program_increment: ProgramIncrement = dspy.OutputField(description="Generated Program Increment")


class ValueStreamSignature(dspy.Signature):
    """Generate a Value Stream based on the business objective.

    FAANG Enterprise Architect Quality: Value Streams should represent end-to-end flow of value to customers, with clear capabilities and measurable outcomes.
    Length Restriction: Value Stream descriptions should be 3-5 sentences, containing 3-5 capabilities and 3-5 program increments.
    """

    business_objective: str = dspy.InputField(description="Business objective")
    value_stream: ValueStream = dspy.OutputField(description="Generated Value Stream")


class SAFePortfolioSignature(dspy.Signature):
    """Generate a SAFe Portfolio based on the business objective.

    FAANG Enterprise Architect Quality: The portfolio should align with enterprise strategy, balancing short-term opportunities with long-term architectural initiatives.
    Length Restriction: Portfolio description should be 5-7 sentences, containing 3-5 value streams.
    """

    business_objective: str = dspy.InputField(description="Business objective")
    safe_portfolio: SAFePortfolio = dspy.OutputField(description="Generated SAFe Portfolio")
# Implement generator functions: generate_capabilities, generate_features, generate_epics, generate_program_increments, generate_value_streams

# ... [Include the Signature classes and generator functions from the previous steps] ...

def generate_capabilities(value_stream_name: str) -> List[Capability]:
    capabilities = []
    capability_predictor = dspy.TypedPredictor(CapabilitySignature)
    for _ in range(3):
        prediction = capability_predictor(value_stream_name=value_stream_name)
        capabilities.append(prediction.capability)
    return capabilities

def generate_features(epic_name: str) -> List[Feature]:
    features = []
    feature_predictor = dspy.TypedPredictor(FeatureSignature)
    for _ in range(3):
        prediction = feature_predictor(epic_name=epic_name)
        features.append(prediction.feature)
    return features

def generate_epics(program_increment_name: str) -> List[Epic]:
    epics = []
    epic_predictor = dspy.TypedPredictor(EpicSignature)
    for _ in range(3):
        prediction = epic_predictor(program_increment_name=program_increment_name)
        epic = prediction.epic
        epic.features = generate_features(epic.name)
        epics.append(epic)
    return epics

def generate_program_increments(value_stream_name: str) -> List[ProgramIncrement]:
    program_increments = []
    pi_predictor = dspy.TypedPredictor(ProgramIncrementSignature)
    for _ in range(3):
        prediction = pi_predictor(value_stream_name=value_stream_name)
        pi = prediction.program_increment
        pi.epics = generate_epics(pi.name)
        program_increments.append(pi)
    return program_increments

def generate_value_streams(business_objective: str) -> List[ValueStream]:
    value_streams = []
    vs_predictor = dspy.TypedPredictor(ValueStreamSignature)
    for _ in range(3):
        prediction = vs_predictor(business_objective=business_objective)
        vs = prediction.value_stream
        vs.capabilities = generate_capabilities(vs.name)
        vs.program_increments = generate_program_increments(vs.name)
        value_streams.append(vs)
    return value_streams

def generate_safe_portfolio(business_objective: str) -> SAFePortfolio:
    portfolio_predictor = dspy.TypedPredictor(SAFePortfolioSignature)
    prediction = portfolio_predictor(business_objective=business_objective)
    portfolio = prediction.safe_portfolio
    portfolio.value_streams = generate_value_streams(business_objective)
    return portfolio

# Main function
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
            print("    Objectives:")
            for obj in pi.objectives:
                print(f"      - {obj}")
            print("    Epics:")
            for epic in pi.epics:
                print(f"    - {epic.name}")
                print("      Features:")
                for feature in epic.features:
                    print(f"        - {feature.name}")
                    print(f"          Description: {feature.description}")
                    print(f"          Acceptance Criteria: {feature.acceptance_criteria}")
                    print(f"          Story Points: {feature.story_points}")
    # Save to JSON file
    with open("safe_portfolio.json", "w") as f:
        f.write(safe_portfolio.model_dump_json(indent=2))

if __name__ == '__main__':
    main()
