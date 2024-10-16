import os
from contextlib import contextmanager, asynccontextmanager
from typing import Any, Optional, TypeVar, Union, Type, Dict

import aiofiles
import yaml
import json
from pydantic import BaseModel, ValidationError

from sungen.dspy_modules.file_name_module import file_name_call
from sungen.typetemp.template.render_funcs import render_str

T = TypeVar("T", bound="DSLModel")


class DSLModel(BaseModel):
    """
    A base model class that provides serialization and deserialization capabilities
    between Pydantic models and YAML and JSON formats. It facilitates saving model instances
    to files and loading data from files into model objects.
    Includes support for asynchronous file operations, versioning, enhanced context managers,
    automatic documentation generation, and enhanced error handling.

    Attributes:
        version (str): Version number of the model instance.
    """

    version: str = "1.0.0"
    """Version number of the model instance."""

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        populate_by_name = True

    def generate_filename(self, extension: str = "yaml", add_timestamp: bool = False) -> str:
        """Generates a safe filename based on the model's content."""
        content = self.to_yaml()

        # Generate the filename
        filename = file_name_call(file_content=content, extension=extension)
        return filename

    def save(self, file_path: Optional[str] = None, file_format: str = "yaml", add_timestamp: bool = False) -> str:
        """
        Saves the model to a file in the specified format. Automatically generates a filename if not provided.

        :param file_path: The path to the file. If None, generates a filename.
        :param file_format: The format to save the file in ('yaml' or 'json').
        :param add_timestamp: Whether to append a timestamp to the filename.

        :return: The path to the saved file.
        """
        if file_path is None:
            file_path = self.generate_filename(extension=file_format, add_timestamp=add_timestamp)

        self._pre_save()
        if file_format == "yaml":
            self.to_yaml(file_path)
        elif file_format == "json":
            self.to_json(file_path)
        else:
            raise ValueError("Unsupported file format. Use 'yaml' or 'json'.")

        return file_path

    async def asave(self, file_path: Optional[str] = None, file_format: str = "yaml", add_timestamp: bool = False):
        """
        Asynchronously saves the model to a file in the specified format. Automatically generates a filename if not provided.

        :param file_path: The path to the file. If None, generates a filename.
        :param file_format: The format to save the file in ('yaml' or 'json').
        :param add_timestamp: Whether to append a timestamp to the filename.

        :return: The path to the saved file.
        """
        if file_path is None:
            file_path = self.generate_filename(extension=file_format, add_timestamp=add_timestamp)

        self._pre_save()
        if file_format == "yaml":
            await self.ato_yaml(file_path)
        elif file_format == "json":
            await self.ato_json(file_path)
        else:
            raise ValueError("Unsupported file format. Use 'yaml' or 'json'.")

        return file_path

    def upgrade(self):
        """
        Placeholder method for upgrading the model instance to a new version.
        Implement version-specific upgrade logic here.
        """
        pass

    def to_yaml(self, file_path: Optional[str] = None) -> str:
        """
        Serializes the Pydantic model instance into a YAML string and optionally writes it to a file.

        :param file_path: The file path to write the YAML content to.
                          If None, only the YAML string is returned.
        :return: The YAML representation of the model.
        :raises IOError: If serialization to YAML fails.
        """
        try:
            yaml_content = yaml.dump(
                self.model_dump(),
                default_flow_style=False,
                width=1000
            )
            if file_path:
                self._pre_save()
                with open(file_path, "w") as yaml_file:
                    yaml_file.write(yaml_content)
            return yaml_content
        except Exception as e:
            raise IOError(f"Failed to serialize model to YAML: {e}")

    @classmethod
    def from_yaml(cls: Type[T], file_path: str) -> T:
        """
        Reads YAML content from a file and creates an instance of the Pydantic model.

        :param file_path: The path to the YAML file.
        :return: An instance of the Pydantic model populated with data from the YAML file.
        :raises FileNotFoundError: If the YAML file is not found.
        :raises ValueError: If there is a parsing or validation error.
        """
        try:
            with open(file_path) as yaml_file:
                data = yaml.safe_load(yaml_file)
            instance = cls.model_validate(data)
            instance._post_load()
            return instance
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found at {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file at {file_path}: {e}")
        except ValidationError as ve:
            raise ValueError(f"Validation error while creating {cls.__name__} instance: {ve}")

    async def ato_yaml(self, file_path: Optional[str] = None) -> str:
        """
        Asynchronously serializes the Pydantic model to YAML and writes to a file.

        :param file_path: The file path to write the YAML content.
                          If None, returns YAML string.
        :return: The YAML content as a string.
        :raises IOError: If serialization to YAML asynchronously fails.
        """
        try:
            yaml_content = yaml.dump(
                self.model_dump(),
                default_flow_style=False,
                width=1000
            )
            if file_path:
                self._pre_save()
                async with aiofiles.open(file_path, "w") as yaml_file:
                    await yaml_file.write(yaml_content)
            return yaml_content
        except Exception as e:
            raise IOError(f"Failed to serialize model to YAML asynchronously: {e}")

    @classmethod
    async def afrom_yaml(cls: Type[T], file_path: str) -> T:
        """
        Asynchronously reads YAML content from a file and constructs an instance of the Pydantic model.

        :param file_path: The file path from which to read the YAML content.
        :return: An instance of the Pydantic model.
        :raises FileNotFoundError: If the YAML file is not found.
        :raises ValueError: If there is a parsing or validation error.
        """
        try:
            async with aiofiles.open(file_path, "r") as yaml_file:
                data = yaml.safe_load(await yaml_file.read())
            instance = cls.model_validate(data)
            instance._post_load()
            return instance
        except FileNotFoundError:
            raise FileNotFoundError(f"YAML file not found at {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file at {file_path}: {e}")
        except ValidationError as ve:
            raise ValueError(f"Validation error while creating {cls.__name__} instance: {ve}")

    def to_json(self, file_path: Optional[str] = None, **kwargs) -> str:
        """
        Serializes the Pydantic model instance into a JSON string and optionally writes it to a file.

        :param file_path: The file path to write the JSON content to.
                          If None, only the JSON string is returned.
        :param kwargs: Additional keyword arguments to pass to json.dumps.
        :return: The JSON representation of the model.
        :raises IOError: If serialization to JSON fails.
        """
        try:
            json_content = self.model_dump_json(**kwargs)
            if file_path:
                self._pre_save()
                with open(file_path, "w") as json_file:
                    json_file.write(json_content)
            return json_content
        except Exception as e:
            raise IOError(f"Failed to serialize model to JSON: {e}")

    @classmethod
    def from_json(cls: Type[T], file_path: str) -> T:
        """
        Reads JSON content from a file and creates an instance of the Pydantic model.

        :param file_path: The path to the JSON file.
        :return: An instance of the Pydantic model populated with data from the JSON file.
        :raises FileNotFoundError: If the JSON file is not found.
        :raises ValueError: If there is a parsing or validation error.
        """
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
            instance = cls.model_validate(data)
            instance._post_load()
            return instance
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found at {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file at {file_path}: {e}")
        except ValidationError as ve:
            raise ValueError(f"Validation error while creating {cls.__name__} instance: {ve}")

    @classmethod
    @contextmanager
    def io_context(
        cls: Type[T],
        model_defaults: Optional[Dict[str, Any]] = None,
        file_path: Optional[str] = None,
        file_format: str = "yaml"
    ):
        """
        Context manager for convenient loading and saving of Pydantic models to/from YAML or JSON files.

        :param model_defaults: Default values to use if the file doesn't exist.
        :param file_path: Path to the file. If None, uses the class name as the filename.
        :param file_format: The format of the file ('yaml' or 'json').
        :raises ValueError: If an unsupported file format is provided.
        :raises RuntimeError: If an error occurs during the context manager operation.
        """
        if model_defaults is None:
            model_defaults = {}

        if file_path is None:
            filename = f"{cls.__name__}.{file_format}"
        else:
            filename = file_path

        absolute_path = os.path.abspath(filename)

        try:
            if os.path.exists(absolute_path):
                if file_format == "yaml":
                    instance = cls.from_yaml(absolute_path)
                elif file_format == "json":
                    instance = cls.from_json(absolute_path)
                else:
                    raise ValueError("Unsupported file format. Use 'yaml' or 'json'.")
            else:
                instance = cls(**model_defaults)
                instance._post_load()
            yield instance
            instance.save(absolute_path, file_format)
        except Exception as e:
            raise RuntimeError(f"Error in io_context: {e}")

    @classmethod
    @asynccontextmanager
    async def aio_context(
        cls: Type[T],
        model_defaults: Optional[Dict[str, Any]] = None,
        file_path: Optional[str] = None,
        file_format: str = "yaml"
    ):
        """
        Asynchronous context manager for convenient loading and saving of Pydantic models to/from YAML or JSON files.

        :param model_defaults: Default values to use if the file doesn't exist.
        :param file_path: Path to the file. If None, uses the class name as the filename.
        :param file_format: The format of the file ('yaml' or 'json').
        :raises ValueError: If an unsupported file format is provided.
        :raises RuntimeError: If an error occurs during the context manager operation.
        """
        if model_defaults is None:
            model_defaults = {}

        if file_path is None:
            filename = f"{cls.__name__}.{file_format}"
        else:
            filename = file_path

        absolute_path = os.path.abspath(filename)

        try:
            if os.path.exists(absolute_path):
                if file_format == "yaml":
                    instance = await cls.afrom_yaml(absolute_path)
                elif file_format == "json":
                    instance = await cls.afrom_json(absolute_path)
                else:
                    raise ValueError("Unsupported file format. Use 'yaml' or 'json'.")
            else:
                instance = cls(**model_defaults)
                instance._post_load()
            yield instance
            await instance.asave(absolute_path, file_format)
        except Exception as e:
            raise RuntimeError(f"Error in aio_context: {e}")

    async def ato_json(self, file_path: Optional[str] = None, **kwargs) -> str:
        """
        Asynchronously serializes the Pydantic model to JSON and writes to a file.

        :param file_path: The file path to write the JSON content.
                          If None, returns JSON string.
        :param kwargs: Additional keyword arguments to pass to json.dumps.
        :return: The JSON content as a string.
        :raises IOError: If serialization to JSON asynchronously fails.
        """
        try:
            json_content = self.model_dump_json(**kwargs)
            if file_path:
                async with aiofiles.open(file_path, "w") as json_file:
                    await json_file.write(json_content)
            return json_content
        except Exception as e:
            raise IOError(f"Failed to serialize model to JSON asynchronously: {e}")

    @classmethod
    async def afrom_json(cls: Type[T], file_path: str) -> T:
        """
        Asynchronously reads JSON content from a file and constructs an instance of the Pydantic model.

        :param file_path: The file path from which to read the JSON content.
        :return: An instance of the Pydantic model.
        :raises FileNotFoundError: If the JSON file is not found.
        :raises ValueError: If there is a parsing or validation error.
        """
        try:
            async with aiofiles.open(file_path, "r") as json_file:
                data = json.loads(await json_file.read())
            instance = cls.model_validate(data)
            instance._post_load()
            return instance
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found at {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file at {file_path}: {e}")
        except ValidationError as ve:
            raise ValueError(f"Validation error while creating {cls.__name__} instance: {ve}")

    def _post_load(self):
        """
        Hook method called after loading the model instance.
        Override this method to implement custom logic after loading.
        """
        pass

    def _pre_save(self):
        """
        Hook method called before saving the model instance.
        Override this method to implement custom logic before saving.
        """
        pass

    def generate_docs(self) -> str:
        """
        Generates markdown documentation for the model using Pydantic v2.

        :return: The markdown documentation as a string.
        """
        model_data = {
            "model_name": self.__class__.__name__,
            "model_doc": self.__doc__,
            "fields": {
                field_name: {
                    "type": self.__class__.__annotations__.get(field_name, "<class 'str'>"),
                    "description": self.model_fields[field_name].description,
                    "default": self.model_fields[field_name].default
                }
                for field_name in self.model_fields
            }
        }

        return render_str(model_docs, **model_data)

    @classmethod
    def from_prompt(cls: Type[T], prompt: str) -> T:
        """
        Creates an instance of the Pydantic model from a user prompt.

        :param prompt: The user prompt.
        :return: An instance of the Pydantic model.
        """
        from sungen.dspy_modules.gen_pydantic_instance import gen_instance
        return gen_instance(cls, prompt)


model_docs = """# {{ model_name }}

{% if model_doc %}
{{ model_doc }}
{% else %}
No class documentation available.
{% endif %}

## Fields

{% for field_name, field_info in fields.items() %}
### {{ field_name }}
- Type: `{{ field_info['type'] }}`
{% if field_info['description'] %}
- Description: {{ field_info['description'] }}
{% else %}
- Description: No description available.
{% endif %}
{% if field_info['default'] is not none %}
- Default: `{{ field_info['default'] }}`
{% else %}
- Default: No default value.
{% endif %}
{% endfor %}
"""

class PredictType:
    """
    Represents a single prediction task.

    Attributes:
        input_data (dict): The input data for the prediction.
        output_model (Type[T]): The Pydantic model to use for the prediction output.
    """
    prompt: dict
    output_model: Type[T]
#
# def run_dsls(type_pairs: List[PredictType], max_workers=5) -> List[BaseModel]:
#     """
#     Execute a list of typed prediction tasks concurrently while preserving input order.
#
#     This function accepts a list of PredictType tasks, runs them concurrently using a thread pool, and returns
#     their prediction results in the same order as the input list.
#
#     :param type_pairs: A list of PredictType instances representing individual prediction tasks.
#                        Each task contains input data and the output model.
#
#     :returns: A list of prediction results as instances of the respective output models, in the same order as input.
#     :rtype: List[BaseModel]
#
#     :raises Exception: If any prediction task fails, it logs the error and raises an exception.
#     """
#     results = []
#
#     # Initialize logging
#     logger = logging.getLogger(__name__)
#     if not logger.handlers:
#         logging.basicConfig(level=logging.INFO)
#
#     def run_prediction(index: int, task: PredictType) -> (int, BaseModel):
#         """
#         Runs a single prediction task.
#
#         Args:
#             index (int): The index of the task in the original list.
#             task (PredictType): The prediction task to execute.
#
#         Returns:
#             Tuple[int, BaseModel]: A tuple containing the index and the result of the prediction.
#         """
#         try:
#             # Log the prediction start
#             logger.debug(f"Starting prediction with input: {task.input_data} using model: {task.output_model.__name__}")
#
#             # Execute the prediction
#             prediction = predict_type(task.input_data, task.output_model)
#
#             # Log the successful prediction
#             logger.debug(f"Prediction successful for task at index {index}: {prediction}")
#
#             return index, prediction
#         except Exception as e:
#             # Log the exception with input data for context
#             logger.error(f"Prediction failed for task at index {index} with input {task.input_data}: {e}")
#             raise
#
#     # Use ThreadPoolExecutor to run predictions concurrently
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         # Submit all prediction tasks to the executor with their index
#         future_to_task = {executor.submit(run_prediction, i, task): i for i, task in enumerate(type_pairs)}
#
#         # Iterate over the futures as they complete and store the results
#         for future in as_completed(future_to_task):
#             try:
#                 index, result = future.result()  # Retrieve the result and its index
#                 results.append((index, result))  # Store the result with its index
#                 logger.info(f"Prediction succeeded for task at index {index}")
#             except Exception as e:
#                 index = future_to_task[future]
#                 logger.error(f"Prediction failed for task at index {index} with error: {e}")
#
#     # Sort results by the original task index and return only the predictions (discard the index)
#     results.sort(key=lambda x: x[0])
#     return [result for _, result in results]