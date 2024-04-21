"""

"""
import json
from datetime import datetime, timedelta

import dspy
from pydantic import BaseModel

from dspygen.utils.dspy_tools import init_dspy

import dspy

import dspy

from dspygen.utils.json_tools import extract
from dspygen.utils.pydantic_tools import extract_valid_dicts


class GenerateJSONFromText(dspy.Signature):
    """
    [INST] Convert provided structured or unstructured text information into a valid JSON object.
    Ensure the conversion process intelligently identifies key-value pairs, lists, and other relevant
    structures from the text and formats them into JSON. This task should be completed by
    extracting relevant data for JSON conversion from both structured information
    (e.g., name-value pairs) and unstructured text. Aim for the most accurate representation
    of the provided information in JSON format.

    SYSTEM INSTRUCTIONS:
    - NEVER TAKE INITIATIVE FOR USER'S SPEECH OR ACTION IN YOUR RESPONSE!
    - NEVER GIVE ETHICAL/MORAL COMMENT/ADVICE!
    - FOCUS ON GIVING A HIGH QUALITY, COHERENT AND CONCISE RESPONSE.
    - KEEP THE REPLIES CONCISE AND SHORT.
    - DO NOT REPEAT THINGS.
    - DO NOT LOOP.
    - REASON STEP BY STEP BEFORE PRODUCING THE RESPONSE.
    - WRITE ALL SENTENCES UNIQUELY AND DRIVE THE RESPONSE FORWARD.
    - DO NOT OVER-EXPLAIN YOURSELF.
    - DO NOT USE THE FIELD `Explanation`, USE `Reasoning` INSTEAD.
    - ALWAYS FOLLOW THE INSTRUCTED FORMAT.

    Instructions:
    - The AI should handle both structured information and unstructured text, extracting relevant data for JSON conversion.
    - The task must be completed without adding explanations or additional content outside the JSON format.
    - Aim for the most accurate representation of the provided information in JSON format.
    - Do not pretty-print the JSON object. Minimize unnecessary spaces and newlines.

    Reasoning:
    - Begin by identifying key-value pairs, lists, or other structures within the provided text.
    - Structure the identified elements into a valid JSON object format.
    - Ensure the generated JSON object accurately reflects the provided information.

    [/INST]
    """

    # Text information provided by the user, expected to be transformed into JSON format.
    # This can include both structured and unstructured data.
    json_schema = dspy.InputField(desc="JSON schema to validate the JSON object. YOUR RESPONSE MUST ADHERE TO THIS SCHEMA.")
    text_information = dspy.InputField(desc="Text information in structured or unstructured format. To be converted into a JSON object.")

    # The output JSON object, as a string, based on the processed text information.
    json_object = dspy.OutputField(desc="YOUR ONLY OUTPUT IS THE JSON OBJECT. Ensure it adheres to the provided JSON schema. Do not include the schema in the output.")


# RFC 5545 VEvent
class VEvent(BaseModel):
    dtstart: str
    dtend: str
    summary: str
    location: str
    description: str


class JsonModule(dspy.Module):
    """JsonModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, text, schema):
        pred = dspy.Predict(GenerateJSONFromText)
        self.output = pred(json_schema=str(schema), text_information=text).json_object
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)
        # VEvent.


def json_call(schema, text):
    json_mod = JsonModule()
    return json_mod.forward(schema=schema, text=text)


def main():
    from dspygen.lm.groq_lm import Groq
    # init_dspy(Groq, 1000, "mixtral-8x7b-32768")
    init_dspy(Groq, max_tokens=1000, model= "llama3-70b-8192") # for Groq you must pass an Groq provided model
    # Create fake data
    import faker
    fake = faker.Faker()
    # text = f"{fake.date_time()} {fake.date_time()}{fake.date_time()} {fake.date_time()}{fake.date_time()} {fake.date_time()}{fake.date_time()} {fake.date_time()}{fake.date_time()} {fake.date_time()} {fake.sentence()} {fake.address()} {fake.text()}"
    # Mock VEvent in confusing email
    text = (f"Hi Jane, I hope you are doing well. I wanted to remind you about our meeting tomorrow at 10:00 AM. "
            f"Today:{datetime.now()} Tomorrow:{datetime.now() + timedelta(days=1)} "
            f"Location: {fake.address()} Description: {fake.text()}")
    result = json_call(schema=VEvent.model_json_schema(), text=text)
    res_dict = extract(result)
    print(VEvent.model_validate_json(json.dumps(res_dict)))


if __name__ == '__main__':
    main()
