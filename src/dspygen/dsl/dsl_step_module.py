# Import necessary modules and classes
import dspy

from dspygen.dsl.dsl_pydantic_models import StepDSLModel, PipelineDSLModel, LanguageModelConfig
from dspygen.dsl.utils.dsl_language_model_utils import _get_language_model_instance
from dspygen.dsl.utils.dsl_lm_module_utils import _get_lm_module_instance
from dspygen.dsl.utils.dsl_retrieval_model_utils import _get_retrieval_model_instance
from dspygen.dsl.utils.dsl_rm_module_utils import _get_rm_module_instance
from dspygen.typetemp.functional import render
from munch import Munch
from dspygen.dsl.dsl_pydantic_models import PipelineDSLModel, StepDSLModel


class DSLStepModule:
    """
    A module to execute a single step in a DSPyGen pipeline.
    """
    def __init__(self, pipeline: PipelineDSLModel, step: StepDSLModel):
        self.pipeline = pipeline
        self.step = step

    def execute(self):
        """
        Executes the configured step, including rendering arguments,
        loading and executing the module, and updating the pipeline context.
        """
        lm_default = next((m for m in self.pipeline.lm_models if m.label == "default"), None)

        if not lm_default:
            self.pipeline.lm_models.append(LanguageModelConfig(label="default", name="OpenAI", args={}))

        # Render the arguments for the current step using Jinja2
        rendered_args = self._get_rendered_args()

        if self.step.lm_model:
            lm_inst = _get_language_model_instance(self.pipeline, self.step)

            # Instantiate the module, language model, and retrieval model for this step
            module_inst = _get_lm_module_instance(self.pipeline, rendered_args, self.step)

            # Execute the module with the current context
            with dspy.context(lm=lm_inst):
                module_output = module_inst.forward(**rendered_args)

                # Update the pipeline context with the output from this step
                self.pipeline.context[self.step.module] = module_output

        if self.step.rm_model:
            # rm_inst = _get_retrieval_model_instance(self.pipeline, self.step)

            # Instantiate the module, language model, and retrieval model for this step
            module_inst = _get_rm_module_instance(self.pipeline, rendered_args, self.step)

            # Execute the module with the current context
            module_output = module_inst.forward(**self.step.args)

            # Update the pipeline context with the output from this step
            self.pipeline.context[self.step.module] = module_output

        return Munch(self.pipeline.context)

    def _get_rendered_args(self):
        rendered_args = {arg: render(str(value), **self.pipeline.context) for arg, value in self.step.args.items()}
        # Iterate through rendered_args and convert to a python primitive if possible
        for key, value in rendered_args.items():
            try:
                rendered_args[key] = eval(value)
            except:
                pass
        return rendered_args


def execute_step(pipeline, step):
    """
    Revised _execute_step function that utilizes DSLStepModule for step execution.
    """
    # Instantiate the DSLStepModule with the current pipeline and step
    step_module = DSLStepModule(pipeline, step)

    # Execute the step and update the pipeline context with the results
    updated_context = step_module.execute()

    # Update the pipeline's context with the new context returned by the DSLStepModule
    pipeline.context.update(updated_context)
