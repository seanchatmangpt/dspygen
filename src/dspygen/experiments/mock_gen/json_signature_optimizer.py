import dspy
from dspy.teleprompt import COPRO
from dspy.evaluate import Evaluate

from dspygen.experiments.mock_gen.text_to_json_data_set import TextToJSONDataset
from dspygen.utils.json_tools import extract


class TextToJSONSignature(dspy.Signature):
    """There should be only ```json, no other text outside of the ```json."""
    input = dspy.InputField(desc="Describe the scenario.")
    instruction = dspy.InputField(desc="Instructions for JSON formatting.")
    output = dspy.OutputField(desc="JSON formatted output.",
                              prefix="```json\n")


def custom_metric(example, pred):
    # Metric to compare predicted JSON to the actual JSON in the dataset

    out_d = extract(example.output.replace("'", '"'))
    pred_d = extract(pred.output.output)
    # print(out_d, pred_d)
    # print(out_d == pred_d)
    return pred_d is not None


class TextToJSONModule(dspy.Module):
    def __init__(self, signature=None):
        super().__init__()
        if signature is None:
            signature = TextToJSONSignature
        self.predictor = dspy.Predict(signature)  # Simulated predictor

    def forward(self, input, instruction):
        # Simulate prediction process
        prediction = self.predictor(input=input, instruction=instruction)
        return dspy.Prediction(output=prediction)


def main():
    from dspygen.utils.dspy_tools import init_ol
    init_ol(max_tokens=3000)
    # dspy.set_log_level('debug')
    # Initialize COPRO with a custom metric
    teleprompter = COPRO(metric=custom_metric, verbose=True, depth=2, breadth=2)

    dataset = TextToJSONDataset(do_shuffle=True, shuffle_seed=42)

    trainset, devset = dataset.train[:1], dataset.dev[:1]

    # Compile to optimize the signature
    kwargs = dict(num_threads=10, display_progress=True)
    optimized_signature = teleprompter.compile(TextToJSONModule(), trainset=trainset, eval_kwargs=kwargs)
    optimized_signature.save("optimized_signature.json")
    # Create a module with the optimized signature
    module = TextToJSONModule(optimized_signature)

    # Evaluate the module using the Evaluate class
    evaluator = Evaluate(devset=devset, metric=custom_metric, num_threads=10, display_progress=True)
    evaluation_results = evaluator(module)

    # Print evaluation results
    print(evaluation_results)


if __name__ == '__main__':
    main()
