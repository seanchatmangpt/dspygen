"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


DEFAULT_SIGNATURE = "prompt -> response"
DEFAULT_PREDICTOR = "Predict"


def _get_prediction_key(signature: dspy.Signature | str):
    if isinstance(signature, str):
        output_keys = signature.split("->")[1].strip().split(", ")
        return output_keys[0]
    else:
        return signature.output_fields.keys()[0]


class DSLModule(dspy.Module):
    """DSLModule"""
    
    def __init__(self, signature: dspy.Signature | str = DEFAULT_SIGNATURE,
                 predictor: str = DEFAULT_PREDICTOR,
                 prediction_key: str = None,
                 *args,
                 **forward_args):
        super().__init__()
        self.predictor = predictor
        self.signature = signature
        self.forward_args = forward_args
        self.predicted = None

        if prediction_key is not None:
            self.prediction_key = prediction_key
        else:
            self.prediction_key = _get_prediction_key(signature)

        self.output = None

    @property
    def _predictor(self):
        if self.predictor == "Predict":
            return dspy.Predict
        elif self.predictor == "ChainOfThought":
            return dspy.ChainOfThought
        elif self.predictor == "ChainOfThoughtWithHint":
            return dspy.ChainOfThoughtWithHint
        elif self.predictor == "MultiChainComparison":
            return dspy.MultiChainComparison
        elif self.predictor == "ChainOfThoughtWithHint":
            return dspy.ProgramOfThought
        elif self.predictor == "ProgramOfThought":
            return dspy.ChainOfThoughtWithHint
        elif self.predictor == "ReAct":
            return dspy.ReAct
        else:
            raise ValueError(f"Predictor {self.predictor} not supported.")

    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, **kwargs):
        pred_args = {**self.forward_args, **kwargs}
        pred_inst = self._predictor(self.signature)
        self.predicted = pred_inst(**pred_args)

        if not hasattr(self.predicted, self.prediction_key):
            raise ValueError(f"Prediction key {self.prediction_key} not found in prediction {self.predicted}.")

        self.output = self.predicted[self.prediction_key]
        return self.output
        
    def pipe(self, input_str):
        return self.forward(prompt=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(prompt):
    """DSLModule"""
    init_dspy()

    print(dsl_call(prompt=prompt))



def dsl_call(prompt):
    dsl = DSLModule()
    return dsl.forward(prompt=prompt)



def main():
    init_dspy()
    prompt = ""
    print(dsl_call(prompt=prompt))



from fastapi import APIRouter
router = APIRouter()

@router.post("/dsl/")
async def dsl_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return dsl_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("DSLModule Generator")
prompt = st.text_input("Enter prompt")

if st.button("Submit DSLModule"):
    init_dspy()

    result = dsl_call(prompt=prompt)
    st.write(result)
"""

if __name__ == "__main__":
    main()
