import os
import tempfile

from dspygen.dsl.dsl_pipeline_executor import execute_pipeline
from dspygen.dsl.dsl_pydantic_models import *
from dspygen.utils.file_tools import dsl_dir
from dspygen.utils.pydantic_tools import InstanceMixin
from dspygen.utils.yaml_tools import YAMLMixin


def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    signature = GenSignatureModel.to_inst("SQL Query to Natual Language")
    print(signature)
    signature.to_yaml("sql_to_natural_signature.yaml")


def main2():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    signature = GenSignatureModel.to_inst("SQL Query to Natual Language")

    # signature = GenSignatureModel.from_yaml(str(dsl_dir("signature/.yaml")))

    print(signature)

    # module = GenModuleModel.to_inst(f"name: RawToStructure, raw_to_structure_signature, Predict {signature}")

    module = GenLMModuleModel.from_yaml(str(dsl_dir("modules/raw_to_structure_module.yaml")))

    # print(module)

    step = GenStepModel.to_inst(f"{module} {signature}")

    print(step)

    pipeline = GenPipelineModel(signatures=[signature], modules=[module], steps=[step])

    # Create a temporary file to hold the YAML content
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.yaml') as tmp:
        tmp.write(pipeline.to_yaml())
        # print(f"Temporary file created at {tmp.name} {pipeline.to_yaml()}")
        tmp_path = tmp.name

    context = execute_pipeline(tmp_path, {"raw_data": "guid,title,content\n1,Title 1,Content 1\n2,Title 2,Content 2"})

    # Optionally, clean up the temporary file after execution
    os.remove(tmp_path)

    print(context)


if __name__ == '__main__':
    main()
