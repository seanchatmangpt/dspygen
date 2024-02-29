from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class JSToFastAPISig(Signature):
    """
    This task will use the js_source as the input field and the fast_api_source as the output field.
    """
    js_source = InputField(desc="The JavaScript source code to be converted into a FastAPI source code.")

    fast_api_source = OutputField(desc="The generated FastAPI source code.")
    