import random
import tqdm
from datasets import load_dataset
import dspy

from pydantic import BaseModel, Field
from typing import List, Optional
import json


class TextToJSONData(BaseModel):
    input: str = Field(description="Text input describing the condition or scenario.")
    output: str = Field(description="JSON formatted output representing the condition or scenario.")
    instruction: str = Field(description="Instruction provided to guide the JSON conversion process.")

class TextToJSONDataset:
    def __init__(self, do_shuffle=True, shuffle_seed=0) -> None:
        super().__init__()

        # Load the dataset from the Hugging Face Hub
        dataset = load_dataset("azizshaw/text_to_json", 'default')

        hf_train = dataset['train']
        train_set = []

        for example in tqdm.tqdm(hf_train):
            input_text = example['input']
            output_json = example['output']
            instruction = example['instruction']

            train_set.append(dict(input=input_text, output=output_json, instruction=instruction))

        # Optionally shuffle datasets
        if do_shuffle:
            rng = random.Random(shuffle_seed)
            rng.shuffle(train_set)

        # Split the data
        split_index = int(0.8 * len(train_set))
        self.train = [dspy.Example(**x).with_inputs('input', 'instruction') for x in train_set[:split_index]]
        self.dev = [dspy.Example(**x).with_inputs('input', 'instruction') for x in train_set[split_index:]]

def main():
    """Main function"""
    # Example instantiation and use:
    text_to_json_dataset = TextToJSONDataset(do_shuffle=True, shuffle_seed=42)
    print(f"Trainset size: {len(text_to_json_dataset.train)}")
    print(f"Devset size: {len(text_to_json_dataset.dev)}")

if __name__ == '__main__':
    main()
