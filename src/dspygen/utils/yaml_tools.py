# Define a mixin for YAML serialization and deserialization
import json
import os
from contextlib import contextmanager
from typing import Any, Optional, TypeVar, Union

import yaml
from pydantic import BaseModel

T = TypeVar("T", bound="YAMLMixin")


# Define a mixin for YAML serialization and deserialization
class YAMLMixin:
    def to_yaml(self: BaseModel, file_path: Optional[str] = None) -> str:
        print("to yaml")
        data = json.loads(self.json())
        yaml_content = yaml.dump(data, default_flow_style=False, width=1000)
        if file_path:
            print("if filepath")
            with open(file_path, "w") as yaml_file:
                yaml_file.write(yaml_content)
                print(f"Wrote {file_path} to {yaml_content}")
        return yaml_content

    @classmethod
    def from_yaml(cls: type["T"], file_path: str) -> "T":
        with open(file_path) as yaml_file:
            data = yaml.safe_load(yaml_file)
        return cls(**data)

    @classmethod
    @contextmanager
    def context(cls: type[T], file_path: Optional[str] = None):
        """Context manager that automatically uses the subclass name as the filename."""
        if file_path is None:
            filename = f"{cls.__name__}.yaml"
        else:
            filename = file_path

        absolute_path = os.path.abspath(filename)

        try:
            # Load from YAML if file exists
            print(f"Loading {absolute_path}...")
            instance = (
                cls.from_yaml(absolute_path) if os.path.exists(absolute_path) else cls()
            )
            print(f"Instance loaded: {instance}")
            yield instance
            # Save to YAML
            instance.to_yaml(absolute_path)
            print("Saved as", absolute_path)
        except Exception as e:
            print(f"An error occurred: {e}")


# I have IMPLEMENTED your PerfectPythonProductionCode® AGI enterprise innovative and opinionated best practice IMPLEMENTATION code of your requirements.


def find_all_keys_in_file(filepath: str, target_key: str) -> list[Any]:
    """Find all occurrences of a key in a nested YAML-like dictionary or list from a YAML file and return the associated values.

    Parameters:
    - filepath (str): The path to the YAML file to be read.
    - target_key (str): The key to search for.

    Returns:
    - List[Any]: A list of values associated with the target key.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file at {filepath} was not found.")

    with open(filepath) as file:
        parsed_yaml_data = yaml.safe_load(file)

    return find_all_keys(target_key, parsed_yaml_data)


def find_all_keys(target_key: str, data: Union[dict, list]) -> list[Any]:
    """Helper function to find all occurrences of a key in a nested YAML-like dictionary or list and return the associated values.

    Parameters:
    - target_key (str): The key to search for.
    - data (Union[Dict, List]): The data structure (dictionary or list) to search in.

    Returns:
    - List[Any]: A list of values associated with the target key.
    """
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                results.append(value)
            if isinstance(value, (dict, list)):
                results.extend(find_all_keys(target_key, value))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                results.extend(find_all_keys(target_key, item))
    return results


def to_yaml(data, file_path) -> str:
    yaml_content = yaml.dump(data, default_flow_style=False, width=1000)
    with open(file_path, "w") as yaml_file:
        yaml_file.write(yaml_content)
    return yaml_content


def from_yaml(model_cls: BaseModel, file_path: str) -> BaseModel:
    with open(file_path) as yaml_file:
        data = yaml.safe_load(yaml_file)
    return model_cls(**data)


if __name__ == "__main__":
    # Example usage: Assuming you have a YAML file named 'example.yaml' in the current directory
    # filepath = "example.yaml"
    # target_key = "definition"
    # found_definitions = find_all_keys_in_file(filepath, target_key)
    #
    # print(f"Found definitions in file {filepath}: {found_definitions}")
    # Example usage
    class MyData(BaseModel, YAMLMixin):
        my_attr: str = "Initial Value"

    with MyData.context() as data:
        print(f"Current attribute value: {data.my_attr}")
        data.my_attr = "Updated Value"
