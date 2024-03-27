import aiofiles
import pytest
import os
import asyncio
from pydantic import BaseModel

from dspygen.utils.yaml_tools import YAMLMixin


# Assuming YAMLMixin is in yaml_mixin.py


# Define a simple Pydantic model for testing
class TestModel(BaseModel, YAMLMixin):
    attr: str


@pytest.fixture
def yaml_file(tmp_path):
    # Create a temporary YAML file for testing
    file = tmp_path / "test.yaml"
    yield file


@pytest.mark.sync
def test_to_yaml(yaml_file):
    # Test synchronous YAML serialization
    model = TestModel(attr="test")
    model.to_yaml(yaml_file)

    assert yaml_file.exists()
    with open(yaml_file) as f:
        content = f.read()
    assert "attr: test" in content


@pytest.mark.sync
def test_from_yaml(yaml_file):
    # Test synchronous YAML deserialization
    with open(yaml_file, "w") as f:
        f.write("attr: test_from_yaml")

    model = TestModel.from_yaml(yaml_file)
    assert model.attr == "test_from_yaml"


@pytest.mark.asyncio
async def test_ato_yaml(yaml_file):
    # Test asynchronous YAML serialization
    model = TestModel(attr="async_test")
    await model.ato_yaml(yaml_file)

    assert yaml_file.exists()
    async with aiofiles.open(yaml_file, mode='r') as f:
        content = await f.read()
    assert "attr: async_test" in content


@pytest.mark.asyncio
async def test_afrom_yaml(yaml_file):
    # Test asynchronous YAML deserialization
    async with aiofiles.open(yaml_file, mode='w') as f:
        await f.write("attr: async_test_from_yaml")

    model = await TestModel.afrom_yaml(yaml_file)
    assert model.attr == "async_test_from_yaml"


def test_yaml_context(yaml_file):
    # Test the synchronous context manager
    with TestModel.io_context({"attr": "Hello World"}, yaml_file) as model:
        assert isinstance(model, TestModel)
        model.attr = "context_test"

    # Verify the file was updated
    with open(yaml_file) as f:
        content = f.read()
    assert "attr: context_test" in content


@pytest.mark.asyncio
async def test_yaml_context_async(yaml_file):
    # Test the asynchronous context manager
    async with TestModel.aio_context({"attr": "Hello World"}, yaml_file) as model:
        assert isinstance(model, TestModel)
        model.attr = "async_context_test"

    # Verify the file was updated
    async with aiofiles.open(yaml_file, mode='r') as f:
        content = await f.read()
    assert "attr: async_context_test" in content


# Cleanup after tests
@pytest.fixture(autouse=True)
def cleanup(request, yaml_file):
    # Remove the test YAML file after each test
    def remove_test_file():
        if os.path.exists(yaml_file):
            os.remove(yaml_file)

    request.addfinalizer(remove_test_file)
