from pathlib import Path

import yaml
from dspy.signatures.field import InputField, OutputField
from dspy import Signature
import os


def create_signature_class_from_yaml(signature_yaml_filepath_or_str: Path | str) -> type:
    """Create a DSPy Signature class from a YAML file."""

    # Load YAML content
    if not os.path.exists(signature_yaml_filepath_or_str):
        yaml_content = yaml.safe_load(signature_yaml_filepath_or_str)
    else:
        with open(signature_yaml_filepath_or_str, 'r') as file:
            yaml_content = yaml.safe_load(file)

    # Prepare class creation parameters
    class_name = yaml_content.get("class_name", "DynamicSignature")
    docstring = yaml_content.get("docstring", "")
    inputs = yaml_content.get("inputs", [])
    outputs = yaml_content.get("outputs", [])

    class_dict = {"__doc__": docstring, "__annotations__": {}}

    # Process input fields
    for input_field in inputs:
        name = input_field['name']
        desc = input_field.get('desc', '')
        # InputField doesn't usually use a prefix, so it's omitted here
        field_instance = InputField(desc=desc)
        class_dict[name] = field_instance
        class_dict["__annotations__"][name] = InputField

    # Process output fields
    for output_field in outputs:
        name = output_field['name']
        desc = output_field.get('desc', '')
        prefix = output_field.get('prefix', '')
        # OutputField here includes the prefix if provided
        field_instance = OutputField(prefix=prefix, desc=desc)
        class_dict[name] = field_instance
        class_dict["__annotations__"][name] = OutputField

    # Dynamically create the Signature class
    signature_class = type(class_name, (Signature,), class_dict)
    return signature_class

def main():
    signature_yaml = Path('signature.yaml')
    signature_class = create_signature_class_from_yaml(signature_yaml)
    print(signature_class)


if __name__ == '__main__':
    main()
