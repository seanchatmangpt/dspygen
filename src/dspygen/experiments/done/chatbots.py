from dspygen.modules.gen_keyword_arguments_module import invoke
from dspygen.utils.dspy_tools import init_dspy, init_ol

def chat(message: str):
    # Function to handle the chat logic
    print(f"Received message: {message}")
    return f"Response to: {message}"

def invoke_response(message: str):
    # Provide the prompt as a formatted string
    prompt = f"{message}\nbot:"
    print(f"Generated prompt: {prompt}")  # Debug statement to check prompt
    try:
        response = invoke(chat, prompt=prompt)
    except ValueError as e:
        print(f"Error while invoking: {e}")  # Catch and print the error
        raise
    return response

def main():
    response = invoke_response("bot: Hello world")
    print(response)

if __name__ == '__main__':
    init_ol()
    main()
