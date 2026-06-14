"""
DSPy signature string parser.

Handles signatures like:
    "input_field, other_field -> output_field, second_output"
    "question -> answer"
    "prompt, assertion -> return_bool"
"""

import re
from typing import TypedDict


class ParsedSignature(TypedDict):
    inputs: list[str]
    outputs: list[str]


_ARROW_PATTERN = re.compile(r"\s*->\s*")
_FIELD_SPLIT = re.compile(r"\s*,\s*")
# snake_case: starts with lowercase letter or underscore, rest is alphanumeric + underscore
_SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")


def _split_fields(raw: str) -> list[str]:
    """Split a comma-separated field list, stripping whitespace from each name."""
    if not raw or not raw.strip():
        return []
    return [f.strip() for f in _FIELD_SPLIT.split(raw.strip()) if f.strip()]


def parse_signature(sig_str: str) -> ParsedSignature:
    """
    Parse a DSPy signature string into input and output field name lists.

    Examples:
        >>> parse_signature("question -> answer")
        {'inputs': ['question'], 'outputs': ['answer']}

        >>> parse_signature("input1, input2 -> output1, output2")
        {'inputs': ['input1', 'input2'], 'outputs': ['output1', 'output2']}

        >>> parse_signature("prompt, assertion -> return_bool")
        {'inputs': ['prompt', 'assertion'], 'outputs': ['return_bool']}

    Args:
        sig_str: The signature string to parse.

    Returns:
        A dict with 'inputs' and 'outputs' lists of field name strings.
    """
    if not isinstance(sig_str, str):
        return {"inputs": [], "outputs": []}

    sig_str = sig_str.strip()
    if not sig_str:
        return {"inputs": [], "outputs": []}

    parts = _ARROW_PATTERN.split(sig_str, maxsplit=1)
    if len(parts) == 1:
        # No arrow found — treat everything as inputs, no outputs
        return {"inputs": _split_fields(parts[0]), "outputs": []}

    input_part, output_part = parts[0], parts[1]
    return {
        "inputs": _split_fields(input_part),
        "outputs": _split_fields(output_part),
    }


def validate_signature(sig_str: str) -> list[str]:
    """
    Validate a DSPy signature string and return a list of human-readable error messages.

    Checks:
    - Arrow present
    - Non-empty output fields
    - Non-empty input fields
    - No duplicate field names across inputs/outputs
    - No shared names between inputs and outputs
    - All field names are snake_case

    Args:
        sig_str: The signature string to validate.

    Returns:
        A list of error/warning strings (empty list means valid).
    """
    errors: list[str] = []

    if not isinstance(sig_str, str) or not sig_str.strip():
        errors.append("Signature string is empty or not a string.")
        return errors

    sig_str = sig_str.strip()

    if "->" not in sig_str:
        errors.append("Signature is missing the '->' arrow separator.")
        return errors

    parsed = parse_signature(sig_str)
    inputs = parsed["inputs"]
    outputs = parsed["outputs"]

    if not outputs:
        errors.append("Signature has no output fields (nothing after '->').")

    if not inputs:
        errors.append("Signature has no input fields (nothing before '->').")

    # Check for shared names between inputs and outputs
    input_set = set(inputs)
    output_set = set(outputs)
    conflicts = input_set & output_set
    if conflicts:
        for name in sorted(conflicts):
            errors.append(
                f"Field name '{name}' appears in both inputs and outputs."
            )

    # Check for duplicate names within inputs
    seen: set[str] = set()
    for name in inputs:
        if name in seen:
            errors.append(f"Duplicate input field name: '{name}'.")
        seen.add(name)

    # Check for duplicate names within outputs
    seen = set()
    for name in outputs:
        if name in seen:
            errors.append(f"Duplicate output field name: '{name}'.")
        seen.add(name)

    # Check snake_case convention
    all_fields = inputs + outputs
    for name in all_fields:
        if not _SNAKE_CASE.match(name):
            errors.append(
                f"Field name '{name}' is not snake_case "
                "(should start with a lowercase letter or underscore and contain only "
                "lowercase letters, digits, and underscores)."
            )

    return errors


def extract_field_names(sig_str: str) -> list[str]:
    """
    Extract all field names (inputs + outputs) from a DSPy signature string.

    Args:
        sig_str: The signature string.

    Returns:
        A flat list of all field names.
    """
    parsed = parse_signature(sig_str)
    return parsed["inputs"] + parsed["outputs"]
