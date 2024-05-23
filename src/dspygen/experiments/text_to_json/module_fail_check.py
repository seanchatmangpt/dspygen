import json
import hashlib
import argparse
import os


def generate_hash_id(prompt):
    """Generate a unique hash for a given prompt."""
    hash_object = hashlib.sha256(prompt.encode('utf-8'))
    return hash_object.hexdigest()


def run_tests(json_dataset, module, compare_example_to_prediction, load_previous=True):
    failed_examples = {}
    successful_examples_file = "successful_examples.json"

    # Load previously successful examples if needed
    if load_previous and os.path.exists(successful_examples_file):
        with open(successful_examples_file, 'r') as file:
            successful_examples = set(json.load(file))
            print(f"Loaded {len(successful_examples)} previously successful example IDs.")
    else:
        successful_examples = set()

    # Function to process each example
    def process_example(example, dataset_type):
        example_id = generate_hash_id(example.prompt)

        # Skip processing if this example was previously successful
        if example_id in successful_examples:
            print(f"Skipping previously successful {dataset_type} example ID {example_id}")
            return

        pred = module(example.schema, example.prompt)
        result = compare_example_to_prediction(example, pred)

        if result:
            successful_examples.add(example_id)  # Update successful examples set
            print(f"Successfully processed {dataset_type} example ID {example_id}")
        else:
            if example_id not in failed_examples:
                failed_examples[example_id] = (example, pred)
                save_failed_examples(failed_examples)

        # Save successful examples to disk
        with open(successful_examples_file, 'w') as file:
            json.dump(list(successful_examples), file)
            json.dump(list(example.values()), file, indent=2, default=str)
            json.dump(list(pred), file, indent=2, default=str)


        # Print the progress
        total_examples = len(json_dataset.train) if dataset_type == 'train' else len(json_dataset.dev)
        print(f"{dataset_type.capitalize()}: {total_examples - len(failed_examples)} / {total_examples} correct")
        print(f"{dataset_type.capitalize()}: {100 * (total_examples - len(failed_examples)) / total_examples}% correct")

    # Process datasets
    for example in json_dataset.train:
        process_example(example, 'train')
    for example in json_dataset.dev:
        process_example(example, 'dev')


def save_failed_examples(failed_examples):
    """Save the failed examples to disk."""
    with open("gold_failed_examples.json", "w") as f:
        json.dump(list(failed_examples.values()), f, indent=2, default=str)


def main(load_previous):
    from dspygen.utils.dspy_tools import init_ol
    lm = init_ol(model="phi3:instruct", max_tokens=8000)

    from dspygen.experiments.text_to_json.json_mode_eval_dataset import JsonModeEvalDataset
    json_dataset = JsonModeEvalDataset(0)

    # Initialize the module
    from dspygen.modules.prompt_to_json_module import PromptToJSONModule
    module = PromptToJSONModule()
    # Assume json_dataset and module are defined somehow
    from dspygen.modules.prompt_to_json_module import compare_example_to_prediction
    run_tests(json_dataset, module, compare_example_to_prediction, load_previous)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run tests and skip previously successful examples if requested.")
    parser.add_argument("--load-previous", action='store_true',
                        help="Load previously successful examples from disk to skip.")
    args = parser.parse_args()
    main(args.load_previous)
