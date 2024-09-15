from typing import Any, Type, List, Dict, Union, get_args, get_origin
from pydantic import BaseModel, Field, ValidationError
import dspy

# Define your Pydantic models
class Capability(BaseModel):
    name: str
    description: str

class Feature(BaseModel):
    name: str
    description: str
    acceptance_criteria: List[str]

class Epic(BaseModel):
    name: str
    description: str
    features: List[Feature]

class ProgramIncrement(BaseModel):
    name: str
    description: str
    epics: List[Epic]

class ValueStream(BaseModel):
    name: str
    description: str
    program_increments: List[ProgramIncrement]

class SAFePortfolio(BaseModel):
    name: str
    description: str
    value_streams: List[ValueStream]

# Initialize DSPy
lm = dspy.OpenAI(model='gpt-4', max_tokens=2000, temperature=0.7)
dspy.settings.configure(lm=lm)

def coerce_value(value: Any, field_type: Any) -> Any:
    """
    Coerce the value to the specified field type.
    """
    try:
        return field_type(value)
    except (TypeError, ValueError):
        if field_type is int:
            return int(float(value))
        elif field_type is float:
            return float(value)
        elif field_type is str:
            return str(value)
        elif field_type is bool:
            return bool(value)
        else:
            return value  # Return as is or handle accordingly

def process_field(value: Any, field_type: Any) -> Any:
    """
    Process a field value based on its type.
    """
    origin = get_origin(field_type)
    args = get_args(field_type)

    if isinstance(field_type, type) and issubclass(field_type, BaseModel):
        # Nested BaseModel
        return generate_model_instance(field_type)
    elif origin is list or origin is List:
        # List field
        item_type = args[0] if args else Any
        if not isinstance(value, list):
            value = [value]  # Ensure value is a list
        return [process_field(item, item_type) for item in value]
    elif origin is dict or origin is Dict:
        # Dictionary field
        key_type, val_type = args if args else (Any, Any)
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict for field, got {type(value)}")
        return {process_field(k, key_type): process_field(v, val_type) for k, v in value.items()}
    else:
        # Simple field
        return coerce_value(value, field_type)

def generate_model_instance(model_class: Type[BaseModel]) -> Any:
    """
    Recursively generate an instance of the given Pydantic model class.
    """
    # Create a dynamic signature based on the model's fields
    fields = model_class.model_fields
    field_descriptions = {}
    for name, field in fields.items():
        field_descriptions[name] = field.description or ""

    # Build the prompt for the LLM
    prompt = f"Generate data for the model '{model_class.__name__}' with the following fields:\n"
    for name, field in fields.items():
        constraints = []
        if isinstance(field.annotation, str):
            field_type = field.annotation
        else:
            field_type = field.annotation.__name__

        # Check for Field constraints
        if isinstance(field.default, Field):
            if field.default.min_length is not None:
                constraints.append(f"min_length={field.default.min_length}")
            if field.default.max_length is not None:
                constraints.append(f"max_length={field.default.max_length}")
            if field.default.gt is not None:
                constraints.append(f"gt={field.default.gt}")
            if field.default.ge is not None:
                constraints.append(f"ge={field.default.ge}")
            if field.default.lt is not None:
                constraints.append(f"lt={field.default.lt}")
            if field.default.le is not None:
                constraints.append(f"le={field.default.le}")

        constraint_str = f" ({', '.join(constraints)})" if constraints else ""
        prompt += f"- {name} ({field_type}{constraint_str}): {field_descriptions[name]}\n"

    # Define the Signature dynamically
    class DynamicSignature(dspy.Signature):
        """ """
        input: str = dspy.InputField(description="Instructions for data generation")
        output: Dict[str, Any] = dspy.OutputField(description="Generated data")

    predictor = dspy.TypedPredictor(DynamicSignature)

    # Use the LLM to generate data
    try:
        prediction = predictor(input=prompt)
        generated_data = prediction.output
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise

    # Process the generated data
    processed_data = {}
    for name, field in fields.items():
        value = generated_data.get(name)
        if value is None:
            continue  # Handle missing values as needed

        field_type = field.annotation
        processed_value = process_field(value, field_type)
        processed_data[name] = processed_value

    # Validate and create the model instance
    try:
        model_instance = model_class(**processed_data)
    except ValidationError as ve:
        print(f"Validation error: {ve}")
        raise

    return model_instance

def main():
    safe_portfolio = generate_model_instance(SAFePortfolio)
    print(safe_portfolio)
    with open("safe_portfolio.json", "w") as f:
        f.write(safe_portfolio.model_dump_json(indent=2))

if __name__ == "__main__":
    main()