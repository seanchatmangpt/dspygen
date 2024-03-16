from dspygen.utils.yaml_tools import YAMLMixin
from pydantic import BaseModel, Extra
from typing import List, Dict, Optional, Union


class InputFieldModel(BaseModel):
    name: str
    desc: Optional[str] = None


class OutputFieldModel(BaseModel):
    name: str
    prefix: Optional[str] = ""
    desc: Optional[str] = ""


class SignatureDSLModel(BaseModel):
    name: str
    docstring: Optional[str] = None
    inputs: List[InputFieldModel] = []
    outputs: List[OutputFieldModel] = []


class ArgumentModel(BaseModel):
    name: str
    value: Union[str, Dict[str, str]] = ""  # Allow for both direct values and references


class ModuleDSLModel(BaseModel):
    name: str = ""
    signature: str = ""
    assertions: List[str] = []
    suggestions: List[str] = []
    predictor: Optional[str] = "Predict"
    args: List[ArgumentModel] = []


class PipelineStepModel(BaseModel):
    module: str
    assertions: List[str] = []
    suggestions: List[str] = []
    signature: str = ""
    model: str = "default"
    args: dict = {}  # Support nested argument structures


class LanguageModelConfig(BaseModel):
    label: str
    name: str
    args: dict = {}


class AssertionModel(BaseModel):
    label: str
    logic: str
    message: str


class SuggestionModel(BaseModel):
    label: str
    assertion: str
    message: str


class PipelineConfigModel(BaseModel):
    global_signatures: Dict[str, SignatureDSLModel] = []
    current_step: PipelineStepModel = None

    class Config:
        extra = Extra.allow


class PipelineDSLModel(BaseModel, YAMLMixin):
    assertions: List[AssertionModel] = []
    suggestions: List[SuggestionModel] = []
    models: List[LanguageModelConfig] = []
    signatures: List[SignatureDSLModel] = []
    modules: List[ModuleDSLModel] = []
    steps: List[PipelineStepModel] = []
    context: dict = {}
    config: PipelineConfigModel = PipelineConfigModel()

