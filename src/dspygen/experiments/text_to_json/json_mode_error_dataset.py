import json
import random
import dspy
from dspy.datasets.dataset import Dataset
from pydantic import BaseModel, Field

DEFAULT_PATH = "/Users/sac/dev/dspygen/src/dspygen/experiments/text_to_json/gold_failed_examples.json"


class JsonModeErrorModel(BaseModel):
    """A Pydantic model for handling JSON error data, with an added field for the prediction."""
    prompt: str = Field(..., description="The prompt for the JSON object.")
    json_schema: str = Field(..., alias='schema', description="The schema of the JSON object.")
    completion: str = Field(..., description="The correct gold completion of the JSON object.")
    prediction: str = Field(..., description="The prediction made by the model.")


class JsonModeErrorDataset(Dataset):
    def __init__(self, file_path=DEFAULT_PATH, *args, only_valid_schemas=True, keep_details=True, seed=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert only_valid_schemas, "Ensure all provided examples have valid schemas."

        # Load the dataset from a local JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        error_train = []
        for raw_example in data:
            if keep_details:
                keys = ['prompt', 'schema', 'completion', 'prediction']
            else:
                keys = ['prompt', 'completion', 'prediction']

            example_data = {k: raw_example[k] for k in keys if k in raw_example}

            example = dspy.Example(**example_data).with_inputs("prompt", "schema")  # Creating an Example object
            error_train.append(example)

        # Shuffle the data
        rng = random.Random(seed)
        rng.shuffle(error_train)

        # Split the data, with 75% for training and 25% for development
        # split_index = len(error_train) * 75 // 100
        self._train_ = error_train
        self._dev_ = error_train
        self._test_ = []  # Assuming no test set is available

def main():
    """Main function"""
    dataset_path = "/Users/sac/dev/dspygen/src/dspygen/experiments/text_to_json/gold_failed_examples_v2.json"
    dataset = JsonModeErrorDataset(dataset_path, train_seed=1)

    print(f"Train, Dev, Test sizes: {len(dataset.train)}, {len(dataset.dev)}, {len(dataset.test)}")

    if dataset.train:
        print(f"Train example: {dataset.train[0].prompt}, {dataset.train[0].completion}, {dataset.train[0].prediction}")

    if dataset.dev:
        print(f"Dev example: {dataset.dev[0].prompt}, {dataset.dev[0].completion}, {dataset.dev[0].prediction}")

if __name__ == '__main__':
    main()
