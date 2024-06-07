"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class ChatbotResponseGeneratorModule(dspy.Module):
    """ChatbotResponseGeneratorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, user_input):
        pred = dspy.Predict("user_input -> chatbot_response")
        self.output = pred(user_input=user_input).chatbot_response
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(user_input):
    """ChatbotResponseGeneratorModule"""
    init_dspy()

    print(chatbot_response_generator_call(user_input=user_input))



def chatbot_response_generator_call(user_input):
    chatbot_response_generator = ChatbotResponseGeneratorModule()
    return chatbot_response_generator.forward(user_input=user_input)



def main():
    init_dspy()
    user_input = ""
    result = chatbot_response_generator_call(user_input=user_input)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/chatbot_response_generator/")
async def chatbot_response_generator_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return chatbot_response_generator_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("ChatbotResponseGeneratorModule Generator")
user_input = st.text_input("Enter user_input")

if st.button("Submit ChatbotResponseGeneratorModule"):
    init_dspy()

    result = chatbot_response_generator_call(user_input=user_input)
    st.write(result)
"""

if __name__ == "__main__":
    main()
