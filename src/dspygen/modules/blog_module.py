"""
Source Code: """ """ 
Simple Documentation: This is a source code for a Python module that generates blog articles based on a given subject. It uses the dspy library and the Typer framework. The main function is the `blog_call` function, which takes in a subject and returns a markdown blog article. There is also a `blog_route` function that can be used as an API endpoint to generate blog articles.
"""
import dspy
from typer import Typer
from dspygen.lm.groq_lm import Groq
from dspygen.lm.ollama_lm import Ollama

from dspygen.utils.dspy_tools import init_dspy
from dspygen.writer import data_writer


app = Typer()


class BlogArticleGenerationSignature(dspy.Signature):
    """
    Transforms a given subject into a detailed markdown blog article.
    """

    subject = dspy.InputField(desc="The main subject or topic for the blog article.")

    markdown_blog_article = dspy.OutputField(desc="Generated blog article in markdown format.", prefix="```markdown")


class BlogModule(dspy.Module):
    """BlogModule"""
    def __init__(self, *args, **kwargs):
        super().__init__()

    def forward(self, subject):
        pred = dspy.ChainOfThought(BlogArticleGenerationSignature)
        result = pred(subject=subject).markdown_blog_article
        return result


def blog_call(subject):
    blog = BlogModule()
    return blog.forward(subject=subject)


@app.command()
def call(subject):
    """BlogModule"""
    init_dspy()
    
    print(blog_call(subject=subject))


# TODO: Add streamlit component


from fastapi import APIRouter
router = APIRouter()

@router.post("/blog/")
async def blog_route(data: dict):
    # Your code generation logic here
    init_dspy()
    
    print(data)
    return blog_call(**data)


def main():
    #init_dspy(Groq, model="llama3-70b-8192", max_tokens=8000) # with Groq you must set the model!
    init_dspy(Ollama, model="llama3:8b-instruct-q5_1", max_tokens=8000) # with Ollama you must set the model! -- llama3:70b-instruct ollama run llama3:70b-instruct-q3_K_M
    subject = "The Tetris Game, simple but working : in 100 lines" # 300 did not end ok with ollama mistral
    #( pls do not run into those issues here: TypeError: unsupported operand type(s) for +=: 'int' and 'NoneType')"
    print(blog_call(subject=subject))
    # manually created the output to src\dspygen\experiments\blog\Tetris_1.md
    #data_writer(data=subject, file_path="Tetris_File.py",)
    

if __name__ == "__main__":
    main()
