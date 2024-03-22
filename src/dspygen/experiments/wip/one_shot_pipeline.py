from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.dsl.dsl_pydantic_models import GenPipelineModel


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy(model="gpt-4", max_tokens=4000)

    pipeline = GenPipelineModel.to_inst("3 step pipeline that creates a newsletter article from a user input. Be extremly verbose. Fill every value with salient details.")

    print(pipeline)

    pipeline.to_yaml(f"{pipeline.signatures[0].name}_pipeline.yaml")

    context = execute_pipeline(f"{pipeline.signatures[0].name}_pipeline.yaml",
                               {"user_input": "A full stack nextjs DSL pipeline nocode generator"})

    print(context)


if __name__ == '__main__':
    main()
