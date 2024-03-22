import pytest
from unittest.mock import patch
from dspy.utils import DummyLM

from dspygen.dsl.dsl_pipeline_executor import execute_pipeline


# def test_example_pipeline():
#     context = execute_pipeline('/Users/candacechatman/dev/dspygen/src/dspygen/dsl/examples/example_pipeline.yaml')
#
#     assert "John" in context.processed_data
#     assert "Jane" in context.report


@pytest.fixture
def example_lm_response():
    # Customize this list as needed for your tests
    return ["""'Data processed into a structured format:

- id: 1
  name: John
  age: 25

- id: 2
  name: Jane
  age: 30'""", """The final report generated from the structured data:

Report Title: Summary Report

1. John
   - ID: 1
   - Age: 25

2. Jane
   - ID: 2
   - Age: 30

This report provides a summary of the data processed into a structured format. Each entry includes the individual's name, ID, and age. 

---

End of Report."""]


@patch('dspygen.dsl.dsl_step_module._get_language_model_instance')
def test_execute_pipeline(mock_get_lm, example_lm_response):
    # Setup the mock to return a DummyLM instance with the specified response
    mock_get_lm.return_value = DummyLM(example_lm_response)

    init_ctx = {}  # Adjust as needed

    # Execute your pipeline function. Adjust arguments as needed.
    # For demonstration, assuming `execute_pipeline` takes a YAML string directly.
    context = execute_pipeline('/Users/candacechatman/dev/dspygen/src/dspygen/dsl/examples/example_pipeline.yaml',
                               init_ctx=init_ctx)

    # Now you can make assertions about the result
    assert "Data processed" in context.processed_data
    assert "The final report generated" in context.report
    # Add more specific assertions here based on your expected outcome


def test_execute_data_pipeline():
    # Execute your pipeline function. Adjust arguments as needed.
    # For demonstration, assuming `execute_pipeline` takes a YAML string directly.
    context = execute_pipeline('/dsl/data_hello_world_pipeline.yaml')

    # Now you can make assertions about the result
    assert len(context.HelloWorldModule) == 5
    # Add more specific assertions here based on your expected outcome
