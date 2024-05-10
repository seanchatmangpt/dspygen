import dspy

from dspygen.experiments.mock_gen.json_mode_eval_dataset import JsonModeEvalDataset
from dspygen.experiments.mock_gen.jsonpro_optimizer import JSONPRO


import dspy
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from dspygen.experiments.mock_gen.json_mode_eval_dataset import JsonModeEvalDataset
from dspygen.utils.dspy_tools import init_ol, init_dspy
from dspygen.utils.json_tools import extract


class PromptToJSONSignature(dspy.Signature):
    """
    Proposed Instruction: Transform the provided text with key-value pairs into a valid JSON object that conforms to the specified JSON schema. Ensure all required fields are included and that data types match the expected format in the schema. Use curly braces to encapsulate your resulting JSON structure, commas to separate items within an array, colons to separate keys from values, and quotation marks for string literals.
    """
    # Inputs
    json_schema = dspy.InputField(
        desc="JSON schema to validate the JSON object. Your response must exactly adhere to this schema. ")
    prompt = dspy.InputField(
        desc="Text information in structured or unstructured format, to be converted into a JSON object.")
    step_by_step_instructions = dspy.OutputField(
        desc="Explicitly state the steps to extract key-value pairs and format them into JSON, including any specific formatting or data validation requirements.")
    constructed_json_object = dspy.OutputField(
        desc="A JSON object that conforms to the provided JSON schema. from jsonschema import validate",
        prefix="Constructed JSON Object:\n```json\n")


class JSONErrorRetrySignature(dspy.Signature):
    """
    This signature is essential for automating the detection and correction of errors in JSON objects. It focuses on providing detailed feedback on non-compliance with a JSON schema and facilitates targeted modifications to ensure that outputs meet stringent data format and structure requirements. This signature acts as an intermediary step in a data validation workflow, where it interprets validation failures and provides specific, actionable feedback to refine the output.

    Instruction Flow:
    - Analyze the provided JSON object against the schema.
    - Identify specific deviations from the schema requirements.
    - Offer precise corrections to align the JSON output with the schema, enhancing both data integrity and accuracy.
    - Iterate the process to minimize error rates and optimize compliance.
    """
    # Inputs
    json_schema = dspy.InputField(
        desc="A comprehensive blueprint that the JSON object must conform to. It specifies the structure, required fields, permissible data types, and other validation rules essential for the JSON object’s integrity.")
    prompt = dspy.InputField(
        desc="The initial input or instructions used to generate the JSON object. This may include the raw data and specific guidelines or parameters that influenced the JSON creation process.")
    validation_error = dspy.InputField(
        desc="Detailed feedback on the JSON object’s failure points when measured against the schema. This includes type mismatches, missing fields, and structural errors, providing a basis for targeted corrections.")

    # Outputs
    step_by_step_instructions = dspy.OutputField(
        desc="Comprehensive instructions to guide the correction of the JSON object. This includes identifying errors, applying fixes, and validating adjustments to ensure schema compliance.")
    constructed_json_object = dspy.OutputField(
        desc="The revised JSON object post-correction, accurately formatted and validated against the schema, demonstrating full compliance with all specified requirements.",
        prefix="Corrected JSON Object:\n```json\n")


class PromptToJSONModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = PromptToJSONSignature
        self.predictor = dspy.Predict(self.signature)
        # Adding a Retry meta-module for handling retries after failures
        self.retry_predictor = dspy.Predict(JSONErrorRetrySignature)

    def forward(self, schema, prompt):
        result = self.predictor(json_schema=schema, prompt=prompt)
        try:
            # Convert the result from JSON string to a Python dict to validate
            json_output = extract(result.constructed_json_object)
            # Validate the JSON output against the schema
            validate(instance=json_output, schema=json.loads(schema))
            completion = json.dumps(json_output)
        except ValidationError as ve:
            # If validation fails, log the error and retry the prediction
            # dspy.Assert(False, f"{result.constructed_json_object} failed validation")
            # Adjust the prompt or parameters if needed before retrying
            # updated_prompt = self.modify_prompt_based_on_error(prompt, ve)
            result2 = self.retry_predictor(json_schema=schema,
                                           prompt=prompt,
                                           validation_error=str(ve))
            json_output = extract(result2.constructed_json_object)
            # validate(instance=json_output, schema=json.loads(schema))
            completion = json.dumps(json_output)

        except json.JSONDecodeError as je:
            # Handle JSON decoding errors
            print(f"JSON decoding error: {je.msg}")
            return None  # or handle more gracefully as needed

        return dspy.Prediction(
            completion=completion,
        )


def validate_context_and_answer(example, pred, trace=None):
    from dspygen.utils.json_tools import extract
    ecomp = extract(example.completion)
    pcomp = extract(pred.completion)
    return pcomp == ecomp


from dspy.teleprompt import COPRO

teleprompter = COPRO(
    metric=validate_context_and_answer,
    verbose=True,
    batch_size=2,
    depth=2,
)


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()
    # init_dspy(api_key="sk-my-service-account-h1hYB7umvc95nTjqj0dPT3BlbkFJsMKub3QPxM8lO7l2Ekxs")
    from dsp.utils import dotdict

    dataset = JsonModeEvalDataset()
    #
    # print(dataset)
    # print(dataset.train[0]['prompt'], dataset.train[0]['completion'])
    # print(len(dataset.train), len(dataset.dev), len(dataset.test))
    #
    # if dataset.dev:
    #     print(dataset.dev[0]['prompt'], dataset.dev[0]['completion'])

    # NUM_THREADS = 5
    # evaluate = Evaluate(devset=dataset.dev, metric=validate_context_and_answer, num_threads=NUM_THREADS,
    #                     display_progress=True, display_table=False)
    from dspy.teleprompt import COPRO

    teleprompter = COPRO(
        metric=validate_context_and_answer,
        verbose=True,
    )

    kwargs = dict(num_threads=1, display_progress=True,
                  display_table=0)  # Used in Evaluate class in the optimization process
    cot = PromptToJSONModule()
    compiled_prompt_opt = teleprompter.compile(cot, trainset=dataset.train[:5], eval_kwargs=kwargs)
    from datetime import datetime

    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Convert the datetime object to a string in the format 'YYYY-MM-DD HH:MM:SS'
    zulu_time_str = current_time_utc.strftime('%Y-%m-%d %H:%M:%S')

    compiled_prompt_opt.save(f"compiled_prompt_opt_advanced_{zulu_time_str}.json")
    cot.save(f"cot_{zulu_time_str}.json")


if __name__ == '__main__':
    while True:
        main()
