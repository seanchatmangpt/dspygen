import os
from fastapi import APIRouter, HTTPException

import tempfile
from typing import Optional

import dspy
from pydantic import BaseModel

from dspygen.llm_pipe.dsl_step_module import execute_step
from dspygen.llm_pipe.dsl_pydantic_models import PipelineDSLModel, LanguageModelConfig
from dspygen.llm_pipe.utils.dsl_signature_utils import _create_signature_from_model
from munch import Munch


from loguru import logger


def execute_pipeline(file_path, init_ctx=None, **kwargs):
    """
    Execute a pipeline from a YAML file and return the context.
    """
    logger.info(f"Executing pipeline from {file_path}")
    logger.info(f"Initial context: {init_ctx}")

    pipeline = _get_pipeline(file_path)

    if init_ctx:
        pipeline.context.update(init_ctx)

    if kwargs:
        pipeline.context.update(kwargs)

    for step in pipeline.steps:
        execute_step(pipeline, step)

    return Munch(pipeline.context)


def _get_pipeline(file_path):
    """
    Load a PipelineDSLModel instance from a YAML file. Also, create the global signatures from the YAML.
    """
    pipeline = PipelineDSLModel.from_yaml(file_path)
    # Gather the signatures from the YAML
    pipeline.config.global_signatures = {signature.name: _create_signature_from_model(signature)
                                              for signature in pipeline.signatures}
    return pipeline


router = APIRouter()


class PipelineRequest(BaseModel):
    yaml_content: str
    init_ctx: Optional[dict] = None


@router.post("/execute_pipeline/")
async def run_pipeline(request: PipelineRequest):
    try:
        # Create a temporary file to hold the YAML content
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.yaml') as tmp:
            tmp.write(request.yaml_content)
            tmp_path = tmp.name

        context = execute_pipeline(tmp_path, request.init_ctx)

        # Optionally, clean up the temporary file after execution
        os.remove(tmp_path)

        # Convert the context to a dictionary making sure it is JSON serializable
        context = {k: v for k, v in context.items() if isinstance(v, (str, int, float, list, dict, bool, type(None)))}

        print(f"Context:\n\n{context}\n\n")

        return context
    except Exception as e:
        # Ensure the temporary file is removed even if an error occurs
        if 'tmp_path' in locals():
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))


def main():
    # context = execute_pipeline('/Users/sac/dev/dspygen/src/dspygen/llm_pipe/examples/example_pipeline.yaml')
    # context = execute_pipeline(str(dsl_dir('examples/text_signature_pipeline.yaml')),
    #                            {"raw_data": "id,name,job\n1,Joe,Coder"})
    from dspygen.utils.file_tools import dsl_dir
    context = execute_pipeline(str(dsl_dir('examples/sql_to_nl.yaml')),
                               {"query": "SELECT * FROM table WHERE id = 1"})


    print(context)

if __name__ == '__main__':
    main()
