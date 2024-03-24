import json
import os
import tempfile
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from dspygen.experiments.control_flow.dsl_control_flow_models import execute_workflow, Workflow, serialize_context

router = APIRouter()


class WorkflowRequest(BaseModel):
    yaml_content: str
    init_ctx: Optional[dict] = None


@router.post("/execute_workflow/")
async def run_workflow(request: WorkflowRequest):
    try:
        # Create a temporary file to hold the YAML content
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.yaml') as tmp:
            tmp.write(request.yaml_content)
            tmp_path = tmp.name

        wf = Workflow.from_yaml(tmp_path)

        context = execute_workflow(wf, request.init_ctx)

        # Optionally, clean up the temporary file after execution
        os.remove(tmp_path)

        # Convert the context to a dictionary making sure it is JSON serializable
        # context = {k: v for k, v in context.items() if isinstance(v, (str, int, float, list, dict, bool, type(None)))}

        serializable_context = serialize_context(context)

        del serializable_context["__builtins__"]

        return serializable_context
    except Exception as e:
        # Ensure the temporary file is removed even if an error occurs
        if 'tmp_path' in locals():
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))