from confz import BaseConfig, FileSource
from typing import Dict
from pydantic import BaseModel, Field
import dspy

from dspygen.utils.dspy_tools import init_ol


# Configuration Classes
class AdConfig(BaseConfig):
    adClient: str
    adSlot: str


class DomainConfig(BaseConfig):
    name: str
    description: str
    ads: AdConfig


class RenderConfig(BaseConfig):
    domains: Dict[str, DomainConfig]

    CONFIG_SOURCES = FileSource(file='domains.yaml')


# Input and Output Models for DSPy
class AdInput(BaseModel):
    domain_name: str = Field(description="The name of the domain")
    domain_description: str = Field(description="A brief description of the domain")


class AdOutput(BaseModel):
    ad_copy: str = Field(description="Generated blog article copy")
    # click_probability: float = Field(ge=0, le=1, description="Estimated probability of ad clicks")


class AdSignature(dspy.Signature):
    input: AdInput = dspy.InputField()
    output: AdOutput = dspy.OutputField()


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Create Typed Predictor
    ad_predictor = dspy.TypedPredictor(AdSignature)

    # Load Configuration
    config = RenderConfig()

    # Generate and Optimize Ad Content
    for domain_key, domain_data in config.domains.items():
        ad_input = AdInput(
            domain_name=domain_data.name,
            domain_description=domain_data.description,
            ad_client=domain_data.ads.adClient,
            ad_slot=domain_data.ads.adSlot
        )

        prediction = ad_predictor(input=ad_input)
        ad_copy = prediction.output.ad_copy
        # click_probability = prediction.output.click_probability

        print(f"Domain: {domain_data.name}")
        print(f"Generated Ad: {ad_copy}")
        # print(f"Click Probability: {click_probability:.2f}")

    # # Optimizing Typed Predictors
    # from dspy.evaluate import Evaluate
    # from dspy.evaluate.metrics import click_through_rate
    # from dspy.teleprompt.signature_opt_typed import optimize_signature
    #
    # # Assuming 'devset' contains the development set data for evaluation
    # evaluator = Evaluate(devset=config.domains, metric=click_through_rate, num_threads=10, display_progress=True)
    #
    # result = optimize_signature(
    #     student=dspy.TypedPredictor(AdSignature),
    #     evaluator=evaluator,
    #     initial_prompts=6,
    #     n_iterations=100,
    #     max_examples=30,
    #     verbose=True,
    #     prompt_model=dspy.OpenAI(model='gpt-4', max_tokens=4000),
    # )


if __name__ == '__main__':
    main()
