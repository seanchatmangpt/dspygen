"""dspygen testing utilities — fixtures, factories, and helpers."""
from dspygen.testing.factories import MockLM, MockPredict, make_module_runner
from dspygen.testing.fixtures import dspy_lm, mock_predict, pipeline_executor
from dspygen.testing.helpers import assert_module_output, assert_signature_valid

__all__ = [
    "MockLM", "MockPredict", "make_module_runner",
    "assert_signature_valid", "assert_module_output",
    "dspy_lm", "mock_predict", "pipeline_executor",
]
