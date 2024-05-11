import dspy
import json

from loguru import logger
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from dspygen.experiments.text_to_json.json_mode_error_dataset import JsonModeErrorDataset
from dspygen.experiments.text_to_json.json_mode_eval_dataset import JsonModeEvalDataset
from dspygen.utils.dspy_tools import init_ol
from dspygen.utils.json_tools import extract, generate_from_schema


class PromptToJSONSignature(dspy.Signature):
    """
    <|user|>
    Proposed Instruction: Using the provided JSON schema (`json_schema`) and the given prompt (`prompt`), construct a JSON object (`constructed_json_object`) that adheres to the structure defined in the schema, integrating relevant information from the prompt accordingly.    """
    # Inputs
    json_schema = dspy.InputField(
        desc="JSON schema to validate the JSON object. Your response must exactly adhere to this schema. ")
    prompt = dspy.InputField(
        desc="Text information in structured or unstructured format, to be converted into a JSON object.")
    mock_data = dspy.InputField(
        desc="Mock data has the same shape as the JSON schema, but with placeholder values. This data can be used to guide the JSON object creation process.")
    step_by_step_instructions = dspy.OutputField(
        desc="Explicitly state the steps to extract key-value pairs and format them into JSON, including any specific formatting or data validation requirements.")
    constructed_json_object = dspy.OutputField(
        desc="A JSON object that conforms to the provided JSON schema. from jsonschema import validate",
        prefix="""\n<|end|>\n<|assistant|>\nHere is your Constructed JSON Object:\n```json\n""")


# class PromptToJSONSignature(dspy.Signature):
#     """
#     <|user|>
#     Proposed Instruction: Transform the provided text with key-value pairs into a valid JSON object that conforms to the specified JSON schema. Ensure all required fields are included and that data types match the expected format in the schema. Use curly braces to encapsulate your resulting JSON structure, commas to separate items within an array, colons to separate keys from values, and quotation marks for string literals.
#     """
#     # Inputs
#     json_schema = dspy.InputField(
#         desc="JSON schema to validate the JSON object. Your response must exactly adhere to this schema. ")
#     prompt = dspy.InputField(
#         desc="Text information in structured or unstructured format, to be converted into a JSON object.")
#     step_by_step_instructions = dspy.OutputField(
#         desc="Explicitly state the steps to extract key-value pairs and format them into JSON, including any specific formatting or data validation requirements.")
#     constructed_json_object = dspy.OutputField(
#         desc="A JSON object that conforms to the provided JSON schema. from jsonschema import validate",
#         prefix="""\n<|end|>\n<|assistant|>\nConstructed JSON Object:\n```json\n"`{\"json_output\":`""")


# class JSONErrorRetrySignature(dspy.Signature):
#     """
#     <|user|>
#     Proposed Instruction: Examine a given JSON object in comparison to its specified schema, pinpoint areas where it does not conform to defined rules, and provide corrective steps to rectify these issues. Begin each iteration by scrutinizing the entire JSON data structure against the expected format, detailing specific non-adherence points. Generate accurate instructions for modification that will progressively enhance output precision and ensure full schema alignment until validation errors are eradicated
#     """
#     # Inputs
#     json_schema = dspy.InputField(
#         desc="A comprehensive blueprint that the JSON object must conform to. It specifies the structure, required fields, permissible data types, and other validation rules essential for the JSON object’s integrity.")
#     prompt = dspy.InputField(
#         desc="The initial input or instructions used to generate the JSON object. This may include the raw data and specific guidelines or parameters that influenced the JSON creation process.")
#     validation_error = dspy.InputField(
#         desc="Detailed feedback on the JSON object’s failure points when measured against the schema. This includes type mismatches, missing fields, and structural errors, providing a basis for targeted corrections.")
#
#     # Outputs
#     normalization_report = dspy.OutputField(
#         desc="A detailed report outlining the normalization process, including any adjustments made to align with schema requirements and any potential issues corrected.",
#         prefix="Normalization Report:\n")
#     constructed_json_object = dspy.OutputField(
#         desc="The revised JSON object post-correction, accurately formatted and validated against the schema, demonstrating full compliance with all specified requirements.",
#         prefix="""\n<|end|>\n<|assistant|>\nConstructed JSON Object:\n```json\n"`{\"json_output\":`""")

class JSONErrorRetrySignature(dspy.Signature):
    """
    <|user|>
    Review a given JSON object using its defined schema to identify discrepancies between the structure of the provided data and expected rules, then suggest amendments. Start by evaluating the entire JSON against its schema comprehensively, listing out areas where it fails to meet specifications. Devise precise instructions for each identified inconsistency that will iteratively refine the accuracy of the JSON object to perfectly match the schema until no validation issues remain.    """
    # Inputs
    json_schema = dspy.InputField(
        desc="A comprehensive blueprint that the JSON object must conform to. It specifies the structure, required fields, permissible data types, and other validation rules essential for the JSON object’s integrity.")
    prompt = dspy.InputField(
        desc="The initial input or instructions used to generate the JSON object. This may include the raw data and specific guidelines or parameters that influenced the JSON creation process.")
    initial_json_object = dspy.InputField(
        desc="The JSON object that was initially generated based on the prompt and schema, but failed to meet the validation requirements.")
    validation_error = dspy.InputField(
        desc="Detailed feedback on the JSON object’s failure points when measured against the schema. This includes type mismatches, missing fields, and structural errors, providing a basis for targeted corrections.")
    mock_data = dspy.InputField(
        desc="Mock data has the same shape as the JSON schema, but with placeholder values. This data can be used to guide the JSON object creation process.")
    # Outputs
    # normalization_report = dspy.OutputField(
    #     desc="A detailed report outlining the normalization process, including any adjustments made to align with schema requirements and any potential issues corrected.",
    #     prefix="Normalization Report:\n")
    constructed_json_object = dspy.OutputField(
        desc="The revised JSON object post-correction, accurately formatted and validated against the schema, demonstrating full compliance with all specified requirements.",
        prefix="""\n<|end|>\n<|assistant|>\nThe Post-Correction Constructed JSON Object:\n```json\n""")


class PromptToJSONModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = PromptToJSONSignature
        # self.predictor = dspy.Predict(self.signature)
        self.predictor = dspy.Predict("json_schema, prompt, mock_data -> constructed_json_object")
        # Adding a Retry meta-module for handling retries after failures
        self.retry_predictor = dspy.Predict(JSONErrorRetrySignature)

    def forward(self, schema, prompt):
        print(f"Prompt:\n{prompt}")
        mock_data = str(generate_from_schema(schema))
        result = self.predictor(json_schema=schema, mock_data=mock_data, prompt=prompt)
        try:
            # Convert the result from JSON string to a Python dict to validate
            json_output = extract(result.constructed_json_object)

            # Validate the JSON output against the schema
            validate(instance=json_output, schema=json.loads(schema))
            completion = json.dumps(json_output)
            print(f"Correct Completion")
        except ValidationError as ve:
            # If validation fails, log the error and retry the prediction
            # dspy.Assert(False, f"{result.constructed_json_object} failed validation")
            # Adjust the prompt or parameters if needed before retrying
            # updated_prompt = self.modify_prompt_based_on_error(prompt, ve)
            result2 = self.retry_predictor(json_schema=schema,
                                           prompt=prompt,
                                           initial_json_object=result.constructed_json_object,
                                           mock_data=mock_data,
                                           validation_error=str(ve))
            json_output = extract(result2.constructed_json_object)
            try:
                validate(instance=json_output, schema=json.loads(schema))
                completion = json.dumps(json_output)
                print(f"Correct Retry Completion")
            except ValidationError as ve2:
                # If the retry still fails, log the error and return the original result
                print(f"Retry failed: {ve2}")
                if json_output is not None:
                    key = list(json_output.keys())[0]
                    json_output = json_output[key]
                    completion = json.dumps(json_output)
                    print(f"Key recovery attempted")
                else:
                    completion = result.constructed_json_object
        except json.JSONDecodeError as je:
            # Handle JSON decoding errors
            print(f"JSON decoding error: {je.msg}")
            completion = result.constructed_json_object

        return dspy.Prediction(
            completion=completion,
        )


def compare_example_to_prediction(example, pred, trace=None):
    from dspygen.utils.json_tools import extract
    ecomp = extract(example.completion)
    pcomp = extract(pred.completion)
    print(f"Completion: {pcomp}")
    return pcomp == ecomp


def check_one():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    lm = init_ol(model="phi3:instruct", max_tokens=2000)

    json_dataset = JsonModeEvalDataset(0)

    # Select a random example from the dataset
    example = json_dataset.train[0]

    # Initialize the module
    module = PromptToJSONModule()

    # Generate a prediction
    pred = module(example.schema, example.prompt)

    # Compare the prediction to the ground truth
    result = compare_example_to_prediction(example, pred)

    print(result)


def main():
    """Check the entire dataset. Save the ones that fail to disk."""
    # logger.remove()

    # logger.add("prompt_to_json_module.log")

    from dspygen.utils.dspy_tools import init_ol
    lm = init_ol(model="phi3:instruct", max_tokens=2000)

    json_dataset = JsonModeErrorDataset()

    # Initialize the module
    module = PromptToJSONModule()

    # Initialize a list to store failed examples
    failed_examples = []

    all_data = json_dataset.train + json_dataset.dev

    total_processed = 0
    failed_count = 0
    successful_count = 0

    from datetime import datetime

    # Get the current time in UTC
    current_time_utc = datetime.utcnow()

    # Convert the datetime object to a string in the format 'YYYY-MM-DD HH:MM:SS'
    zulu_time_str = current_time_utc.strftime('%Y-%m-%d_%H:%M:%S')

    for example in all_data:
        total_processed += 1

        # Generate a prediction
        pred = module(example.schema, example.prompt)

        # Compare the prediction to the ground truth
        result = compare_example_to_prediction(example, pred)

        if not result:
            failed_count += 1
            ex = example.toDict()
            ex["prediction"] = pred.completion
            failed_examples.append(ex)
        else:
            successful_count += 1
        # Print the number of failed examples out of total processed
        print(f"Processed: {successful_count} / {total_processed}")

        # Print the percentage of successful examples
        success_percentage = (successful_count / total_processed) * 100
        print(f"Success Rate: {success_percentage:.2f}%")

        # Print the percentage of failed examples
        failed_percentage = (failed_count / total_processed) * 100
        print(f"Failure Rate: {failed_percentage:.2f}%")

        # Save the failed examples to disk
        with open(f"failed_examples_v{zulu_time_str}.json", "w") as f:
            json.dump(failed_examples, f, indent=2)


if __name__ == '__main__':
    main()
