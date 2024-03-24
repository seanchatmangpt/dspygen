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
