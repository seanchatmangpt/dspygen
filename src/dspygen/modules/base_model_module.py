import dspy
import typing

from pydantic import BaseModel, Field


Model = typing.TypeVar('Model', bound='BaseModel')


class GenerateJSONForPrompt(dspy.Signature):
    """
    Takes a prompt and a response schema and returns a JSON formatted prompt. Make sure the schema is completely
    aligned with the prompt and schema
    """
    prompt = dspy.InputField(desc="Text prompt for generating the response.")
    response_schema = dspy.InputField(desc="Schema describing the desired structure of the response.")

    json_for_prompt = dspy.OutputField(desc="JSON formatted prompt based on input specifications.",
                                       prefix="Only return the JSON formatted prompt based on the input specifications "
                                              "and schema.\n\n```json\n",)


class BaseModelModule(dspy.Module):
    """JsonModule"""
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, model: type[Model], prompt) -> Model:
        pred = dspy.ChainOfThought(GenerateJSONForPrompt)
        from inspect import getsource
        result = pred(response_schema=str(model.model_json_schema()), prompt=prompt).json_for_prompt
        print(result)
        from dspygen.utils.json_tools import extract
        result = extract(result)
        self.output = model.model_validate(result)
        return self.output


# RFC 5545 VEvent
class VEvent(BaseModel):
    dtstart: str
    dtend: str
    summary: str
    location: str
    description: str


class HelloWorldModel(BaseModel):
    guid: str = Field(..., description="The GUID of the message.")
    message: str = Field(..., description="The message to be displayed.")
    world_description: str = Field(..., description="The description of the world. Required")


def model_call(model: type[Model], prompt: str) -> Model:
    """Takes the BaseModel type and prompt and returns the BaseModel instance."""
    model_module = BaseModelModule()
    return model_module.forward(model=model, prompt=prompt)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    # init_ol(model="llama3")
    init_ol(model="phi3:instruct")
    # pred = dspy.Predict(GenerateJSONForPrompt)
    # result = pred(response_schema=str(HelloWorldModel.model_json_schema()), prompt="Hello, World!").json_for_prompt
    # from dspygen.utils.json_tools import extract
    # result = extract(result)
    # print(result)

    vevent_meeting_desc = """Hello Robin, I would like to schedule a meeting with you.
    The meeting will be held at the conference room on the 5th floor.
    The meeting will start at 10:00 AM and end at 11:00 AM, May 9th 2024.
    The purpose of the meeting is to discuss the upcoming project.
    """

    vevent = model_call(VEvent, vevent_meeting_desc)

    print(vevent)


if __name__ == '__main__':
    main()
