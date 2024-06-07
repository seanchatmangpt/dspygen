"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class SpeechToTextCommandsModule(dspy.Module):
    """SpeechToTextCommandsModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, speech_audio):
        pred = dspy.Predict("speech_audio -> text_commands")
        self.output = pred(speech_audio=speech_audio).text_commands
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(speech_audio):
    """SpeechToTextCommandsModule"""
    init_dspy()

    print(speech_to_text_commands_call(speech_audio=speech_audio))



def speech_to_text_commands_call(speech_audio):
    speech_to_text_commands = SpeechToTextCommandsModule()
    return speech_to_text_commands.forward(speech_audio=speech_audio)



def main():
    init_dspy()
    speech_audio = ""
    result = speech_to_text_commands_call(speech_audio=speech_audio)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/speech_to_text_commands/")
async def speech_to_text_commands_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return speech_to_text_commands_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("SpeechToTextCommandsModule Generator")
speech_audio = st.text_input("Enter speech_audio")

if st.button("Submit SpeechToTextCommandsModule"):
    init_dspy()

    result = speech_to_text_commands_call(speech_audio=speech_audio)
    st.write(result)
"""

if __name__ == "__main__":
    main()
