from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class BlogArticle(Signature):
    """
    Generate a blog article based on a celebrity and news.
    """

    celebrity = InputField(desc="The celebrity to base the article on.")
    news = InputField(desc="The news to include in the article.")

    blog_article = OutputField(desc="The generated blog article.")
