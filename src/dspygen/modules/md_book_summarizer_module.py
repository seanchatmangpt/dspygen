"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


import dspy


class MDBookSummarySignature(dspy.Signature):
    """
    [INST]
    Generate a properly formatted summary.md for MDBook from any length text.

    The output summary.md will include structured headings for chapters and links to the chapter files,
    adhering to MDBook's summary.md formatting guidelines.

    Example:
        # Summary

    [Introduction](README.md)

    # User Guide

    - [Installation](guide/installation.md)
    - [Reading Books](guide/reading.md)
    - [Creating a Book](guide/creating.md)

    # Reference Guide

    - [Command Line Tool](cli/README.md)
        - [init](cli/init.md)
        - [build](cli/build.md)
        - [watch](cli/watch.md)
        - [serve](cli/serve.md)
        - [test](cli/test.md)
        - [clean](cli/clean.md)
        - [completions](cli/completions.md)
    - [Format](format/README.md)
        - [SUMMARY.md](format/summary.md)
            - [Draft chapter]()
        - [Configuration](format/configuration/README.md)
            - [General](format/configuration/general.md)
            - [Preprocessors](format/configuration/preprocessors.md)
            - [Renderers](format/configuration/renderers.md)
            - [Environment Variables](format/configuration/environment-variables.md)
        - [Theme](format/theme/README.md)
            - [index.hbs](format/theme/index-hbs.md)
            - [Syntax highlighting](format/theme/syntax-highlighting.md)
            - [Editor](format/theme/editor.md)
        - [MathJax Support](format/mathjax.md)
        - [mdBook-specific features](format/mdbook.md)
        - [Markdown](format/markdown.md)
    - [Continuous Integration](continuous-integration.md)
    - [For Developers](for_developers/README.md)
        - [Preprocessors](for_developers/preprocessors.md)
        - [Alternative Backends](for_developers/backends.md)

    -----------

    [Contributors](misc/contributors.md)
    [/INST]
    """
    # Input: The text or Markdown content of the MDBook.
    mdbook_content = dspy.InputField(desc="Full text or Markdown content of the MDBook.")

    # Output: Properly formatted summary.md content.
    summary_md = dspy.OutputField(desc="Formatted summary.md content for MDBook, including headings and links to chapters. It is critical that it is formatted correctly for MDBook to recognize it per the Example.")


class MDBookSummarizerModule(dspy.Module):
    """MDBookSummarizerModule"""
    
    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, mdbook_content):
        pred = dspy.ChainOfThought(MDBookSummarySignature)
        self.output = pred(mdbook_content=mdbook_content).summary_md
        return self.output


def md_book_summarizer_call(any_length_text):
    md_book_summarizer = MDBookSummarizerModule()
    return md_book_summarizer.forward(any_length_text)


text = """Product Requirements Document (PRD): Summarizer Module
Document Owner
Name: [Product Director's Name]
Position: Product Director, BookGen Project
Contact: [Contact Information]
Document Version
Version: 1.0
Last Updated: [Date]
Overview
The Summarizer module aims to revolutionize how we process and digest long-form texts within the BookGen ecosystem. By leveraging state-of-the-art AI and NLP technologies, this module will automatically generate concise, meaningful summaries of texts of any length. These summaries will then be saved as .MD files, seamlessly integrating with the MDBook component of BookGen. This capability is especially critical for users looking to quickly create summaries for chapters or entire books, enhancing readability and accessibility.

Objective
To develop an AI-powered Summarizer module that can accurately and efficiently condense texts of varying lengths into summarized .MD files, supporting the broader objectives of the BookGen project by improving user experience and content management.

Scope
In Scope:
Integration with the BookGen ecosystem.
Processing texts retrieved by the DocRetriever module.
Generating summaries in Markdown format (.MD files).
Out of Scope:
Translating text between languages.
Full-text editing and content creation beyond summarization.
Requirements
Functional Requirements
Text Input Handling:
The module must accept text inputs of any length.
The input mechanism should be compatible with texts retrieved using the DocRetriever module.
Summary Generation:
The AI model must generate a summary that captures the core essence and key points of the original text.
The length of the summary should be configurable, with default settings provided.
Markdown Output:
The summary must be output as a Markdown (.MD) file, ensuring compatibility with MDBook.
The module should support custom Markdown templates for summary outputs.
Integration with BookGen:
The summarizer must seamlessly integrate with the existing BookGen CLI and web interface.
Users should be able to invoke the summarizer via command-line arguments or through the web interface.
Non-Functional Requirements
Performance:
The summarization process should not exceed [X seconds/minutes] for texts up to [Y] words to ensure a responsive user experience.
Scalability:
The module must efficiently handle increasing volumes of text without degradation in performance or accuracy.
Accuracy:
The summarization algorithm should maintain a high level of accuracy, ensuring the summary is representative of the original text.
Usability:
The interface for generating summaries, whether on CLI or web, must be intuitive and user-friendly.
Dependencies
AI and NLP Libraries: The development of the summarizer module will depend on third-party AI and NLP libraries for text processing and summary generation.
DocRetriever Module: Seamless integration with the DocRetriever for fetching and processing text documents.
Stakeholders
Development Team: Responsible for the design, development, and testing of the Summarizer module.
UI/UX Team: Ensures the module's features are accessible and efficiently integrated into the BookGen UI.
Quality Assurance: Validates the functionality, performance, and integration of the summarizer module.
End Users: The primary beneficiaries, including authors, educators, and content creators, providing feedback for continuous improvement.
Milestones
Research Phase: Completion Date - [MM/DD/YYYY]
Research and selection of AI/NLP libraries.
Development Phase: Completion Date - [MM/DD/YYYY]
Development of the summarizer module and integration testing with DocRetriever.
UI Integration: Completion Date - [MM/DD/YYYY]
Integration with the BookGen CLI and web interface.
Beta Testing: Completion Date - [MM/DD/YYYY]
Beta release to select users for feedback.
Launch: Completion Date - [MM/DD/YYYY]
Full release of the summarizer feature within the BookGen ecosystem.
Evaluation Criteria
User Feedback: Satisfaction with the accuracy and usefulness of the summaries.
Performance Metrics: Compliance with performance benchmarks for speed and scalability.
Usability Testing: Ease of use as determined by UI/UX testing and user reports.
This PRD sets the direction for the development of the Summarizer module, a critical enhancement aimed at bolstering the capabilities and appeal of the BookGen ecosystem."""


def main():

    from dspygen.lm.groq_lm import Groq
    # init_dspy(lm_class=Groq, model="llama3-8b-8192", max_tokens=1000)
    # init_dspy(lm_class=Groq, model="llama3-70b-8192", max_tokens=1000)
    init_dspy(lm_class=Groq, model="mixtral-8x7b-32768", max_tokens=1000)
    any_length_text = text
    print(md_book_summarizer_call(any_length_text))


if __name__ == "__main__":
    main()

