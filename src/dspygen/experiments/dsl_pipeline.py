from typing import List, Dict, Optional, Union

import dspy
from pydantic import BaseModel

from dspygen.modules.dsl_module import DSLModule
from dspygen.typetemp.functional import render
from dspygen.utils.yaml_tools import YAMLMixin


class InputFieldModel(BaseModel, YAMLMixin):
    name: str
    desc: Optional[str] = None


class OutputFieldModel(BaseModel, YAMLMixin):
    name: str
    prefix: Optional[str] = ""
    desc: Optional[str] = ""


class SignatureDSLModel(BaseModel, YAMLMixin):
    name: str
    docstring: Optional[str] = None
    inputs: List[InputFieldModel] = []
    outputs: List[OutputFieldModel] = []


class ArgumentModel(BaseModel, YAMLMixin):
    name: str
    value: Union[str, Dict[str, str]]  # Allow for both direct values and references


class ModuleDSLModel(BaseModel, YAMLMixin):
    name: str = ""
    model: str = ""
    signature: str = ""
    predictor: Optional[str] = None
    args: List[ArgumentModel] = []


class PipelineStepModel(BaseModel, YAMLMixin):
    module: str
    args: Dict[str, Union[str, Dict[str, str]]] = {}  # Support nested argument structures


class LanguageModelConfig(BaseModel):
    label: str
    name: str
    args: dict


class PipelineDSLModel(BaseModel, YAMLMixin):
    models: List[LanguageModelConfig] = []
    signatures: List[SignatureDSLModel] = []
    modules: List[ModuleDSLModel] = []
    steps: List[PipelineStepModel] = []


def create_signature_from_model(signature_model: SignatureDSLModel) -> type:
    """Create a DSPy Signature class from a SignatureDSLModel instance."""
    class_dict = {"__doc__": signature_model.docstring, "__annotations__": {}}

    # Process input fields
    for input_field in signature_model.inputs:
        name = input_field.name
        desc = input_field.desc
        field_instance = dspy.InputField(desc=desc)
        class_dict[name] = field_instance
        class_dict["__annotations__"][name] = dspy.InputField

    # Process output fields
    for output_field in signature_model.outputs:
        name = output_field.name
        desc = output_field.desc
        prefix = output_field.prefix
        field_instance = dspy.OutputField(prefix=prefix, desc=desc)
        class_dict[name] = field_instance
        class_dict["__annotations__"][name] = dspy.OutputField

    # Dynamically create the Signature class
    signature_class = type(signature_model.name, (dspy.Signature,), class_dict)
    return signature_class


def create_module_from_model(module_model: ModuleDSLModel, global_signatures) -> dspy.Module:
    """Create a DSPy Module from a ModuleDSLModel instance."""
    signature = global_signatures[module_model.signature]
    predictor = module_model.predictor
    args = module_model.args

    # Prepare forward_args if args are meant for the forward method
    # Assuming args is a list of dictionaries where each dict represents kwargs for a method call
    forward_args = {}
    if isinstance(args, list):
        for arg in args:
            forward_args.update(arg)
    elif isinstance(args, dict):
        forward_args = args
    else:
        raise ValueError("Unsupported argument format in YAML.")

    # Initialize the module with predictor, signature, and forward_args
    module_inst = DSLModule(predictor=predictor, signature=signature, **forward_args)
    return module_inst


def execute_pipeline(file_path):
    pipeline_inst = PipelineDSLModel.from_yaml(file_path)
    global_signatures = {signature.name: create_signature_from_model(signature) for signature in pipeline_inst.signatures}

    context = {}  # Shared context for all steps

    for step in pipeline_inst.steps:
        # Retrieve the module definition based on the step's module name
        module_def = next((m for m in pipeline_inst.modules if m.name == step.module), None)

        if not module_def:
            raise ValueError(f"Module definition for {step.module} not found.")

        # Resolve Jinja2 templates in arguments against the context
        rendered_args = {arg: render(str(value), **context) for arg, value in step.args.items()}

        # Dynamically create a new module instance for this step
        signature = global_signatures[module_def.signature]
        predictor = module_def.predictor

        # Note: Additional logic may be required to dynamically resolve args from rendered_args
        module_inst = DSLModule(signature=signature, predictor=predictor, context=context, **rendered_args)

        # Execute the module, potentially updating the context with its output

        lm_label = module_def.model

        # Find the lm class within the dspy module. Need to import the class dynamically from the dspy module
        lm_config = next((m for m in pipeline_inst.models if m.label == lm_label), None)

        lm_class = getattr(dspy, lm_config.name)
        lm_inst = lm_class(**lm_config.args)

        with dspy.context(lm=lm_inst):
            module_output = module_inst.forward()

        # Optionally, update the context with this module's output if needed
        # This assumes a convention for naming outputs in the context, e.g., using the module's name
        context[step.module] = module_output

    return context


def main():
    context = execute_pipeline('example_pipeline.yaml')
    print(context)


if __name__ == '__main__':
    main()
