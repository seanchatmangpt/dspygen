from pydantic import BaseModel, ValidationError
import json

class DecisionInput(BaseModel):
    income: float
    credit_score: int
    loan_amount: float

class DecisionOutput(BaseModel):
    loan_approval: str
    maximum_loan_amount: float

class Decision(BaseModel):
    inputs: DecisionInput
    outputs: DecisionOutput

def populate_model(model: BaseModel, data: dict, depth=0):
    field_values = {}
    for field_name, field_type in model.__annotations__.items():
        if issubclass(field_type, BaseModel):
            # Recurse into submodels
            field_values[field_name] = populate_model(field_type, data.get(field_name, {}), depth+1)
        else:
            # Directly assign data if available
            field_values[field_name] = data.get(field_name)

    try:
        # Create model instance with populated data
        return model(**field_values)
    except ValidationError as ve:
        print(f"Validation error at depth {depth}: {ve}")
        return None

# Example usage
data = {
    "inputs": {"income": 5000.00, "credit_score": 720, "loan_amount": 15000},
    "outputs": {"loan_approval": "Approved", "maximum_loan_amount": 15000}
}

decision_model = populate_model(Decision, data)
print(decision_model)
