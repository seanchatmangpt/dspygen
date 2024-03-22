import importlib

import dspy

from dspygen.dsl.dsl_pydantic_models import RMModuleDSLModel
from dspygen.rm.data_retriever import DataRetriever


def _create_rm_module_from_model(module_model: RMModuleDSLModel) -> dspy.Module:
    """
    Create a DSPy Module from a ModuleDSLModel instance.
    """


def _load_rm_module_class(dspy_module_class_name: str):
    """
    Dynamically loads a signature class by its fully qualified name.
    """
    module_name, class_name = dspy_module_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def _get_rm_module_instance(pipeline, rendered_args, step):
    """
    Get the module instance for a given step from the top level definition or load the module.
    Uses the DSLModule class from dspygen.modules.dsl_module to handle modules defined in the pipeline YAML.
    """
    return DataRetriever(**rendered_args, pipeline=pipeline, step=step)


