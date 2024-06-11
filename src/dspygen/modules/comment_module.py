"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy        


import dspy

class GenerateViralComment(dspy.Signature):
    """
    Generate a viral comment for a YouTube video based on its title and relevant keywords.
    This Signature class leverages common strategies for creating engaging and shareable comments
    to maximize visibility and interaction. Includes relevant hashtags to boost discoverability.
    """
    vid_title = dspy.InputField(desc="Title of the YouTube video. This provides context and helps tailor the comment to the video's content.")
    words = dspy.InputField(desc="Relevant keywords or phrases to include in the comment. These should reflect popular and trending terms related to the video.")
    viral_comment = dspy.OutputField(desc="Generated comment designed to engage viewers and increase the likelihood of going viral. Includes relevant hashtags and emojis for discoverability.")




class CommentModule(dspy.Module):
    """CommentModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, vid_title, words):
        pred = dspy.Predict(GenerateViralComment)
        self.output = pred(vid_title=vid_title, words=words).viral_comment
        return self.output



from typer import Typer
app = Typer()


@app.command()
def call(vid_title, words):
    """CommentModule"""
    init_dspy()

    print(comment_call(vid_title=vid_title, words=words))



def comment_call(vid_title, words):
    comment = CommentModule()
    return comment.forward(vid_title=vid_title, words=words)



def main():
    init_dspy()
    vid_title = ""
    words = ""
    result = comment_call(vid_title=vid_title, words=words)
    print(result)



from fastapi import APIRouter
router = APIRouter()

@router.post("/comment/")
async def comment_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return comment_call(**data)


if __name__ == "__main__":
    main()
