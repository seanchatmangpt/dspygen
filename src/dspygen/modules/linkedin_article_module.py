"""
Source Code:
"""
"""
Simple Documentation: This is a source code for a Python module that generates LinkedIn articles based on a given source. It uses the dspy library and the Typer framework. The main function is the `linkedin_article_call` function, which takes in a source and returns a markdown LinkedIn article. There is also a `linkedin_article_route` function that can be used as an API endpoint to generate LinkedIn articles.
"""
import dspy
from typer import Typer
from dspygen.lm.groq_lm import Groq
from dspygen.lm.ollama_lm import Ollama

from dspygen.utils.dspy_tools import init_ol, init_dspy
from dspygen.writer import data_writer

app = Typer()


class LinkedInArticleGenerationSignature(dspy.Signature):
    """
    Transforms the source into a detailed markdown LinkedIn article worthy of the Harvard business review
    """

    source = dspy.InputField(desc="The main source material for the LinkedIn article.")

    markdown_linkedin_article = dspy.OutputField(desc="Generated LinkedIn article in markdown format.",
                                                 prefix="```markdown")


class LinkedInModule(dspy.Module):
    """LinkedInModule"""

    def __init__(self, *args, **kwargs):
        super().__init__()

    def forward(self, source):
        pred = dspy.ChainOfThought(LinkedInArticleGenerationSignature)
        result = pred(source=source).markdown_linkedin_article
        return result


def linkedin_article_call(source):
    linkedin_article = LinkedInModule()
    return linkedin_article.forward(source=source)


@app.command()
def call(source):
    """LinkedInModule"""
    init_dspy()

    print(linkedin_article_call(source=source))


# TODO: Add streamlit component

from fastapi import APIRouter

router = APIRouter()


@router.post("/linkedin/")
async def linkedin_article_route(data: dict):
    # Your code generation logic here
    init_dspy()

    print(data)
    return linkedin_article_call(**data)


def main():
    # init_dspy(lm_class=Groq, model="llama3-70b-8192", max_tokens=8000) # with Groq you must set the model!
    # init_ol("codellama:python", max_tokens=12000)
    init_ol("phi3:medium", max_tokens=5000, timeout=500)

    # init_dspy(Ollama, model="llama3:8b-instruct-q5_1", max_tokens=8000) # with Ollama you must set the model! -- llama3:70b-instruct ollama run llama3:70b-instruct-q3_K_M
    source = "The Tetris Game, simple but working: in 100 lines"  # 300 did not end ok with ollama mistral
    # ( pls do not run into those issues here: TypeError: unsupported operand type(s) for +=: 'int' and 'NoneType')"
    print(linkedin_article_call(source=source))
    # manually created the output to src\dspygen\experiments\blog\Tetris_1.md
    data_writer(data=source, file_path="./Tetris_LinkedIn_Phi3Med.md", )


if __name__ == "__main__":
    main()
