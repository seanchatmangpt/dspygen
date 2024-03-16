import importlib

import dspy

from dspygen.dsl.dsl_pydantic_models import SignatureDSLModel


def _process_module_signatures(global_signatures, module_def, step):
    """
    Process the signatures for a module definition and a step. Load the signature class if not already loaded.
    """
    # Check if the signature class is already loaded, if not try to load the module
    # Assuming `pipeline.signatures` contains fully qualified names or similar identifiers:
    if module_def and module_def.signature != "" and module_def.signature not in global_signatures:
        signature_class = _load_signature_class(module_def.signature)
        global_signatures[module_def.signature] = signature_class

    if step.signature != "" and step.signature not in global_signatures:
        signature_class = _load_signature_class(step.signature)
        global_signatures[module_def.signature] = signature_class


def _create_signature_from_model(signature_model: SignatureDSLModel) -> type:
    """
    Create a DSPy Signature class from a SignatureDSLModel instance.
    """
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


def _load_signature_class(signature_class_name: str):
    """
    Dynamically loads a signature class by its fully qualified name.
    """
    module_name, class_name = signature_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
