import dspy

from dspygen.dsl.dsl_pydantic_models import PipelineDSLModel


def _get_language_model_instance(pipeline: PipelineDSLModel, step):
    """
    Get the language model instance for a given step from the top level definition.
    """
    lm_label = step.lm_model
    # Find the lm class within the dspy module. Need to import the class dynamically from the dspy module
    lm_config = next((m for m in pipeline.lm_models if m.label == lm_label), None)
    lm_class = getattr(dspy, lm_config.name)
    lm_inst = lm_class(**lm_config.args)
    return lm_inst