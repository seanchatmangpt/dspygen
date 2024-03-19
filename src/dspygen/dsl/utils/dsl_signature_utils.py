import importlib

import dspy

from dspygen.dsl.dsl_pydantic_models import SignatureDSLModel, GenSignatureModel
from dspygen.utils.file_tools import dsl_dir


def get_sig_key(module_def, step):
    sig_key = ""

    if module_def and module_def.signature != "":
        sig_key = module_def.signature

    if step.signature != "":
        sig_key = step.signature

    return sig_key


def _process_module_signatures(global_signatures, module_def, step):
    """
    Process the signatures for a module definition and a step. Load the signature class if not already loaded.
    """
    sig_key = get_sig_key(module_def, step)

    if sig_key in global_signatures:
        return

    sig_cls = _load_signature_class(sig_key)

    global_signatures[sig_key] = sig_cls


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
    if signature_class_name.endswith(".yaml") or signature_class_name.endswith(".yml"):
        if signature_class_name.startswith("/"):
            signature_model = GenSignatureModel.from_yaml(signature_class_name)
        else:
            signature_model = GenSignatureModel.from_yaml(str(dsl_dir(signature_class_name)))
        return _create_signature_from_model(signature_model)
    else:
        module_name, class_name = signature_class_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
