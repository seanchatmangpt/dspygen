import random

import dspy
from datasets import load_dataset
from dspy.datasets.dataset import Dataset


class JsonModeEvalDataset(Dataset):
    def __init__(self, *args, only_valid_schemas=True, keep_details=True, unofficial_dev=True, seed=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert only_valid_schemas, "Care must be taken when adding support for examples with invalid schemas."

        # Load the dataset
        hf_official_train = load_dataset("NousResearch/json-mode-eval", split='train')

        official_train = []
        for raw_example in hf_official_train:
            if keep_details:
                keys = ['prompt', 'schema', 'completion']
            else:
                keys = ['prompt', 'completion']

            example_data = {k: raw_example[k] for k in keys}
            example_data['prompt'] = str(example_data['prompt'])
            example = dspy.Example(**example_data).with_inputs("prompt", "schema")  # Creating an Example object
            official_train.append(example)

        rng = random.Random(seed)
        rng.shuffle(official_train)

        self._train_ = official_train[:len(official_train) * 75 // 100]

        if unofficial_dev:
            self._dev_ = official_train[len(official_train) * 75 // 100:]
        else:
            self._dev_ = []

        # Assuming no official test set provided in the dataset for consistency with the HotPotQA class
        self._test_ = []

def main():
    """Main function"""
    from dsp.utils import dotdict

    data_args = dotdict(train_seed=1, train_size=16, eval_seed=2023, dev_size=200 * 5, test_size=0)
    dataset = JsonModeEvalDataset(**data_args)

    print(dataset)
    print(dataset.train[0].prompt, dataset.train[0].completion)
    print(len(dataset.train), len(dataset.dev), len(dataset.test))

    if dataset.dev:
        print(dataset.dev[0].prompt, dataset.dev[0].completion)


if __name__ == '__main__':
    main()
