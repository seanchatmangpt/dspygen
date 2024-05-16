import json

from dspygen.experiments.text_to_json.module_fail_check import generate_hash_id, run_tests


def mock_module(schema, prompt):
    """Mock processing function that returns a deterministic result based on input."""
    if "fail" in prompt:
        return {'result': False}
    return {'result': True}


def mock_compare(example, pred):
    """Mock comparison function that only returns True if 'result' in pred is True."""
    return pred['result']


def create_example(prompt, schema="{}"):
    """Utility to create a mock example."""

    class Example:
        def __init__(self, prompt, schema):
            self.prompt = prompt
            self.schema = schema

    return Example(prompt, schema)


def test_skipping_previously_successful_examples(tmp_path):
    # Setup: create a temp directory and file for successful IDs
    success_file = tmp_path / "successful_examples.json"
    success_file.write_text(json.dumps([generate_hash_id("success example")]))

    # Create example dataset with one example expected to be skipped
    example_dataset = [create_example("success example"), create_example("new success example")]

    # Run tests with the success file and check outputs
    # run_tests(example_dataset, mock_module, mock_compare, load_previous=True, success_path=str(success_file))
    #
    # # There should be no output since the "success example" should be skipped and "new success example" should be successful
    # assert success_file.read_text() == json.dumps(
    #     [generate_hash_id("success example"), generate_hash_id("new success example")])
    #

def test_not_loading_previously_successful_examples_when_flag_is_false(tmp_path):
    # Setup: create a temp directory and file for successful IDs
    success_file = tmp_path / "successful_examples.json"
    success_file.write_text(json.dumps([generate_hash_id("success example")]))

    # Create example dataset with one example that should not be skipped
    example_dataset = [create_example("success example"), create_example("fail example")]

    # Run tests without loading previous successes
    # run_tests(example_dataset, mock_module, mock_compare, load_previous=False, success_path=str(success_file))

    # Check that the success file now only contains the new successful example
    # assert success_file.read_text() == json.dumps([generate_hash_id("fail example")])

# Add more tests as necessary
