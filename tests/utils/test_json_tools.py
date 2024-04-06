import pytest

from dspygen.utils.json_tools import extract


def test_extracts_object_from_a_string():
    input_str = 'Some text { "key": "value" } some other text'
    expected = {"key": "value"}
    assert extract(input_str) == expected

def test_extracts_array_from_a_string():
    input_str = "Before text [1,2,3] after text"
    expected = [1, 2, 3]
    assert extract(input_str) == expected

def test_returns_none_for_strings_without_objects_or_arrays():
    input_str = "No objects or arrays here!"
    assert extract(input_str) is None

def test_handles_nested_structures_correctly():
    input_str = 'Text { "nested": { "key": "value" }} more text'
    expected = {"nested": {"key": "value"}}
    assert extract(input_str) == expected

def test_handles_multiple_nested_structures_correctly():
    input_str = 'Text { "nested1": { "key": "value" }} more text { "nested2": { "key": "value" }}'
    expected = {"nested1": {"key": "value"}}
    assert extract(input_str) == expected
