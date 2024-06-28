from re import S
from pydantic import BaseModel, Field
from typing import Optional, List
import dspy

class SimplifiedJiraIssueFields(BaseModel):
    summary: str = Field(description="A brief summary of the Jira issue")
    description: Optional[str] = Field(
        description="Use this for the As a ... format. Do not use the 'user' or 'developer' come up with a different type ")
    issue_type: str = Field(description="The type of the Jira issue (e.g., Story, Bug)")
    components: Optional[List[str]] = Field(default_factory=list,
                                            description="Components associated with the Jira issue")
    due_date: Optional[str] = Field(description="Due date of the Jira issue in YYYY-MM-DD format", default=None)
    comments: Optional[List[str]] = Field(default_factory=list, description="Comments associated with the Jira issue")
    attachments: Optional[List[str]] = Field(default_factory=list,
                                             description="Attachments associated with the Jira issue")
    resolution: Optional[str] = Field(description="Resolution status of the Jira issue", default="Unresolved")

    def __repr__(self):
        return f"Summary: {self.summary}\n" \
               f"Description: {self.description}\n" \
               f"Issue Type: {self.issue_type}\n" \
               f"Components: {self.components}\n" \
               f"Due Date: {self.due_date}\n" \
               f"Comments: {self.comments}\n" \
               f"Attachments: {self.attachments}\n" \
               f"Resolution: {self.resolution}\n"

class SimplifiedJiraIssue(BaseModel):
    fields: SimplifiedJiraIssueFields


class UserStoryInput(BaseModel):
    summary: str = Field(description="A brief summary of the user story")
    description: str = Field(description="")


class MultipleUserStoryInput(BaseModel):
    summary: str = Field(description="A brief summary of the user story")
    description: str = Field(description="")
    count: int = Field(description="Number of new user stories to generate")


class UserStoryOutput(BaseModel):
    issue: SimplifiedJiraIssue = Field(description="The verbose Jira issue ready for insertion. FAANG PO QUALITY")


class MultipleUserStoryOutput(BaseModel):
    issues: List[SimplifiedJiraIssue] = Field(description="List of generated Jira issues")


# Define single story signature
class UserStorySignature(dspy.Signature):
    """Generate a Jira issue from user story input. Reply with verbose text for each field."""
    input: UserStoryInput = dspy.InputField()
    output: UserStoryOutput = dspy.OutputField()


# Define multiple story signature
class MultipleUserStorySignature(dspy.Signature):
    """Generate multiple Jira issues from a single user story input."""
    input: MultipleUserStoryInput = dspy.InputField()
    output: MultipleUserStoryOutput = dspy.OutputField()


# Create predictors
single_predictor = dspy.TypedPredictor(UserStorySignature)
multiple_predictor = dspy.TypedPredictor(MultipleUserStorySignature)



def create_single_user_story(user_story_input: UserStoryInput) -> SimplifiedJiraIssue:
    prediction = single_predictor(input=user_story_input)
    issue = prediction.output.issue

    print(issue)

    return issue


def create_multiple_user_stories(user_story_input: MultipleUserStoryInput) -> List[SimplifiedJiraIssue]:
    prediction = multiple_predictor(input=user_story_input)
    issues = prediction.output.issues

    for idx, issue in enumerate(issues, start=1):
        print(f"\nUser Story {idx}:")
        print(issue)

    from dspygen.writer.data_writer import DataWriter

    # Prepare data for CSV
    user_stories_data = []
    for issue in issues:
        user_stories_data.append({
            'Summary': issue.fields.summary,
            'Description': issue.fields.description,
            'Issue Type': issue.fields.issue_type,
            'Components': issue.fields.components,
            'Due Date': issue.fields.due_date,
            'Comments': issue.fields.comments,
            'Attachments': issue.fields.attachments,
            'Resolution': issue.fields.resolution
        })

    # Define the file path for the CSV
    csv_file_path = "user_stories.csv"

    # Write the data to the CSV
    data_writer = DataWriter(data=user_stories_data, file_path=csv_file_path)
    data_writer.forward()

    return issues


def main2():
    from dspygen.utils.dspy_tools import init_ol, init_dspy
    init_ol(timeout=30)

    # Example input for single user story
    user_story_input = UserStoryInput(
        summary="Authentication",
        description="I want to be able to authenticate to the system",
    )

    print("Creating single user story...")
    story = create_single_user_story(user_story_input)

    # Example input for multiple user stories
    multiple_user_story_input = MultipleUserStoryInput(
        summary=story.fields.summary,
        description=story.fields.description,
        count=5
    )

    print("\nCreating multiple user stories...")
    create_multiple_user_stories(multiple_user_story_input)


def main():
    from dspygen.utils.dspy_tools import init_ol, init_dspy
    init_ol(timeout=30)
    from dspygen.agents.coder_agent_v4 import CoderAgent
    from dspygen.rm.data_retriever import DataRetriever

    # Define the file path for the user stories data
    user_stories_file_path = "user_stories.csv"

    # Initialize the Data Retriever with the user stories file path
    data_retriever = DataRetriever(file_path=user_stories_file_path)

    # Use the Coder Agent to loop through the user stories
    for story in data_retriever.forward():
        # Initialize the Coder Agent
        coder_agent = CoderAgent(str(story))
        coder_agent.start_coding()


if __name__ == '__main__':
    main()
