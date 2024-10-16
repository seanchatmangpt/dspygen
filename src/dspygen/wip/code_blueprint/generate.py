# generate.py
import dsp
import random
from dspy import Module, Prediction
from dspy.predict.parameter import Parameter
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging

from sungen.utils.dspy_tools import init_dspy, init_ol


class Generate(Module, Parameter):
    """
    Generate class to handle text generation based on a prompt using dsp.settings.lm.
    """

    def __init__(self, prompt: str, **config):
        """
        Initializes the Generate module with a given prompt.

        Args:
            prompt (str): The prompt to send to the language model for generation.
            **config: Additional configuration parameters for the generation process.
        """
        self.stage = random.randbytes(8).hex()
        self.prompt = prompt
        self.config = config
        self.reset()

    def reset(self):
        """
        Resets the internal state of the Generate module.
        """
        self.lm = None
        self.traces = []
        self.train = []
        self.demos = []

    def dump_state(self) -> Dict[str, Any]:
        """
        Dumps the current state of the Generate module for persistence.

        Returns:
            dict: A dictionary representing the current state.
        """
        state_keys = ["lm", "traces", "train"]
        state = {k: getattr(self, k) for k in state_keys}

        state["demos"] = []
        for demo in self.demos:
            demo_copy = demo.copy()

            for field in demo_copy:
                if isinstance(demo_copy[field], BaseModel):
                    demo_copy[field] = demo_copy[field].json()

            state["demos"].append(demo_copy)

        # Cache the prompt
        state["prompt"] = self.prompt

        # Cache the configuration
        state["config"] = self.config

        return state

    def load_state(self, state: Dict[str, Any]):
        """
        Loads the state into the Generate module.

        Args:
            state (dict): The state dictionary to load.
        """
        for name, value in state.items():
            setattr(self, name, value)

        # If there are any additional attributes or complex objects, handle their reconstruction here
        # For example, if you have a signature or extended_signature, reconstruct them similarly
        # This example assumes no such attributes for simplicity

    def __call__(self, **kwargs) -> Prediction:
        """
        Allows the instance to be called directly with keyword arguments.

        Args:
            **kwargs: Additional keyword arguments for generation.

        Returns:
            Prediction: The prediction result from the language model.
        """
        return self.forward(**kwargs)

    def forward(self, **kwargs) -> Prediction:
        """
        Executes the generation process.

        Args:
            **kwargs: Additional keyword arguments that may override or extend the configuration.

        Returns:
            Prediction: The prediction result containing the generated text.
        """
        assert not dsp.settings.compiling, "It's no longer ever the case that .compiling is True"

        # Extract additional configurations if provided
        config = dict(**self.config, **kwargs.pop("config", {}))

        # Get the language model to use
        lm = kwargs.pop("lm", self.lm) or dsp.settings.lm
        assert lm is not None, "No LM is loaded."

        # Merge any additional configuration parameters
        # For example, temperature, max_tokens, etc.
        temperature = config.get('temperature', lm.kwargs.get('temperature', 0.7))
        config['temperature'] = temperature

        # Prepare the prompt
        prompt = self.prompt

        # Execute the generation using the language model
        try:
            completions = self.generate_text(lm, prompt, **config)
        except Exception as e:
            logging.error(f"Generation failed: {e}")
            raise

        # Create a Prediction object from the completions
        prediction = Prediction.from_completions(completions)

        # Handle tracing if enabled
        if kwargs.pop("_trace", True) and dsp.settings.trace is not None:
            trace = dsp.settings.trace
            trace.append((self, {**kwargs}, prediction))

        return prediction

    def generate_text(self, lm, prompt: str, **config) -> List[Dict[str, Any]]:
        """
        Generates text using the language model.

        Args:
            lm: The language model instance to use for generation.
            prompt (str): The prompt string to generate text from.
            **config: Additional configuration parameters for generation.

        Returns:
            list: A list of generated completions.
        """
        if dsp.settings.experimental:
            completions = self.new_generate(lm, prompt, **config)
        else:
            completions = self.old_generate(prompt, config, lm, self.stage)

        return completions

    def old_generate(self, prompt: str, config: Dict[str, Any], lm, stage: str) -> List[Dict[str, Any]]:
        """
        Legacy generation method using the old generate function.

        Args:
            prompt (str): The prompt string to generate text from.
            config (dict): Configuration parameters.
            lm: The language model instance.
            stage (str): A unique identifier for the generation stage.

        Returns:
            list: A list of generated completions.
        """
        # Switch to legacy format for dsp.generate
        # Since dsp.generate is not implemented, we'll mock this
        # Replace this with your actual dsp.generate logic
        example = dsp.Example(prompt=prompt)
        template = "GENERATE: " + prompt  # Adjust based on actual template requirements

        if lm is None:
            # Assuming dsp.generate(template, **config)(example, stage=stage) returns (x, C)
            # where C is a list of completions
            x, C = dsp.generate(template, **config)(example, stage=stage)
        else:
            # Note: query_only=True means the instructions and examples are not included.
            with dsp.settings.context(lm=lm, query_only=True):
                x, C = dsp.generate(template, **config)(example, stage=stage)

        # Process completions
        completions = []
        for c in C:
            completions.append({})
            completions[-1]['text'] = getattr(c, 'text', '')

        return completions

    def new_generate(self, lm, prompt: str, max_depth=6, **kwargs) -> List[Dict[str, Any]]:
        """
        New generation method using the updated generate function.

        Args:
            lm: The language model instance to use for generation.
            prompt (str): The prompt string to generate text from.
            max_depth (int): The maximum recursion depth for generation.
            **kwargs: Additional configuration parameters for generation.

        Returns:
            list: A list of generated completions.
        """
        kwargs['stop'] = tuple(kwargs.get('stop', [])) or ('\n---',)

        response = lm(prompt, **kwargs)

        # Handle OpenAI-like responses
        if hasattr(response, 'choices') and isinstance(response.choices, list):
            completions = [{'text': choice.get('text', '').strip()} for choice in response.choices]
        elif isinstance(response, list) and all(isinstance(c, dict) for c in response):
            completions = [
                {'text': c.get('text', '') or c.get('text', '')}
                for c in response
            ]
        elif isinstance(response, list) and all(isinstance(c, str) for c in response):
            completions = [{'text': c} for c in response]
        else:
            raise ValueError("Language model returned an unexpected format for completions.")

        return completions

    def update_config(self, **kwargs):
        """
        Updates the configuration parameters.

        Args:
            **kwargs: Configuration parameters to update.
        """
        self.config = {**self.config, **kwargs}

    def get_config(self) -> Dict[str, Any]:
        """
        Retrieves the current configuration.

        Returns:
            dict: The current configuration parameters.
        """
        return self.config

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(prompt='{self.prompt}')"


# ============================
# Main Function for Testing
# ============================

def main():
    """
    Main function to test the Generate class.
    """
    init_ol()

    # Define your prompt
    prompt_text = "Elixir that uses GenServer to write ping module. Return perfect elixir only\n\n```elixir"

    # Create an instance of Generate
    generator = Generate(prompt=prompt_text, temperature=0.0, max_tokens=150)

    # Execute the generation
    try:
        prediction = generator()
        text = prediction.text  # Access the generated text
        print("Generated Text:")
        print(text)
    except Exception as e:
        print(f"Generation failed: {e}")

    # Optionally, inspect the trace
    if dsp.settings.trace:
        print("\nTrace:")
        for trace_entry in dsp.settings.trace:
            module, kwargs, prediction = trace_entry
            print(f"Module: {module}, Kwargs: {kwargs}, Prediction: {prediction}")


if __name__ == "__main__":
    main()
