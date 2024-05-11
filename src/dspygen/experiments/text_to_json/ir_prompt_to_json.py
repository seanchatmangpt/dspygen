import dspy
from loguru import logger
import json

from dspygen.utils.json_tools import extract





class IntPromptToJSONModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.initial_validation_signature = IntermediateDataValidationSignature
        self.intermediate_validator = dspy.Predict(self.initial_validation_signature)
        # self.signature = PromptToJSONSignature
        # self.predictor = dspy.Predict(self.signature)
        # self.retry_predictor = dspy.Predict(JSONErrorRetrySignature)

    def forward(self, schema, prompt):
        # Perform initial normalization and validation
        # Convert the schema to a YAML string
        import yaml
        y_schema = yaml.dump(extract(schema))
        normalization_result = self.intermediate_validator(raw_input=prompt, schema_requirements=y_schema)
        # normalized_data = extract(normalization_result.normalized_data)
        # logger.info(f"Normalized Data:\n{normalization_result.normalized_data}")
        logger.info(f"Normalization Report:\n{normalization_result.normalization_report}")
        from dspygen.utils.file_tools import extract_code
        y_src = extract_code(normalization_result.normalization_report)
        y_inst = yaml.load(y_src, Loader=yaml.FullLoader)
        from jsonschema.validators import validate
        import json

        try:
            validate(instance=y_inst, schema=json.loads(schema))
        except Exception as ve:
            # Get the sub dictionary that failed validation
            # Get the key of the root of the dictionary
            key = list(y_inst.keys())[0]
            # Get the sub dictionary that failed validation
            y_inst = y_inst[key]
            logger.error(f"Validation Error: {ve.message}")

        # Continue with JSON construction
        return dspy.Prediction(
            completion=y_inst,
        )        # The rest of the implementation follows as previously described


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    from dspygen.experiments.text_to_json.json_mode_eval_dataset import JsonModeModel
    # example = JsonModeModel.model_validate({
    #     "prompt": "I am currently working on the inventory management system for our trading company within the Capital Goods sector, specifically under Trading Companies & Distributors. We need to automate the generation of purchase orders. Could you please assist me by generating a JSON object for a purchase order? The purchase order should include the orderID, orderDate, a list of items with each item containing a productID, quantity, and unitPrice, and the totalAmount for the order. Here are the details for a specific order: orderID is 'PO123456', orderDate is '2023-04-15', and the items list includes two items. The first item has a productID of 'PRD001', a quantity of 10, and a unitPrice of 29.99. The second item has a productID of 'PRD002', a quantity of 5, and a unitPrice of 49.99. The totalAmount for this order is 549.85. Please respond with a valid JSON object.",
    #     "schema": "{\"title\": \"PurchaseOrder\", \"type\": \"object\", \"properties\": {\"orderID\": {\"title\": \"Order ID\", \"type\": \"string\"}, \"orderDate\": {\"title\": \"Order Date\", \"type\": \"string\", \"format\": \"date\"}, \"items\": {\"title\": \"Items\", \"type\": \"array\", \"items\": {\"type\": \"object\", \"properties\": {\"productID\": {\"title\": \"Product ID\", \"type\": \"string\"}, \"quantity\": {\"title\": \"Quantity\", \"type\": \"integer\"}, \"unitPrice\": {\"title\": \"Unit Price\", \"type\": \"number\"}}, \"required\": [\"productID\", \"quantity\", \"unitPrice\"]}}, \"totalAmount\": {\"title\": \"Total Amount\", \"type\": \"number\"}}, \"required\": [\"orderID\", \"orderDate\", \"items\", \"totalAmount\"]}",
    #     "completion": "{\"orderID\": \"PO123456\", \"orderDate\": \"2023-04-15\", \"items\": [{\"productID\": \"PRD001\", \"quantity\": 10, \"unitPrice\": 29.99}, {\"productID\": \"PRD002\", \"quantity\": 5, \"unitPrice\": 49.99}], \"totalAmount\": 549.85}"
    # })

    # Load up the failed examples

    with open("gold_failed_examples.json", "r") as f:
        failed_examples = json.load(f)

    for example in failed_examples:
        # Implementation example with usage
        module = IntPromptToJSONModule()
        example = JsonModeModel(**example)

        result = module.forward(example.json_schema, example.prompt)

        logger.info(f"Completion:\n{result.completion}")
        logger.info(f"Expected completion:\n{example.completion}")

        if extract(example.completion) != result.completion:
            logger.error("The completion does not match the expected result.")
        else:
            logger.info("The completion matches the expected result.")


if __name__ == '__main__':
    main()
