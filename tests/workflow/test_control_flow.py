from dspygen.experiments.control_flow.dsl_control_flow_models import Workflow, execute_workflow


def test_workflow():
    wf = Workflow.from_yaml("/Users/candacechatman/dev/dspygen/src/dspygen/experiments/control_flow/control_flow_workflow.yaml")
    execute_workflow(wf)
    # wf.to_yaml("control_flow_workflow_output_new.yaml")