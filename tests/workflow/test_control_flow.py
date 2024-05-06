from dspygen.workflow.workflow_models import Workflow
from dspygen.workflow.workflow_executor import execute_workflow


# def test_workflow():
#     wf = Workflow.from_yaml("/Users/sac/dev/dspygen/src/dspygen/workflow/control_flow_workflow.yaml")
#     context = execute_workflow(wf)
#     print(context)


def test_import_workflow():
    wf = Workflow.from_yaml("/Users/sac/dev/dspygen/src/dspygen/workflow/data_analysis_workflow.yaml")
    context = execute_workflow(wf)
    print(context)
