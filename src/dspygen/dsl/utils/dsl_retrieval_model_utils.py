import dspy

from dspygen.dsl.dsl_pydantic_models import PipelineStepModel, PipelineDSLModel


def _get_retrieval_model_instance(pipeline: PipelineDSLModel, step: PipelineStepModel):
    """
    Get the retrieval model instance for a given step from the top level definition.
    """
    rm_label = step.rm_model
    # Find the rm class within the dspy module. Need to import the class dynamically from the dspy module
    rm_config = next((m for m in pipeline.rm_models if m.label == rm_label), None)

    if rm_config and hasattr(dspy, rm_config.name):
        rm_class = getattr(dspy, rm_config.name)
        rm_inst = rm_class(**rm_config.args)
        return rm_inst
