from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.dsl.dsl_pydantic_models import *


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    module, signature, step = make_step("LinkedIn Newsletter Article Generator", is_first_step=True)

    sig_list = [signature]
    mod_list = [module]
    step_list = [step]

    module, signature, step = make_step(f"Create synthetic critic feedback generator for improvement for {signature.docstring} include critic in the signature name. ", last_sig=signature)

    sig_list.append(signature)
    mod_list.append(module)
    step_list.append(step)

    pipeline = PipelineDSLModel(signatures=sig_list, modules=mod_list, steps=step_list)

    pipeline.to_yaml(f"{signature.name}_pipeline.yaml")

    context = execute_pipeline(f"{signature.name}_pipeline.yaml",
                               {"user_input": "A full stack nextjs DSL pipeline nocode generator"})

    print(context)


def make_step(sig_prompt, last_sig=None, is_first_step=False):
    if last_sig:
        signature = GenSignatureModel.to_inst(f"{sig_prompt}. The inputs should be the outputs {last_sig.outputs}")
    else:
        signature = GenSignatureModel.to_inst(sig_prompt)

    if is_first_step:
        signature.inputs = [signature.inputs[0]]

    module = GenLMModuleModel.to_inst(f"{signature.docstring} convert into a Module. It's name should be similar to {signature.name}")
    module.signature = signature.name

    if is_first_step:
        arg_dict = {signature.inputs[0].name: "{{ user_input }}"}
    else:
        value = "{{" + f" {last_sig.outputs[0].name} " + "}}"
        arg_dict = {signature.inputs[0].name: value}

    step = StepDSLModel(module=module.name, signature=signature.name, args=arg_dict)

    return module, signature, step


if __name__ == '__main__':
    main()
