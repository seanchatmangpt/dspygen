import ast
import re
from typing import Any

from pydantic import BaseModel

from dspygen.modules.gen_pydantic_instance import GenPydanticDict
from dspygen.utils.yaml_tools import YAMLMixin


class InstanceMixin:
    @classmethod
    def to_inst(cls, prompt):
        """
        Turns the prompt into the instance of the Pydantic model.
        """
        inst_dict = GenPydanticDict(model=cls)(prompt)
        return cls.model_validate(inst_dict)


def extract_valid_dicts(s: str) -> list[dict[str, Any]]:
    valid_dicts = []

    # Regular expression to find dictionary-like patterns
    # This pattern looks for sequences that start with '{', end with '}', and contain any characters in between.
    # Adjust the pattern as needed to more accurately capture the dictionaries in your strings.
    dict_patterns = re.finditer(r"\{.*?\}", s, re.DOTALL)

    for match in dict_patterns:
        dict_str = match.group()
        try:
            # Attempt to safely evaluate the string to a dict
            potential_dict = ast.literal_eval(dict_str)
            if isinstance(potential_dict, dict):
                valid_dicts.append(potential_dict)
        except (SyntaxError, ValueError):
            # If evaluation fails or the result is not a dict, ignore this match
            continue

    return valid_dicts



def main():
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    class ContactModel(BaseModel, InstanceMixin, YAMLMixin):
        name: str
        age: int
        email: str
        address: str

    # contact = ContactModel.to_inst("John Doe, 30, john@doe.com, 123 Main St.")
    contact = ContactModel.from_yaml("contact.yaml")

    print(contact)

    contact.to_yaml("contact.yaml")


if __name__ == '__main__':
    main()
