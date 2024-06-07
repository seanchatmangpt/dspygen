import typing

import dspy
import json

from loguru import logger
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from dspygen.experiments.text_to_json.json_mode_error_dataset import JsonModeErrorDataset
from dspygen.experiments.text_to_json.json_mode_eval_dataset import JsonModeEvalDataset
from dspygen.utils.dspy_tools import init_ol
from dspygen.utils.json_tools import extract, generate_from_schema, strip_non_validation_properties
from dspygen.models.bpm_plus_domain_models import DMN, Rule

Model = typing.TypeVar('Model', bound='BaseModel')

def compare_example_to_prediction(example, pred, trace=None):
    # Metric to compare predicted JSON to the actual JSON in the dataset

    out_d = extract(example.completion.replace("'", '"').replace("hours and", "hours"))
    pred_d = extract(pred.completion)
    #print("---- trace", trace)
    #print(out_d, pred_d)
    # print(out_d == pred_d)
    return pred_d == out_d #is not None


class PromptToJSONSignature(dspy.Signature):
    """
    Proposed Instruction:
    Understand the provided JSON schema, create a relevant prompt based on its contents,
    then use a large language model to generate the output field. Do not include comments.
    """
    # Inputs
    json_schema = dspy.InputField(
        desc="JSON schema to validate the JSON object. Your response must exactly adhere to this schema. ")
    prompt = dspy.InputField(
        desc="Text information in structured or unstructured format, to be converted into a JSON object.")
    # mock_data = dspy.InputField(
    #     desc="Mock data has the same shape as the JSON schema, but with placeholder values. This data can be used to guide the JSON object creation process.")
    step_by_step_instructions = dspy.OutputField(
        desc="Explicitly state the steps to extract key-value pairs and format them into JSON, including any specific formatting or data validation requirements.")
    output = dspy.OutputField(
        desc="A JSON object that conforms to the provided JSON schema.",
        prefix="""```json\n""")


class JSONErrorRetrySignature(dspy.Signature):
    """
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
    # mock_data = dspy.InputField(
    #     desc="Mock data has the same shape as the JSON schema, but with placeholder values. This data can be used to guide the JSON object creation process.")
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
        self.predictor = dspy.Predict("json_schema, prompt -> output")
        # Adding a Retry meta-module for handling retries after failures
        self.retry_predictor = dspy.Predict(JSONErrorRetrySignature)

    def forward(self, schema, prompt):
        print(f"Prompt:\n{prompt}")
        mock_data = str(generate_from_schema(schema))
        result = self.predictor(json_schema=str(schema), prompt=prompt)
        try:
            # Convert the result from JSON string to a Python dict to validate
            json_output = extract(result.output)

            # Validate the JSON output against the schema
            # validate(instance=json_output, schema=schema)

            if json_output is None:
                raise ValidationError("JSON output is not parsing. Make sure it contains only valid JSON.")

            completion = json.dumps(json_output)
            print(f"Correct Completion")
        except ValidationError as ve:
            # If validation fails, log the error and retry the prediction
            # dspy.Assert(False, f"{result.constructed_json_object} failed validation")
            # Adjust the prompt or parameters if needed before retrying
            # updated_prompt = self.modify_prompt_based_on_error(prompt, ve)
            result2 = self.retry_predictor(json_schema=str(schema),
                                           prompt=prompt,
                                           initial_json_object=result.output,
                                           validation_error=str(ve))
            json_output = extract(result2.constructed_json_object)
            try:
                # validate(instance=json_output, schema=schema)
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


def instance(model: typing.Type[Model], prompt: str) -> Model:
    module = PromptToJSONModule()
    result = module.forward(schema=model.model_json_schema(), prompt=prompt).completion
    return model.model_validate_json(result)


dmn_str = """Develop a decision-making model for a loan approval system. The system should evaluate if an applicant qualifies for a personal loan based on their income, credit score, and requested loan amount. The decision process involves:

Inputs:

Income: Monthly income of the applicant.
Credit Score: The credit score of the applicant, reflecting their creditworthiness.
Loan Amount Requested: The total amount the applicant wishes to borrow.
Outputs:

Loan Approval: A decision of 'Approved' or 'Rejected'.
Maximum Loan Amount: If approved, the maximum amount the bank is willing to lend.
Rules:

If the credit score is below 600, the loan is rejected.
If the credit score is above 700 and the income is at least three times the requested loan amount, the loan is approved.
If the requested loan amount is more than 50% of the applicant’s yearly income, the loan is rejected.
Decision Table Details:

The decision table should use the inputs to determine the outputs based on the defined rules."
Decision Structure:

Decision ID: LoanDecision1
Decision Name: Evaluate Loan Approval
Decision Table:

Inputs:

Income: Identified by input1, labeled as 'Monthly Income', expression to capture 'monthlyIncome'.
Credit Score: Identified by input2, labeled as 'Credit Score', expression to capture 'creditScore'.
Loan Amount Requested: Identified by input3, labeled as 'Loan Amount Requested', expression to capture 'loanAmount'.
Outputs:

Loan Approval: Identified by output1, possible values include 'Approved', 'Rejected'.
Maximum Loan Amount: Identified by output2, list the possible amounts or state as dynamic.
Rules:

Rule 1: Input entries for credit score <600 result in 'Rejected' and no maximum amount. 
Rule 2: Input entries for credit score >700 and monthly income >= 3 times the loan amount result in 'Approved' and the same amount as requested.
Rule 3: Input entries for requested loan amount > 50% of annual income (calculated as 12 times monthly income) result in 'Rejected' and no maximum amount."""


def main():
    init_ol(max_tokens=8000)
    #from dspygen.lm.ollama_lm import Ollama
    #from dspygen.utils.dspy_tools import init_dspy
    #init_dspy(Ollama, model="llama3:8b-instruct-fp16", max_tokens=17000)
    #init_dspy(Ollama, model="phi3:3.8b-mini-instruct-4k-fp16", max_tokens=17000)

    # Create fake data
    import faker
    fake = faker.Faker()

    # from dspygen.utils.dspy_tools import init_dspy
    # init_dspy()


    # dmn = instance(Rule, "Input entries for requested loan amount > 50% of annual income (calculated as 12 times monthly income) result in 'Rejected' and no maximum amount.")
    # print(dmn)

    prompt = "Input entries for requested loan amount > 50% of annual income (calculated as 12 times monthly income) result in 'Rejected' and no maximum amount."
    print(prompt)
    print("---------------")
    import inspect
    result = dspy.ChainOfThought("source, prompt -> kwargs_dict")(source=inspect.getsource(Rule), prompt=prompt).kwargs_dict

    print(result)
    import ast
    rdict = ast.literal_eval(result)
    model = Rule.model_validate(rdict)


if __name__ == '__main__':
    main()
