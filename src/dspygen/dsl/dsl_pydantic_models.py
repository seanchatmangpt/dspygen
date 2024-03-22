from typing import Optional

from munch import Munch
from pydantic import BaseModel, Field

from dspygen.utils.pydantic_tools import InstanceMixin
from dspygen.utils.yaml_tools import YAMLMixin


class InputFieldModel(BaseModel):
    """Defines an input field for a DSPy Signature."""
    name: str = Field(
        ...,
        description="The key used to access and pass the input within the Signature.",
    )
    prefix: str = Field(
        "",
        description="Optional additional context or labeling for the input field.",
    )
    desc: str = Field(
        ...,
        description="Description of the input field's purpose or the nature of content it should contain.",
    )


class OutputFieldModel(BaseModel):
    """Defines an output field for a DSPy Signature."""

    name: str = Field(
        ...,
        description="The key used to access and pass the input within the Signature.",
    )
    prefix: str = Field(
        "",
        description="Optional additional context or labeling for the output field.",
    )
    desc: str = Field(
        ...,
        description="Description of the output field's purpose or the nature of content it should contain.",
    )


# Define SignatureDSLModel for capturing signature details
class SignatureDSLModel(BaseModel):
    name: str = Field(..., description="The unique name identifying the Signature.")
    docstring: str = Field(..., description="Documentation of the Signature's purpose.")
    inputs: list[InputFieldModel] = Field(default=[], description="List of input fields required by the Signature.")
    outputs: list[OutputFieldModel] = Field(default=[], description="List of output fields produced by the Signature.")


class LMModuleDSLModel(BaseModel):
    name: str = Field(..., description="Name of the language model module. Used for referencing within the pipeline.")
    signature: str = Field(..., description="Name of the signature associated with this language model module.")
    predictor: Optional[str] = Field("Predict", description="Type of predictor to be used with this module. "
                                                            "Usually 'Predict' or 'ChainOfThought'.")


class RMModuleDSLModel(BaseModel):
    name: str = Field(..., description="Name of the module. Used for referencing within the pipeline.")


# Define PipelineStepModel for pipeline steps
class StepDSLModel(BaseModel):
    module: Optional[str] = Field("dspygen.dsl.dsl_dspy_module.DSLModule",
                                  description="Name of the module to be executed in this step of the pipeline.")
    signature: Optional[str] = Field(default="",
                                     description="Signature associated with this step.")
    lm_model: Optional[str] = Field(default="", description="Identifier of the language model to be used in this step.")
    rm_model: Optional[str] = Field(default="", description="Identifier of the retrieval model to be used in this step.")
    args: Optional[dict] = Field(default={}, description="Arguments for the module in this step.")


class LanguageModelConfig(BaseModel):
    label: str = Field(default="default", description="Used for referencing in the Modules")
    name: str = Field(default="OpenAI", description="The class name of the dspy language model to use")
    args: dict = {}


class RetrievalModelConfig(BaseModel):
    label: str = Field(..., description="Used for referencing in the Modules")
    name: str = Field(..., description="The class name of the dspy retrieval model to use")
    args: dict = {}


class PipelineConfigModel(BaseModel):
    global_signatures: dict = Field(default={},
                                    description="A dictionary of global signatures available in the pipeline.")
    current_step: Optional[StepDSLModel] = Field(None,
                                                 description="The current step being executed in the pipeline.")

    class Config:
        extra = "allow"


class ContextModel(BaseModel, YAMLMixin):
    """A context dictionary for storing global values accessible across the pipeline."""
    class Config:
        extra = "allow"


class PipelineDSLModel(BaseModel, YAMLMixin):
    lm_models: list[LanguageModelConfig] = Field(default=[],
                                                 description="list of language model configurations used in the pipeline.")
    rm_models: list[RetrievalModelConfig] = Field(default=[],
                                                 description="list of retrieval model configurations used in the pipeline.")
    signatures: list[SignatureDSLModel] = Field(default=[],
                                                description="list of signatures defined for use in the pipeline.")
    lm_modules: list[LMModuleDSLModel] = Field(default=[],
                                               description="list of language model modules defined for execution in the pipeline.")
    rm_modules: list[RMModuleDSLModel] = Field(default=[],
                                               description="list of retriever model modules defined for execution in the pipeline.")
    steps: list[StepDSLModel] = Field(default=[],
                                      description="Sequential steps to be executed in the pipeline.")
    context: dict = Field(default=Munch(),
                                  description="A context dictionary for storing global values accessible across the pipeline.")
    config: PipelineConfigModel = Field(default_factory=PipelineConfigModel,
                                        description="Configuration settings for the pipeline execution.")


class GenSignatureModel(SignatureDSLModel, InstanceMixin, YAMLMixin):
    """
    Generate a signature model. Make sure to have at one input and one output field and
    the name is CamelCase and ends with 'Signature'. Include a verbose docstring.
    """


class GenLMModuleModel(LMModuleDSLModel, InstanceMixin, YAMLMixin):
    """Generate a module model. Make sure the name is CamelCase and ends with 'Module'"""


class GenPipelineModel(PipelineDSLModel, InstanceMixin, YAMLMixin):
    """Generate a pipeline model."""


class GenStepModel(StepDSLModel, InstanceMixin, YAMLMixin):
    """Generate a pipeline model."""
