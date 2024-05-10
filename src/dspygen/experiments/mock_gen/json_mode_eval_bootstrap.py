import dspy
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from dspygen.experiments.mock_gen.json_mode_eval_dataset import JsonModeEvalDataset
from dspygen.utils.dspy_tools import init_ol
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
    This signature is designed to handle errors in JSON object construction by focusing on identifying and rectifying the errors in the JSON output. The model uses this signature to understand the nature of the error and to guide the correction process in a retry mechanism. This is crucial for tasks requiring high accuracy in data format and structure adherence to a JSON schema.

    Instructions: Review the incorrect JSON object, identify the mismatches against the specified JSON schema, and modify the text or processing logic to correct these errors. The goal is to refine the JSON output in subsequent iterations until it fully complies with the JSON schema.
    """
    # Inputs
    json_schema = dspy.InputField(
        desc="The JSON schema that the original JSON output failed to meet. This schema acts as the benchmark for validating the corrected JSON object.")
    prompt = dspy.InputField(
        desc="The prompt that was used to generate the incorrect JSON object. This prompt may need to be adjusted to guide the model in producing a compliant JSON object.")
    validation_error = dspy.InputField(
        desc="The error message or details that describe why the original JSON object failed to meet the JSON schema requirements. This information will help guide the correction process.")
    step_by_step_instructions = dspy.OutputField(
        desc="Explicitly state the steps to extract key-value pairs and format them into JSON, including any specific formatting or data validation requirements.")
    constructed_json_object = dspy.OutputField(
        desc="A JSON object that conforms to the provided JSON schema.",
        prefix="Constructed JSON Object:\n```json\n")


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
            validate(instance=json_output, schema=json.loads(schema))
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


def main():
    """Main function"""
    from dspy.teleprompt import BootstrapFewShot
    # Set up the LM
    lm = init_ol(model="phi3:instruct", max_tokens=20000)
    # lm = init_ol(model="llama3", max_tokens=20000)

    # Load the SWE-bench dataset
    swe_bench = JsonModeEvalDataset(0)
    swe_bench_trainset, swe_bench_devset = swe_bench.train[:4], swe_bench.dev[:10]

    # print(swe_bench_trainset)

    # Set up the optimizer: we want to "bootstrap" (i.e., self-generate) 4-shot examples of our CoT program.
    config = dict(max_bootstrapped_demos=4, max_labeled_demos=4)


    teleprompter = BootstrapFewShot(metric=validate_context_and_answer, **config)
    optimized_cot = teleprompter.compile(PromptToJSONModule(), trainset=swe_bench_trainset)

    from time import time
    optimized_cot.save(f"optimized_cot_sig_{str(time())}.json")

    from dspy.evaluate import Evaluate

    # Set up the evaluator, which can be used multiple times.
    evaluate = Evaluate(devset=swe_bench_devset, metric=validate_context_and_answer, num_threads=1, display_progress=True,
                        display_table=0)

    # Evaluate our `optimized_cot` program.
    evaluate(optimized_cot)

    print(lm.inspect_history(n=1))


if __name__ == '__main__':
    main()
