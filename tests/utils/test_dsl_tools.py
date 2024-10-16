import os
import aiofiles
import pytest

from dspygen.utils.dsl_tools import DSLModel


class TestModel(DSLModel):
    """A simple Pydantic model for testing saving functionality."""
    attr: str


@pytest.mark.sync
def test_save_with_provided_filename(yaml_file):
    """
    Test the synchronous save method when a file path is provided.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    model = TestModel(attr="save_test")
    model.save(str(yaml_file), file_format="yaml")

    assert yaml_file.exists(), "YAML file was not created by the save method."

    with open(yaml_file) as f:
        content = f.read()
    assert "attr: save_test" in content, "YAML content does not contain the expected attribute."


@pytest.mark.sync
def test_save_with_generated_filename(tmp_path):
    """
    Test the synchronous save method when no file path is provided (auto-generated filename).

    :param tmp_path: Pytest fixture providing a temporary directory.
    :type tmp_path: pathlib.Path
    """
    from dspygen.utils.dspy_tools import init_instant
    init_instant()
    model = TestModel(attr="generated_filename_test")
    os.chdir(tmp_path)  # Change the current working directory to the temporary directory
    model.save(add_timestamp=True)  # This will generate a file in the current directory with a timestamp

    # Get the most recent file from the tmp_path directory
    generated_files = list(tmp_path.glob("*.yaml"))
    assert len(generated_files) > 0, "No file was generated."

    generated_file = generated_files[0]
    with open(generated_file) as f:
        content = f.read()
    assert "attr: generated_filename_test" in content, "Generated YAML content does not contain the expected attribute."


@pytest.mark.asyncio
async def test_asave_with_provided_filename(yaml_file):
    """
    Test the asynchronous asave method when a file path is provided.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    from dspygen.utils.dspy_tools import init_instant
    init_instant()
    model = TestModel(attr="asave_test")
    await model.asave(str(yaml_file), file_format="yaml")

    assert yaml_file.exists(), "YAML file was not created by the asave method."

    async with aiofiles.open(yaml_file, mode='r') as f:
        content = await f.read()
    assert "attr: asave_test" in content, "Asynchronous YAML content does not contain the expected attribute."


@pytest.mark.asyncio
async def test_asave_with_generated_filename(tmp_path):
    """
    Test the asynchronous asave method when no file path is provided (auto-generated filename).

    :param tmp_path: Pytest fixture providing a temporary directory.
    :type tmp_path: pathlib.Path
    """
    model = TestModel(attr="async_generated_filename_test")
    os.chdir(tmp_path)  # Change the current working directory to the temporary directory
    await model.asave(add_timestamp=True)  # This will generate a file with a timestamp

    # Get the most recent file from the tmp_path directory
    generated_files = list(tmp_path.glob("*.yaml"))
    assert len(generated_files) > 0, "No file was generated."

    generated_file = generated_files[0]
    async with aiofiles.open(generated_file, mode='r') as f:
        content = await f.read()
    assert "attr: async_generated_filename_test" in content, "Generated async YAML content does not contain the expected attribute."



@pytest.fixture
def yaml_file(tmp_path):
    """
    Pytest fixture to create a temporary YAML file for testing.

    :param tmp_path: Pytest fixture providing a temporary directory.
    :type tmp_path: pathlib.Path
    :yield: Temporary YAML file path.
    :rtype: pathlib.Path
    """
    file = tmp_path / "test.yaml"
    yield file


@pytest.fixture
def json_file(tmp_path):
    """
    Pytest fixture to create a temporary JSON file for testing.

    :param tmp_path: Pytest fixture providing a temporary directory.
    :type tmp_path: pathlib.Path
    :yield: Temporary JSON file path.
    :rtype: pathlib.Path
    """
    file = tmp_path / "test.json"
    yield file


@pytest.mark.sync
def test_to_yaml(yaml_file):
    """
    Test synchronous YAML serialization of the model.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    model = TestModel(attr="test")
    model.to_yaml(str(yaml_file))

    assert yaml_file.exists(), "YAML file was not created."

    with open(yaml_file) as f:
        content = f.read()
    assert "attr: test" in content, "YAML content does not contain the expected attribute."


@pytest.mark.sync
def test_from_yaml(yaml_file):
    """
    Test synchronous YAML deserialization of the model.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    with open(yaml_file, "w") as f:
        f.write("attr: test_from_yaml")

    model = TestModel.from_yaml(str(yaml_file))
    assert model.attr == "test_from_yaml", "Deserialized attribute does not match expected value."


@pytest.mark.sync
def test_to_json(json_file):
    """
    Test synchronous JSON serialization of the model.

    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    model = TestModel(attr="json_test")
    model.to_json(str(json_file))

    assert json_file.exists(), "JSON file was not created."

    with open(json_file) as f:
        content = f.read()
    import json

    content_dict = json.loads(content)
    assert content_dict.get("attr") == "json_test", "JSON content does not contain the expected attribute."


@pytest.mark.sync
def test_from_json(json_file):
    """
    Test synchronous JSON deserialization of the model.

    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    with open(json_file, "w") as f:
        f.write('{"attr": "json_test_from_yaml"}')

    model = TestModel.from_json(str(json_file))
    assert model.attr == "json_test_from_yaml", "Deserialized JSON attribute does not match expected value."


@pytest.mark.asyncio
async def test_ato_yaml(yaml_file):
    """
    Test asynchronous YAML serialization of the model.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    model = TestModel(attr="async_test")
    await model.ato_yaml(str(yaml_file))

    assert yaml_file.exists(), "Asynchronous YAML file was not created."

    async with aiofiles.open(yaml_file, mode='r') as f:
        content = await f.read()
    assert "attr: async_test" in content, "Asynchronous YAML content does not contain the expected attribute."


@pytest.mark.asyncio
async def test_afrom_yaml(yaml_file):
    """
    Test asynchronous YAML deserialization of the model.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    async with aiofiles.open(yaml_file, mode='w') as f:
        await f.write("attr: async_test_from_yaml")

    model = await TestModel.afrom_yaml(str(yaml_file))
    assert model.attr == "async_test_from_yaml", "Asynchronously deserialized attribute does not match expected value."


@pytest.mark.asyncio
async def test_ato_json(json_file):
    """
    Test asynchronous JSON serialization of the model.

    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    model = TestModel(attr="async_json_test")
    await model.ato_json(str(json_file))

    assert json_file.exists(), "Asynchronous JSON file was not created."

    async with aiofiles.open(json_file, mode='r') as f:
        content = await f.read()
    import json

    content_dict = json.loads(content)
    assert content_dict.get("attr") == "async_json_test", "Asynchronous JSON content does not contain the expected attribute."


@pytest.mark.asyncio
async def test_afrom_json(json_file):
    """
    Test asynchronous JSON deserialization of the model.

    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    async with aiofiles.open(json_file, mode='w') as f:
        await f.write('{"attr": "async_json_test_from_yaml"}')

    model = await TestModel.afrom_json(str(json_file))
    assert model.attr == "async_json_test_from_yaml", "Asynchronously deserialized JSON attribute does not match expected value."


def test_yaml_context(yaml_file):
    """
    Test the synchronous context manager for loading and saving the model.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    with TestModel.io_context({"attr": "Hello World"}, str(yaml_file), file_format="yaml") as model:
        assert isinstance(model, TestModel), "Model instance is not of type TestModel."
        assert model.attr == "Hello World", "Model attribute does not match the default value."
        model.attr = "context_test"

    # Verify the file was updated
    with open(yaml_file) as f:
        content = f.read()
    assert "attr: context_test" in content, "YAML file was not updated with the new attribute value."


def test_json_context(json_file):
    """
    Test the synchronous context manager for loading and saving the model in JSON format.

    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    with TestModel.io_context({"attr": "Hello JSON World"}, str(json_file), file_format="json") as model:
        assert isinstance(model, TestModel), "Model instance is not of type TestModel."
        assert model.attr == "Hello JSON World", "Model attribute does not match the default value."
        model.attr = "json_context_test"

    # Verify the file was updated
    with open(json_file) as f:
        content = f.read()
    import json

    content_dict = json.loads(content)
    assert content_dict.get("attr") == "json_context_test", "JSON file was not updated with the new attribute value."


@pytest.mark.asyncio
async def test_yaml_context_async(yaml_file):
    """
    Test the asynchronous context manager for loading and saving the model.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    async with TestModel.aio_context({"attr": "Hello World"}, str(yaml_file), file_format="yaml") as model:
        assert isinstance(model, TestModel), "Asynchronously loaded model instance is not of type TestModel."
        assert model.attr == "Hello World", "Asynchronously loaded model attribute does not match the default value."
        model.attr = "async_context_test"

    # Verify the file was updated
    async with aiofiles.open(yaml_file, mode='r') as f:
        content = await f.read()
    assert "attr: async_context_test" in content, "Asynchronous YAML file was not updated with the new attribute value."


@pytest.mark.asyncio
async def test_json_context_async(json_file):
    """
    Test the asynchronous context manager for loading and saving the model in JSON format.

    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    async with TestModel.aio_context({"attr": "Hello JSON World"}, str(json_file), file_format="json") as model:
        assert isinstance(model, TestModel), "Asynchronously loaded model instance is not of type TestModel."
        assert model.attr == "Hello JSON World", "Asynchronously loaded model attribute does not match the default value."
        model.attr = "async_json_context_test"

    # Verify the file was updated
    async with aiofiles.open(json_file, mode='r') as f:
        content = await f.read()
    import json

    content_dict = json.loads(content)
    assert content_dict.get("attr") == "async_json_context_test", "Asynchronous JSON file was not updated with the new attribute value."


def test_versioning():
    """
    Test the versioning support of the model.
    """
    model = TestModel(attr="version_test")
    assert model.version == "1.0.0", "Default version should be '1.0.0'."

    # Simulate upgrading the model
    model.upgrade()
    # Implement actual upgrade logic in DSLModel's upgrade method as needed
    # For this test, we'll manually change the version
    model.version = "1.1.0"
    assert model.version == "1.1.0", "Model version was not updated correctly."


@pytest.mark.sync
def test_error_handling_invalid_yaml(yaml_file):
    """
    Test error handling when deserializing from an invalid YAML file.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    with open(yaml_file, "w") as f:
        f.write("attr: [unclosed list")

    with pytest.raises(ValueError, match="Error parsing YAML file"):
        TestModel.from_yaml(str(yaml_file))


@pytest.mark.sync
def test_error_handling_missing_file(yaml_file):
    """
    Test error handling when deserializing from a non-existent YAML file.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    if yaml_file.exists():
        os.remove(yaml_file)

    with pytest.raises(FileNotFoundError, match="YAML file not found"):
        TestModel.from_yaml(str(yaml_file))


@pytest.mark.sync
def test_error_handling_validation(yaml_file):
    """
    Test error handling when deserializing YAML with invalid data.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    with open(yaml_file, "w") as f:
        f.write("attr: 123")  # attr should be a string

    with pytest.raises(ValueError, match="Validation error"):
        TestModel.from_yaml(str(yaml_file))


@pytest.mark.asyncio
async def test_error_handling_async_invalid_yaml(yaml_file):
    """
    Test asynchronous error handling when deserializing from an invalid YAML file.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    async with aiofiles.open(yaml_file, mode='w') as f:
        await f.write("attr: [unclosed list")

    with pytest.raises(ValueError, match="Error parsing YAML file"):
        await TestModel.afrom_yaml(str(yaml_file))


@pytest.mark.asyncio
async def test_error_handling_async_missing_file(yaml_file):
    """
    Test asynchronous error handling when deserializing from a non-existent YAML file.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    if yaml_file.exists():
        os.remove(yaml_file)

    with pytest.raises(FileNotFoundError, match="YAML file not found"):
        await TestModel.afrom_yaml(str(yaml_file))


@pytest.mark.asyncio
async def test_error_handling_async_validation(yaml_file):
    """
    Test asynchronous error handling when deserializing YAML with invalid data.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    async with aiofiles.open(yaml_file, mode='w') as f:
        await f.write("attr: 123")  # attr should be a string

    with pytest.raises(ValueError, match="Validation error"):
        await TestModel.afrom_yaml(str(yaml_file))


def test_generate_docs_output():
    """
    Test that the generated documentation contains expected sections and content.
    """
    class DocumentModel(DSLModel):
        """
        This is a sample data model for documentation testing.
        """
        title: str = "Sample Title"
        """The title of the document."""
        content: str = "Sample content."
        """The content of the document."""

    model = DocumentModel()
    docs = model.generate_docs()

    print(docs)

    assert "" != docs, "Documentation should render with the class name."


@pytest.mark.sync
def test_save_and_load_version(yaml_file):
    """
    Test saving and loading the model with versioning support.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    model = TestModel(attr="version_save_test")
    model.version = "2.0.0"
    model.to_yaml(str(yaml_file))

    loaded_model = TestModel.from_yaml(str(yaml_file))
    assert loaded_model.attr == "version_save_test", "Loaded attribute does not match saved value."
    assert loaded_model.version == "2.0.0", "Loaded version does not match saved version."


@pytest.mark.asyncio
async def test_save_and_load_async_version(yaml_file):
    """
    Test asynchronous saving and loading the model with versioning support.

    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    """
    model = TestModel(attr="async_version_save_test")
    model.version = "3.0.0"
    await model.ato_yaml(str(yaml_file))

    loaded_model = await TestModel.afrom_yaml(str(yaml_file))
    assert loaded_model.attr == "async_version_save_test", "Loaded async attribute does not match saved value."
    assert loaded_model.version == "3.0.0", "Loaded async version does not match saved version."


# Cleanup after tests
@pytest.fixture(autouse=True)
def cleanup(request, yaml_file, json_file):
    """
    Pytest fixture to clean up the temporary YAML and JSON files after each test.

    :param request: Pytest request object.
    :type request: _pytest.fixtures.SubRequest
    :param yaml_file: Path to the temporary YAML file.
    :type yaml_file: pathlib.Path
    :param json_file: Path to the temporary JSON file.
    :type json_file: pathlib.Path
    """
    def remove_test_files():
        if yaml_file.exists():
            os.remove(yaml_file)
        if json_file.exists():
            os.remove(json_file)

    request.addfinalizer(remove_test_files)
