import importlib

import dspy

from dspygen.dsl.dsl_pydantic_models import ModuleDSLModel
from dspygen.dsl.utils.dsl_signature_utils import _process_module_signatures
from dspygen.dsl.dsl_dspy_module import DSLModule


def _create_module_from_model(module_model: ModuleDSLModel, global_signatures) -> dspy.Module:
    """
    Create a DSPy Module from a ModuleDSLModel instance.
    """
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


def _load_dspy_module_class(dspy_module_class_name: str):
    """
    Dynamically loads a signature class by its fully qualified name.
    """
    module_name, class_name = dspy_module_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def _get_module_instance(pipeline, rendered_args, step):
    """
    Get the module instance for a given step from the top level definition or load the module.
    Uses the DSLModule class from dspygen.modules.dsl_module to handle modules defined in the pipeline YAML.
    """
    module_def = next((m for m in pipeline.modules if m.name == step.module), None)

    # If the module definition is not found, then load the module with load_dspy_module_class
    if not module_def:
        module_inst = _load_dspy_module_class(step.module)(
            **rendered_args)  # Resolve Jinja2 templates in arguments against the context
    else:
        _process_module_signatures(pipeline.config.global_signatures, module_def, step)

        # Note: Additional logic may be required to dynamically resolve args from rendered_args
        module_inst = DSLModule(pipeline=pipeline,
                                signature=pipeline.config.global_signatures[module_def.signature],
                                predictor=module_def.predictor,
                                context=pipeline.context,
                                **rendered_args)
    return module_inst

