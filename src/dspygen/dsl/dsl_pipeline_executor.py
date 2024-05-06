import os
from fastapi import APIRouter, HTTPException

import tempfile
from typing import Optional

import dspy
from pydantic import BaseModel

from dspygen.dsl.dsl_step_module import execute_step
from dspygen.dsl.dsl_pydantic_models import PipelineDSLModel, LanguageModelConfig
from dspygen.dsl.utils.dsl_signature_utils import _create_signature_from_model
from munch import Munch


def execute_pipeline(file_path, init_ctx=None):
    """
    Execute a pipeline from a YAML file and return the context.
    """
    pipeline = _get_pipeline(file_path)

    if init_ctx:
        pipeline.context.update(init_ctx)

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
    context = execute_pipeline('/Users/sac/dev/dspygen/src/dspygen/dsl/examples/example_pipeline.yaml')
    # context = execute_pipeline(str(dsl_dir('examples/text_signature_pipeline.yaml')),
    #                            {"raw_data": "id,name,job\n1,Joe,Coder"})
    # context = execute_pipeline(str(dsl_dir('examples/sql_to_nl.yaml')),
    #                            {"query": poor_query})


    print(context)

if __name__ == '__main__':
    main()
