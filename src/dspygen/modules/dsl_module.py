"""

"""
import dspy

from dspygen.typetemp.functional import render
from dspygen.utils.dspy_tools import init_dspy


DEFAULT_SIGNATURE = "prompt -> response"
DEFAULT_PREDICTOR = "Predict"


def _get_prediction_key(signature: dspy.Signature | str):
    if isinstance(signature, str):
        output_keys = signature.split("->")[1].strip().split(", ")
        return output_keys[0]
    else:
        keys = signature.output_fields.items()
        # Get the key of the first output field
        return next(iter(keys))


class DSLModule(dspy.Module):
    def __init__(self, signature: dspy.Signature | str = DEFAULT_SIGNATURE,
                 predictor: str = DEFAULT_PREDICTOR,
                 context: dict = None,  # Context parameter
                 *additional_args, **kwargs):
        super().__init__()
        self.signature = signature
        self.predictor = predictor
        self.context = context if context is not None else {}
        self.output = None

        if not kwargs:
            kwargs = {}

        self.forward_args = {key: render(str(value), **self.context)
                             for key, value in kwargs.items()}

        print(f"Forward args: {self.forward_args}")

    def _get_predictor_class(self):
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
        # Ensure that any additional runtime arguments are merged with pre-resolved forward_args
        runtime_args = {**self.forward_args, **kwargs}

        # Dynamically resolve arguments right before execution
        resolved_args = {key: render(str(value), **self.context)
                         for key, value in runtime_args.items()}

        # Determine the appropriate predictor to use based on the self.predictor attribute
        pred_cls = self._get_predictor_class()
        pred_inst = pred_cls(self.signature)

        # Call the predictor with only the arguments it expects in the signature
        # This is a bit of a hack, but it's the best we can do without a proper signature system
        pred_args = {k: v for k, v in resolved_args.items() if k in pred_inst.signature.input_fields}

        # Execute the predictor with resolved arguments
        predicted = pred_inst(**pred_args)

        # Optionally, update the context with the new output
        # Assume self.predicted directly gives us the desired output for simplicity
        self.output = predicted

        self.context.update(predicted.items())

        return self.output

    def pipe(self, input_str):
        return self.forward(prompt=input_str)

    def __repr__(self):
        return f"DSLModule(predictor={self.predictor}, signature={self.signature})"


def dsl_call(**kwargs):
    dsl = DSLModule()
    return dsl.forward(**kwargs)


def main():
    init_dspy()
    kwargs = {}
    print(dsl_call(**kwargs))



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
