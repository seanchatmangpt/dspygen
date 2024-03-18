from typing import Optional


from pydantic import BaseModel, Field

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



class ArgumentModel(BaseModel):
    name: str
    value: str | dict = ""  # Allow for both direct values and references


# Define ModuleDSLModel for capturing module details
class ModuleDSLModel(BaseModel):
    name: str = Field(..., description="Name of the module. Used for referencing within the pipeline.")
    signature: str = Field(..., description="Name of the signature associated with this module.")
    predictor: Optional[str] = Field("Predict", description="Type of predictor to be used with this module.")
    args: list[ArgumentModel] = Field(default=[],
                                      description="List of arguments to be passed to the module during its execution.")


# Define PipelineStepModel for pipeline steps
class PipelineStepModel(BaseModel):
    module: str = Field(..., description="Name of the module to be executed in this step of the pipeline.")
    signature: str = Field(default="",
                           description="Signature associated with this step. Optional if defined within the module.")
    lm_model: str = Field(default="default", description="Identifier of the language model to be used in this step.")
    rm_model: str = Field(default="default", description="Identifier of the retrieval model to be used in this step.")
    args: dict = Field(default={}, description="Arguments for the module in this step.")


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
    current_step: Optional[PipelineStepModel] = Field(None,
                                                      description="The current step being executed in the pipeline.")

    class Config:
        extra = "allow"


class PipelineDSLModel(BaseModel, YAMLMixin):
    lm_models: list[LanguageModelConfig] = Field(default=[],
                                                 description="list of language model configurations used in the pipeline.")
    rm_models: list[RetrievalModelConfig] = Field(default=[],
                                                 description="list of retrieval model configurations used in the pipeline.")
    signatures: list[SignatureDSLModel] = Field(default=[],
                                                description="list of signatures defined for use in the pipeline.")
    modules: list[ModuleDSLModel] = Field(default=[],
                                          description="list of modules defined for execution in the pipeline.")
    steps: list[PipelineStepModel] = Field(default=[],
                                           description="Sequential steps to be executed in the pipeline.")
    context: dict = Field(default={},
                          description="A context dictionary for storing global values accessible across the pipeline.")
    config: PipelineConfigModel = Field(default_factory=PipelineConfigModel,
                                        description="Configuration settings for the pipeline execution.")
