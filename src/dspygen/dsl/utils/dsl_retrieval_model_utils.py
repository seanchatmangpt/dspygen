import dspy

from dspygen.dsl.dsl_pydantic_models import StepDSLModel, PipelineDSLModel
from dspygen.rm.data_retriever import DataRetriever


def _get_retrieval_model_instance(pipeline: PipelineDSLModel, step: StepDSLModel):
    """
    Get the retrieval model instance for a given step from the top level definition.
    """
    if not step.rm_model:
        return None

    rm_label = step.rm_model

    # Find the rm class within the dspy module. Need to import the class dynamically from the dspy module
    rm_config = next((m for m in pipeline.rm_models if m.label == rm_label), None)

    if rm_config.name == "DataRetriever":
        return DataRetriever(**rm_config.args)

    if rm_config and hasattr(dspy, rm_config.name):
        rm_class = getattr(dspy, rm_config.name)
        rm_inst = rm_class(**rm_config.args)
        return rm_inst
