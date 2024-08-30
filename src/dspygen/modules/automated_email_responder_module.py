import dspy
import pandas as pd
import io
from dspygen.rm.doc_retriever import DocRetriever
from dspygen.utils.dspy_tools import init_dspy


class AutomatedEmailResponderSignature(dspy.Signature):
    """
    Generates a response to an email considering the LinkedIn profile.
    """
    linkedin_profile = dspy.InputField(desc="The LinkedIn profile in text format.")
    email_message = dspy.InputField(desc="The incoming email message.")
    response = dspy.OutputField(desc="Generated response to the email.")


class AutomatedEmailResponderModule(dspy.Module):
    """AutomatedEmailResponderModule for responding to emails considering LinkedIn profile"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args

    def forward(self, email_message, linkedin_profile):
        pred = dspy.ChainOfThought(AutomatedEmailResponderSignature)
        return pred(email_message=email_message, linkedin_profile=linkedin_profile).response


def automated_email_call(email_message, linkedin_profile):
    module = AutomatedEmailResponderModule()
    return module.forward(email_message=email_message, linkedin_profile=linkedin_profile)


def main():
    from dspygen.utils.dspy_tools import init_ol, init_dspy
    init_ol(model="mistral-nemo")
    # init_dspy()

    # Retrieve LinkedIn profile
    linkedin_profile = DocRetriever("/Users/sac/dev/dspygen/src/dspygen/experiments/pyautomator/linkedin_profile.md").forward()

    # Example email message
    email_message = "Hello, I saw your profile and I'm interested in discussing a potential job opportunity. Can we schedule a call?"

    response = automated_email_call(email_message, linkedin_profile)
    print("Generated Response:")
    print(response)


if __name__ == '__main__':
    main()
