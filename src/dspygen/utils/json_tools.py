import json

import jsonschema
from jsonschema.validators import validate


def extract(string) -> dict or None:
    bracket_pairs = {
        '{': '}',
        '[': ']',
    }

    # Find the index of the first opening bracket
    start_index = -1
    for i, char in enumerate(string):
        if char in bracket_pairs:
            start_index = i
            break

    if start_index == -1:
        return None

    opening_char = string[start_index]
    closing_char = bracket_pairs[opening_char]

    count = 0
    end_index = -1

    # Slice the string from the found opening bracket
    substring = string[start_index:]

    # Iterate over the substring to find the matching closing bracket
    for i, char in enumerate(substring):
        if char == opening_char:
            count += 1
        elif char == closing_char:
            count -= 1

        if count == 0:
            end_index = i
            break

    if end_index == -1:
        return None

    # Parse the JSON-like substring into a Python object
    try:
        return json.loads(substring[:end_index + 1])
    except json.JSONDecodeError:
        return None


from faker import Faker
import json
import random

fake = Faker()


def generate_from_schema(schema, check_validity=False, strip_properties=True):
    if type(schema) is str:
        schema = json.loads(schema)
    instance = generate_instance(schema)
    # Validate the instance against the schema
    if check_validity:
        validate_instance(instance, schema)
    if strip_properties:
        instance = strip_non_validation_properties(instance)
    return instance


def generate_instance(schema):
    schema_type = schema.get('type', 'string')
    if schema_type == 'object':
        return {k: generate_instance(v) for k, v in schema.get('properties', {}).items()}
    elif schema_type == 'array':
        item_schema = schema.get('items', {})
        # Assume a default size of the array if not specified
        length = schema.get('minItems', 1)
        return [generate_instance(item_schema) for _ in range(length)]
    elif schema_type == 'string':
        return generate_string(schema)
    elif schema_type == 'number':
        return fake.pyfloat(left_digits=None, right_digits=None, positive=True)
    elif schema_type == 'integer':
        return fake.pyint()
    elif schema_type == 'boolean':
        return fake.pybool()
    else:
        return generate_default(schema)


def generate_string(schema):
    format_type = schema.get('format')
    pattern = schema.get('pattern')

    if format_type == 'email':
        return fake.email()
    elif format_type == 'date':
        return fake.date()
    elif format_type == 'date-time':
        return fake.date_time().isoformat()
    elif format_type == 'uri':
        return fake.uri()
    elif pattern:
        # Simplistic pattern handling for specific cases (demonstration purposes)
        if pattern == '^[0-1]$':
            return str(random.choice(['0', '1']))
        elif pattern == '^[0-2]$':
            return str(random.choice(['0', '1', '2']))
        else:
            # Generic handler for simple patterns
            return generate_matching_string(pattern)
    else:
        return fake.word()


def generate_matching_string(pattern):
    # This is a placeholder function, needs a real implementation
    # For now, it will just return a fixed correct example for known patterns:
    if pattern == '^[0-1]$':
        return random.choice(['0', '1'])
    elif pattern == '^[0-2]$':
        return random.choice(['0', '1', '2'])
    # You would need to extend this to handle other patterns or write a general regex string generator
    return "0"


def validate_instance(instance, schema):
    try:
        validate(instance=instance, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValueError(f"Generated instance does not comply with the schema: {e}")


def generate_default(schema):
    if 'default' in schema:
        return schema['default']
    return None


def strip_non_validation_properties(schema):
    # Define the list of non-validation properties to remove
    non_validation_keys = {"title", "description", "examples"}

    # If the schema is a dictionary, iterate through its items
    if isinstance(schema, dict):
        keys_to_remove = [key for key in schema if key in non_validation_keys]
        for key in keys_to_remove:
            del schema[key]  # Remove the non-validation properties

        # Recursively process nested dictionaries or arrays
        for key, value in schema.items():
            if isinstance(value, dict) or isinstance(value, list):
                strip_non_validation_properties(value)

    # If the schema is a list, process each element in the list
    elif isinstance(schema, list):
        for item in schema:
            strip_non_validation_properties(item)

    return schema


def main2():
    # Example schema with non-validation properties
    json_schema_example = {
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
    cleaned_schema = strip_non_validation_properties(json_schema_example)
    print(cleaned_schema)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Example JSON schema with nested objects and arrays
    schema = {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            },
            "logins": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "format": "date-time"},
                        "successful": {"type": "boolean"}
                    }
                }
            }
        }
    }

    # Generate an instance that matches the schema
    print(json.dumps(generate_from_schema(schema), indent=4))


def main3():
    import json
    from jsonschema import validate, Draft202012Validator, exceptions

    schema = {"$id": "https://example.com/fstab", "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "required": ["/"], "properties": {"/": {"type": "object", "properties": {"device": {"type": "string"}, "mount_point": {"type": "string"}, "file_system_type": {"type": "string"}, "options": {"type": "string"}, "dump": {"type": "string", "pattern": "^[0-1]$"}, "pass": {"type": "string", "pattern": "^[0-2]$"}}, "required": ["device", "mount_point", "file_system_type", "options", "dump", "pass"]}}, "patternProperties": {"^(/[^/]+)+$": {"type": "object", "properties": {"device": {"type": "string"}, "mount_point": {"type": "string"}, "file_system_type": {"type": "string"}, "options": {"type": "string"}, "dump": {"type": "string", "pattern": "^[0-1]$"}, "pass": {"type": "string", "pattern": "^[0-2]$"}}, "required": ["device", "mount_point", "file_system_type", "options", "dump", "pass"]}}, "additionalProperties": False}
    # Test instance
    instance = {
        "/": {
            "device": "/dev/sda1",
            "mount_point": "/",
            "file_system_type": "ext4",
            "options": "defaults",
            "dump": "1",
            "pass": "2"
        },
        "/home": {
            "device": "/dev/sda2",
            "mount_point": "/home",
            "file_system_type": "ext4",
            "options": "defaults",
            "dump": "0",
            "pass": "1"
        }
    }

    try:
        Draft202012Validator(schema).validate(instance)
        print("The instance is valid!")
    except exceptions.ValidationError as e:
        print(f"Validation error: {e.message}")


if __name__ == '__main__':
    # main()
    main3()
