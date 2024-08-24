"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class VideoStreamFeatureExtractorModule(dspy.Module):
    """VideoStreamFeatureExtractorModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, video_streams):
        pred = dspy.Predict("video_streams -> features")
        self.output = pred(video_streams=video_streams).features
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(video_streams):
    """VideoStreamFeatureExtractorModule"""
    init_dspy()

    print(video_stream_feature_extrinhabitant_call(video_streams=video_streams))



def video_stream_feature_extrinhabitant_call(video_streams):
    video_stream_feature_extractor = VideoStreamFeatureExtractorModule()
    return video_stream_feature_extrinhabitant.forward(video_streams=video_streams)



def main():
    init_dspy()
    video_streams = ""
    result = video_stream_feature_extrinhabitant_call(video_streams=video_streams)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/video_stream_feature_extractor/")
async def video_stream_feature_extrinhabitant_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return video_stream_feature_extrinhabitant_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("VideoStreamFeatureExtractorModule Generator")
video_streams = st.text_input("Enter video_streams")

if st.button("Submit VideoStreamFeatureExtractorModule"):
    init_dspy()

    result = video_stream_feature_extrinhabitant_call(video_streams=video_streams)
    st.write(result)
"""

if __name__ == "__main__":
    main()
