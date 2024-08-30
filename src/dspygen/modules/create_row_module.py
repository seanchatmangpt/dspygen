import dspy
from dspygen.utils.dspy_tools import init_dspy
import logging
import json
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_to_serializable(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64,
                        np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

class CreateRowSignature(dspy.Signature):
    """
    Creates a new row for a list of dictionaries based on a natural language request.
    """
    data_sample = dspy.InputField(desc="The entire existing dataset to understand the structure.")
    schema = dspy.InputField(desc="The schema of the data, including column names and types.")
    request = dspy.InputField(desc="Natural language request to add a new row.")
    new_row = dspy.OutputField(desc="A JSON string representing the new row to be added.")

class CreateRowModule(dspy.Module):
    """CreateRowModule for adding a new row to a list of dictionaries based on a natural language request"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args

    def forward(self, data, request):
        if not data:
            raise ValueError("Input data is empty.")

        # Convert list of dictionaries to DataFrame
        df = pd.DataFrame(data)

        # Use the entire dataset as a sample
        data_sample = df.to_json(orient='records')
        
        # Create schema information
        schema = {col: str(dtype) for col, dtype in df.dtypes.items()}

        pred = dspy.Predict(CreateRowSignature)
        new_row_str = pred(data_sample=data_sample, schema=json.dumps(schema), request=request).new_row

        # Parse the new_row string into a dictionary
        try:
            new_row = json.loads(new_row_str)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse new_row as JSON. Ensure the model outputs valid JSON.")

        # Ensure all columns from the DataFrame are present in the new row
        for col in df.columns:
            if col not in new_row:
                new_row[col] = None
            else:
                # Convert the value to the same type as in the DataFrame
                new_row[col] = df[col].dtype.type(new_row[col])
                # Convert to serializable type
                new_row[col] = convert_to_serializable(new_row[col])

        # Add the new row to the data
        updated_data = data + [new_row]

        return updated_data

def create_row_call(data, request):
    try:
        create_row_module = CreateRowModule()
        return create_row_module.forward(data=data, request=request)
    except Exception as e:
        logger.error(f"Error in create_row_call: {e}")
        raise

def main():
    init_dspy()
    # Example usage
    data = [
        {'name': 'Alice', 'age': 25, 'city': 'New York', 'joined_date': '2023-01-01'},
        {'name': 'Bob', 'age': 30, 'city': 'San Francisco', 'joined_date': '2023-02-01'}
    ]
    request = "Add a new person named Charlie, who is 35 years old, lives in London, and joined on March 1, 2023"
    
    try:
        result_data = create_row_call(data=data, request=request)
        print(json.dumps(result_data, indent=2))
        pd.DataFrame(result_data).to_csv("results.csv", index=False)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
