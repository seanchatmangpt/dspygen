import os
from fastapi import APIRouter, HTTPException

import tempfile
from typing import Optional

import dspy
from pydantic import BaseModel

from dspygen.dsl.utils.dsl_language_model_utils import _get_language_model_instance
from dspygen.dsl.dsl_pydantic_models import PipelineDSLModel, LanguageModelConfig
from dspygen.dsl.utils.dsl_module_utils import _get_module_instance
from dspygen.dsl.utils.dsl_retrieval_model_utils import _get_retrieval_model_instance
from dspygen.dsl.utils.dsl_signature_utils import _create_signature_from_model
from dspygen.typetemp.functional import render
from dspygen.utils.file_tools import dsl_dir


def execute_pipeline(file_path, initial_context=None):
    """
    Execute a pipeline from a YAML file and return the context.
    """
    pipeline = _get_pipeline(file_path)

    if initial_context:
        pipeline.context.update(initial_context)

    for step in pipeline.steps:
        _execute_step(pipeline, step)

    return pipeline.context


def _get_pipeline(file_path):
    """
    Load a PipelineDSLModel instance from a YAML file. Also, create the global signatures from the YAML.
    """
    pipeline = PipelineDSLModel.from_yaml(file_path)
    # Gather the signatures from the YAML
    pipeline.config.global_signatures = {signature.name: _create_signature_from_model(signature)
                                              for signature in pipeline.signatures}
    return pipeline


def _execute_step(pipeline, step):
    """
    Execute a step in a pipeline. Creates the LM, renders the args using Jinja2,
    runs the module, and updates the context.
    """
    if not pipeline.lm_models:
        pipeline.lm_models = [LanguageModelConfig(label="default", name="OpenAI", args={})]

    rendered_args = {arg: render(str(value), **pipeline.context) for arg, value in step.args.items()}

    module_inst = _get_module_instance(pipeline, rendered_args, step)

    lm_inst = _get_language_model_instance(pipeline, step)

    rm_inst = _get_retrieval_model_instance(pipeline, step)

    with dspy.context(lm=lm_inst, rm=rm_inst):
        module_output = module_inst.forward(**rendered_args)

    pipeline.context[step.module] = module_output


router = APIRouter()


class PipelineRequest(BaseModel):
    yaml_content: str
    initial_context: Optional[dict] = None


@router.post("/execute_pipeline/")
async def run_pipeline(request: PipelineRequest):
    try:
        # Create a temporary file to hold the YAML content
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.yaml') as tmp:
            tmp.write(request.yaml_content)
            tmp_path = tmp.name

        context = execute_pipeline(tmp_path, request.initial_context)

        # Optionally, clean up the temporary file after execution
        os.remove(tmp_path)

        return context
    except Exception as e:
        # Ensure the temporary file is removed even if an error occurs
        if 'tmp_path' in locals():
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))


def main():
    context = execute_pipeline('/Users/candacechatman/dev/dspygen/src/dspygen/dsl/examples/example_pipeline.yaml')
    # context = execute_pipeline(str(dsl_dir('examples/text_signature_pipeline.yaml')),
    #                            {"raw_data": "id,name,job\n1,Joe,Coder"})


    print(context)


if __name__ == '__main__':
    main()
