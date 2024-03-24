import os
import tempfile
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.dialects.mysql import json

from dspygen.workflow.workflow_executor import execute_workflow
from dspygen.workflow.workflow_models import Workflow

router = APIRouter()


class WorkflowRequest(BaseModel):
    yaml_content: str
    init_ctx: Optional[dict] = None


# Route to execute a workflow based on YAML content and an optional initial context.
@router.post("/execute_workflow/")
async def run_workflow(request: WorkflowRequest):
    try:
        # Create a temporary file to store the YAML content for processing.
        with tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix=".yaml") as tmp:
            tmp.write(request.yaml_content)
            tmp_path = tmp.name

        # Load the workflow from the temporary YAML file.
        wf = Workflow.from_yaml(tmp_path)

        # Execute the workflow with the provided initial context.
        context = execute_workflow(wf, request.init_ctx)

        # Clean up the temporary file after execution.
        os.remove(tmp_path)

        # Ensure the context returned is JSON serializable by filtering non-serializable objects.
        serializable_context = {k: v for k, v in context.items() if json_serializable(v)}

        return serializable_context
    except Exception as e:
        if "tmp_path" in locals():
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))


def json_serializable(value):
    """Check if value is JSON serializable."""
    try:
        json.dumps(value)
        return True
    except TypeError:
        return False