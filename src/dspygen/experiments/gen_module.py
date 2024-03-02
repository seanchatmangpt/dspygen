import logging  # Import the logging module
from typing import Optional

from dspy import ChainOfThought, Module, OpenAI, settings

logger = logging.getLogger(__name__)  # Create a logger instance
logger.setLevel(
    logging.ERROR
)  # Set the logger's level to ERROR or the appropriate level


class GenModule(Module):
    def __init__(self, output_key, input_keys: Optional[list[str]] = None, lm=None):
        if input_keys is None:
            self.input_keys = ["prompt"]
        else:
            self.input_keys = input_keys

        super().__init__()

        self.output_key = output_key

        # Define the generation and correction queries based on generation_type
        self.signature = ", ".join(self.input_keys) + f" -> {self.output_key}"
        self.correction_signature = (
            ", ".join(self.input_keys) + f", error -> {self.output_key}"
        )

        # DSPy modules for generation and correction
        self.generate = ChainOfThought(self.signature)
        self.correct_generate = ChainOfThought(self.correction_signature)

    def forward(self, **kwargs):
        # Generate the output using provided inputs
        gen_result = self.generate(**kwargs)
        output = gen_result.get(self.output_key)

        # Try validating the output
        try:
            return self.validate_output(output)
        except (AssertionError, ValueError, TypeError) as error:
            logger.error(error)
            logger.error(output)
            # Correction attempt
            corrected_result = self.correct_generate(**kwargs, error=str(error))
            corrected_output = corrected_result.get(self.output_key)
            return self.validate_output(corrected_output)

    def validate_output(self, output):
        # Implement validation logic or override in subclass
        raise NotImplementedError("Validation logic should be implemented in subclass")
