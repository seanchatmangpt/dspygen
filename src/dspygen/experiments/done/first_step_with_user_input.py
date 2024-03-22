from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.dsl.dsl_pydantic_models import *


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    signature = GenSignatureModel.to_inst("Product Requirements Document for Websites")

    signature.inputs = [signature.inputs[0]]

    module = GenLMModuleModel.to_inst(f"{signature}")
    module.signature = signature.name

    arg_dict = {signature.inputs[0].name: "{{ user_input }}"}

    step = StepDSLModel(module=module.name, signature=signature.name, args=arg_dict)

    pipeline = PipelineDSLModel(signatures=[signature], modules=[module], steps=[step])

    pipeline.to_yaml(f"{signature.name}_pipeline.yaml")

    context = execute_pipeline(f"{signature.name}_pipeline.yaml",
                               {"user_input": "A full stack nextjs DSL pipeline nocode generator"})

    print(context)


if __name__ == '__main__':
    main()
