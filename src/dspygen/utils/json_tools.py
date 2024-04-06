import json


def extract(string):
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
