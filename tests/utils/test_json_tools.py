import json

import pytest

from dspygen.utils.json_tools import extract, generate_from_schema, strip_non_validation_properties


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


def test_generate_simple_object():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        }
    }
    result = generate_from_schema(schema)
    assert isinstance(result, dict)
    assert "name" in result and isinstance(result['name'], str)
    assert "age" in result and isinstance(result['age'], int)


def test_generate_nested_object():
    schema = {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                }
            }
        }
    }
    result = generate_from_schema(schema)
    assert isinstance(result, dict)
    assert isinstance(result['user'], dict)
    assert "name" in result['user'] and isinstance(result['user']['name'], str)
    assert "email" in result['user'] and isinstance(result['user']['email'], str)


def test_generate_array_of_objects():
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "active": {"type": "boolean"}
            }
        }
    }
    result = generate_from_schema(schema)
    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)
    assert all('id' in item and isinstance(item['id'], int) for item in result)
    assert all('active' in item and isinstance(item['active'], bool) for item in result)


def test_complex_schema():
    schema = {"$id": "https://example.com/fstab", "$schema": "https://json-schema.org/draft/2020-12/schema",
              "type": "object", "required": ["/"], "properties": {"/": {"type": "object",
                                                                        "properties": {"device": {"type": "string"},
                                                                                       "mount_point": {
                                                                                           "type": "string"},
                                                                                       "file_system_type": {
                                                                                           "type": "string"},
                                                                                       "options": {"type": "string"},
                                                                                       "dump": {"type": "string",
                                                                                                "pattern": "^[0-1]$"},
                                                                                       "pass": {"type": "string",
                                                                                                "pattern": "^[0-2]$"}},
                                                                        "required": ["device", "mount_point",
                                                                                     "file_system_type", "options",
                                                                                     "dump", "pass"]}},
              "patternProperties": {"^(/[^/]+)+$": {"type": "object", "properties": {"device": {"type": "string"},
                                                                                     "mount_point": {"type": "string"},
                                                                                     "file_system_type": {
                                                                                         "type": "string"},
                                                                                     "options": {"type": "string"},
                                                                                     "dump": {"type": "string",
                                                                                              "pattern": "^[0-1]$"},
                                                                                     "pass": {"type": "string",
                                                                                              "pattern": "^[0-2]$"}},
                                                    "required": ["device", "mount_point", "file_system_type", "options",
                                                                 "dump", "pass"]}}, "additionalProperties": False}

    result = generate_from_schema(schema)
    assert isinstance(result, dict)


def test_strip_properties():
    # Example schema with non-validation properties
    schema_example = {
        "title": "User",
        "type": "object",
        "properties": {
            "name": {
                "title": "Name",
                "type": "string",
                "description": "The person's name"
            },
            "age": {
                "title": "Age",
                "type": "integer",
                "description": "The person's age"
            }
        },
        "required": ["name", "age"],
        "description": "A simple user schema"
    }

    # Use the function to strip non-validation properties
    cleaned_schema = strip_non_validation_properties(schema_example)
    assert cleaned_schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "age"]
    }


output_json = """Output: {
  "deal_terms": "2 months free, after that 10% discount for 3 months.",
  "regular_price": 100,
  "monthly_descriptions": [
    {
      "month": 1,
      "description": "Free"
    },
    {
      "month": 2,
      "description": "Free"
    },
    {
      "month": 3,
      "description": "10% discount"
    },
    {
      "month": 4,
      "description": "10% discount"
    },
    {
      "month": 5,
      "description": "10% discount"
    },
    {
      "month": 6,
      "description": "Regular price"
    },
    {
      "month": 7,
      "description": "Regular price"
    },
    {
      "month": 8,
      "description": "Regular price"
    },
    {
      "month": 9,
      "description": "Regular price"
    },
    {
      "month": 10,
      "description": "Regular price"
    },
    {
      "month": 11,
      "description": "Regular price"
    },
    {
      "month": 12,
      "description": "Regular price"
    }
  ]
}"""


def test_extracts_object_from_a_string():
    input_str = output_json
    expected = {
        "deal_terms": "2 months free, after that 10% discount for 3 months.",
        "regular_price": 100,
        "monthly_descriptions": [
            {
                "month": 1,
                "description": "Free"
            },
            {
                "month": 2,
                "description": "Free"
            },
            {
                "month": 3,
                "description": "10% discount"
            },
            {
                "month": 4,
                "description": "10% discount"
            },
            {
                "month": 5,
                "description": "10% discount"
            },
            {
                "month": 6,
                "description": "Regular price"
            },
            {
                "month": 7,
                "description": "Regular price"
            },
            {
                "month": 8,
                "description": "Regular price"
            },
            {
                "month": 9,
                "description": "Regular price"
            },
            {
                "month": 10,
                "description": "Regular price"
            },
            {
                "month": 11,
                "description": "Regular price"
            },
            {
                "month": 12,
                "description": "Regular price"
            }
        ]
    }
    assert extract(input_str) == expected
