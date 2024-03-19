from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.utils.file_tools import dsl_dir


def main():
    context = execute_pipeline(str(dsl_dir('examples/saltcorn_plugin_generator.yaml')),
                               {"user_input": "Saltcorn Sequential Forms"})

    print(context)

    context.to_yaml("saltcorn_plugin_generator_output.yaml")


if __name__ == '__main__':
    main()
