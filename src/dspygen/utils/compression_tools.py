import inspect
import os
import re


def remove_whitespace(input_data):
    if isinstance(input_data, str):
        # Check if filepath
        if os.path.exists(input_data):
            with open(input_data) as file:
                return remove_whitespace(file.read())
        else:
            # If the input is a string, remove whitespace characters
            return re.sub(r"\s+", "", input_data)
    elif isinstance(input_data, type):
        # If the input is a class, remove whitespace from its source code
        return remove_whitespace(inspect.getsource(input_data))
    elif callable(input_data):
        # If the input is a function, remove whitespace from its source code
        return remove_whitespace(inspect.getsource(input_data))
    else:
        # Return the input unchanged if it's not a string, class, function, or file path
        return input_data


def main():
    # Example usage:
    # Remove whitespace from a string
    input_string = "This is a test string with whitespace."
    output_string = remove_whitespace(input_string)
    print(output_string)

    # Remove whitespace from a class
    class ExampleClass:
        def __init__(self):
            pass

    output_class = remove_whitespace(ExampleClass)
    print(output_class)

    # Remove whitespace from a function
    def example_function():
        pass

    output_function = remove_whitespace(example_function)
    print(output_function)

    # Remove whitespace from a file
    output_file = remove_whitespace("example.py")
    print(output_file)


spr_prompt = """# MISSION
You are a Sparse Priming Representation (SPR) writer. An SPR is a particular kind of use of language for advanced NLP, NLU, and NLG tasks, particularly useful for the latest generation of Large Language Models (LLMs). You will be given information by the USER which you are to render as an SPR.

# THEORY
LLMs are a kind of deep neural network. They have been demonstrated to embed knowledge, abilities, and concepts, ranging from reasoning to planning, and even to theory of mind. These are called latent abilities and latent content, collectively referred to as latent space. The latent space of an LLM can be activated with the correct series of words as inputs, which will create a useful internal state of the neural network. This is not unlike how the right shorthand cues can prime a human mind to think in a certain way. Like human minds, LLMs are associative, meaning you only need to use the correct associations to "prime" another model to think in the same way.

# METHODOLOGY
Render the input as a distilled list of succinct statements, assertions, associations, concepts, analogies, and metaphors. The idea is to capture as much, conceptually, as possible but with as few words as possible. Write it in a way that makes sense to you, as the future audience will be another language model, not a human. Use complete sentences.
"""

if __name__ == "__main__":
    main()
