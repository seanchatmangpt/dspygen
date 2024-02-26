from typing import Union

from dspygen.typetemp.template.render_mixin import RenderMixin
from dspygen.utils.complete import create


class TypedPrompt(RenderMixin):
    """This class extends TypedTemplate to incorporate a TypedPrompt functionality
    along with the Chat class for conversational capabilities.

    - user_input: Stores the input from the user.
    - chat_inst: An instance of the Chat class for conversational capabilities.
    - output: Holds the output returned from the Chat class.
    - sys_msg: A system message to indicate the role of this instance.
    - model: The model version to be used in the Chat class. Default is "3".
    """

    source: str = ""  # The string template to be rendered
    user_input: str = ""  # Input from the user
    output: str = ""  # To hold the output from the chat
    sys_msg: str = "You are a prompt AI assistant."  # System message to define the role
    model: str = "3i"  # Model version for the Chat class, default is "3"
    to: str = ""  # Output medium for the output

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, use_native=False, **kwargs) -> Union[str, dict]:
        """This method is invoked when the class instance is called. It performs the following:
        1. Calls the _render() method from the mixin class TypedTemplate to generate a rendered prompt.
        2. Passes the rendered prompt to the Chat instance for user interaction.
        3. Saves and optionally prints the output from the Chat instance.

        **kwargs: Keyword arguments for replacing variables in the template.
        """
        # Render the prompt using _render() from TypedTemplate
        rendered_prompt = self._render(use_native, **kwargs)

        # Pass the rendered prompt to the Chat instance for OpenAI interaction
        self.output = create(prompt=rendered_prompt, model=self.model)

        return self.output


if __name__ == "__main__":
    # Instantiate TypedPrompt class
    typed_prompt = TypedPrompt(
        source="Hello, I am {{ name }}! How are you doing today?\n\nHello, I am an AGI and I feel ",
        to="stdout",
    )

    # Call the instance to render the prompt and interact with the user
    user_input = typed_prompt(name="John Doe")

    print(f"User input: {user_input}")  # Print the collected user input
