import dspy

from dspygen.dsl.dsl_pydantic_models import PipelineDSLModel
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


def _get_predictor_class(predictor):
    if predictor == "Predict":
        return dspy.Predict
    elif predictor == "ChainOfThought":
        return dspy.ChainOfThought
    elif predictor == "ChainOfThoughtWithHint":
        return dspy.ChainOfThoughtWithHint
    elif predictor == "MultiChainComparison":
        return dspy.MultiChainComparison
    elif predictor == "ProgramOfThought":
        return dspy.ProgramOfThought
    elif predictor == "ReAct":
        return dspy.ReAct
    else:
        raise ValueError(f"Predictor {predictor} not supported.")


class DSLPredictModule(dspy.Module):
    def __init__(self, pipeline: PipelineDSLModel, signature: dspy.Signature | str = DEFAULT_SIGNATURE,
                 predictor: str = DEFAULT_PREDICTOR,
                 *additional_args, **kwargs):
        super().__init__()
        self.pipeline = pipeline
        self.signature = signature
        self.predictor = predictor
        self.output = None

        if not kwargs:
            kwargs = {}

        self.forward_args = {key: render(str(value), **self.pipeline.context)
                             for key, value in kwargs.items()}

        input_field_names = self._extract_input_fields()

        for field in input_field_names:
            if field in self.pipeline.context:
                # Use render to possibly process/format context values if necessary
                self.forward_args[field] = render(str(self.pipeline.context[field]), **self.pipeline.context)

        # print(f"Forward args: {self.forward_args}")

    def _extract_input_fields(self):
        # Handle string signature
        if isinstance(self.signature, str):
            input_keys = self.signature.split("->")[0].strip().split(", ")
            return input_keys
        # Handle dspy.Signature object
        elif isinstance(self.signature, dspy.SignatureMeta):
            return list(self.signature.input_fields.keys())
        else:
            raise ValueError("Unsupported signature format")

    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, **kwargs):
        # Ensure that any additional runtime arguments are merged with pre-resolved forward_args
        runtime_args = {**self.forward_args, **kwargs}

        # Dynamically resolve arguments right before execution
        resolved_args = {key: render(str(value), **self.pipeline.context)
                         for key, value in runtime_args.items()}

        # Determine the appropriate predictor to use based on the self.predictor attribute
        pred_cls = _get_predictor_class(self.predictor)
        pred_inst = pred_cls(self.signature)

        # Call the predictor with only the arguments it expects in the signature
        pred_args = {k: v for k, v in resolved_args.items() if k in pred_inst.signature.input_fields}

        # Execute the predictor with resolved arguments
        predicted = pred_inst(**pred_args)

        # Optionally, update the context with the new output
        # Assume self.predicted directly gives us the desired output for simplicity
        self.output = predicted

        self.pipeline.context.update(predicted.items())

        print(f"Output:\n{self.output}")

        return self.output

    def validate_output(self, output):
        print(f"Assertions to run {self.pipeline.config.current_step.assertions}")
        # Implement validation logic or override in subclass
        raise NotImplementedError("Validation logic should be implemented in subclass")

    def pipe(self, input_str):
        return self.forward(prompt=input_str)

    def __repr__(self):
        return f"DSLModule(predictor={self.predictor}, signature={self.signature})"


def dsl_call(**kwargs):
    dsl = DSLPredictModule(pipeline=PipelineDSLModel(), **kwargs)
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
