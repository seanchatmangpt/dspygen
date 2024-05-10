import random
import tqdm
from datasets import load_dataset
import dspy
from pydantic import BaseModel, Field
from typing import List, Optional


class JsonSchemaDescription(BaseModel):
    json_schema: str = Field(description="Schema of the module", alias='schema')
    key: str = Field(description="Key identifier")
    description: str = Field(description="Description of the module")
    object_data: str = Field(description="Object data in string format", alias='object')


class JsonSchemaDescriptionsDataset:
    def __init__(self, do_shuffle=True, shuffle_seed=0) -> None:
        super().__init__()
        # Load the dataset from the Hugging Face Hub
        dataset = load_dataset("dataunitylab/json-schema-descriptions", 'main')

        hf_train = dataset['train']
        train_set = []

        for example in tqdm.tqdm(hf_train):
            schema = example['schema']
            key = example['key']
            description = example['description']
            object_info = example['object']

            train_set.append(JsonSchemaDescription(schema=schema, key=key, description=description,
                                                   object_data=object_info).model_dump())

        # Optionally shuffle datasets
        if do_shuffle:
            rng = random.Random(shuffle_seed)
            rng.shuffle(train_set)

        # Split the data
        split_index = int(0.8 * len(train_set))
        self.train = [dspy.Example(**x).with_inputs('schema', 'classes', 'key', 'description', 'object_data') for x in
                      train_set[:split_index]]
        self.dev = [dspy.Example(**x).with_inputs('schema', 'classes', 'key', 'description', 'object_data') for x in
                    train_set[split_index:]]


def main():
    """Main function"""
    # Example instantiation and use:
    json_schema_descriptions_dataset = JsonSchemaDescriptionsDataset(do_shuffle=True, shuffle_seed=42)
    print(f"Trainset size: {len(json_schema_descriptions_dataset.train)}")
    print(f"Devset size: {len(json_schema_descriptions_dataset.dev)}")


if __name__ == '__main__':
    main()
