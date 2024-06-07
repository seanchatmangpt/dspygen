"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


class SocialMediaSentimentAnalyzerModule(dspy.Module):
    """SocialMediaSentimentAnalyzerModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None
        
    def __or__(self, other):
        if other.output is None and self.output is None:
            self.forward(**self.forward_args)

        other.pipe(self.output)

        return other

    def forward(self, social_media_posts):
        pred = dspy.Predict("social_media_posts -> sentiment_analysis")
        self.output = pred(social_media_posts=social_media_posts).sentiment_analysis
        return self.output
        
    def pipe(self, input_str):
        raise NotImplementedError("Please implement the pipe method for DSL support.")
        # Replace TODO with a keyword from you forward method
        # return self.forward(TODO=input_str)


from typer import Typer
app = Typer()


@app.command()
def call(social_media_posts):
    """SocialMediaSentimentAnalyzerModule"""
    init_dspy()

    print(social_media_sentiment_analyzer_call(social_media_posts=social_media_posts))



def social_media_sentiment_analyzer_call(social_media_posts):
    social_media_sentiment_analyzer = SocialMediaSentimentAnalyzerModule()
    return social_media_sentiment_analyzer.forward(social_media_posts=social_media_posts)



def main():
    init_dspy()
    social_media_posts = ""
    result = social_media_sentiment_analyzer_call(social_media_posts=social_media_posts)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/social_media_sentiment_analyzer/")
async def social_media_sentiment_analyzer_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return social_media_sentiment_analyzer_call(**data)



"""
import streamlit as st


# Streamlit form and display
st.title("SocialMediaSentimentAnalyzerModule Generator")
social_media_posts = st.text_input("Enter social_media_posts")

if st.button("Submit SocialMediaSentimentAnalyzerModule"):
    init_dspy()

    result = social_media_sentiment_analyzer_call(social_media_posts=social_media_posts)
    st.write(result)
"""

if __name__ == "__main__":
    main()
