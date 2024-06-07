"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class AudioToTextNarrativeModule(dspy.Module):
    """AudioToTextNarrativeModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, audio_descriptions):
        pred = dspy.Predict("audio_descriptions -> text_narratives")
        self.output = pred(audio_descriptions=audio_descriptions).text_narratives
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(audio_descriptions):
    """AudioToTextNarrativeModule"""
    init_dspy()

    print(audio_to_text_narrative_call(audio_descriptions=audio_descriptions))



def audio_to_text_narrative_call(audio_descriptions):
    audio_to_text_narrative = AudioToTextNarrativeModule()
    return audio_to_text_narrative.forward(audio_descriptions=audio_descriptions)



def main():
    init_dspy()
    audio_descriptions = ""
    result = audio_to_text_narrative_call(audio_descriptions=audio_descriptions)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/audio_to_text_narrative/")
async def audio_to_text_narrative_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return audio_to_text_narrative_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("AudioToTextNarrativeModule Generator")
audio_descriptions = st.text_input("Enter audio_descriptions")

if st.button("Submit AudioToTextNarrativeModule"):
    init_dspy()

    result = audio_to_text_narrative_call(audio_descriptions=audio_descriptions)
    st.write(result)
"""

if __name__ == "__main__":
    main()
