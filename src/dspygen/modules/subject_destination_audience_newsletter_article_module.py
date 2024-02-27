"""The source code is importing the necessary libraries and creating a Typer app. It also defines a class for a
module that takes in subject, destination, and audience as inputs and returns a newsletter article. The function
"subject_destination_audience_newsletter_article_call" calls this module and returns the result. The Typer app has a
command "call" that takes in subject, destination, and audience as arguments and prints the result of calling the
module. The main function initializes the Typer app and calls the
"subject_destination_audience_newsletter_article_call" function with empty inputs."""
import dspy
from typer import Typer
from dspygen.utils.dspy_tools import init_dspy


app = Typer()


class SubjectDestinationAudienceNewsletterArticleModule(dspy.Module):
    """SubjectDestinationAudienceNewsletterArticleModule"""

    def forward(self, subject, destination, audience):
        pred = dspy.Predict("subject, destination, audience -> newsletter_article")
        result = pred(
            subject=subject, destination=destination, audience=audience
        ).newsletter_article
        return result


def subject_destination_audience_newsletter_article_call(
    subject, destination, audience
):
    subject_destination_audience_newsletter_article = (
        SubjectDestinationAudienceNewsletterArticleModule()
    )
    return subject_destination_audience_newsletter_article.forward(
        subject=subject, destination=destination, audience=audience
    )


@app.command()
def call(subject, destination, audience):
    """SubjectDestinationAudienceNewsletterArticleModule"""
    init_dspy()

    print(
        subject_destination_audience_newsletter_article_call(
            subject=subject, destination=destination, audience=audience
        )
    )


def main():
    init_dspy(max_tokens=3000)
    subject = "Language Models in the year 2050"
    destination = "LinkedIn"
    audience = "Non technical people over the age of 60"
    print(
        subject_destination_audience_newsletter_article_call(
            subject=subject, destination=destination, audience=audience
        )
    )


if __name__ == "__main__":
    main()
