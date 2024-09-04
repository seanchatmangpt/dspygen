import pytest
import os
from unittest.mock import patch, MagicMock
from dspygen.subcommands.wkf_cmd import run_workflows_in_directory, app
from dspygen.pyautomator.linkedin.linkedin_app import LinkedInApp
from dspygen.modules.automated_email_responder_module import AutomatedEmailResponderModule
from typer.testing import CliRunner

@pytest.fixture
def mock_linkedin_app():
    return MagicMock(spec=LinkedInApp)

@pytest.fixture
def mock_email_responder():
    return MagicMock(spec=AutomatedEmailResponderModule)

@pytest.fixture
def sample_workflow_yaml(tmp_path):
    workflow_content = """
    name: email_responder_workflow
    schedule: "*/30 * * * *"
    tasks:
      - name: fetch_linkedin_profile
        module: LinkedInApp
        method: get_profile_markdown
        args:
          profile_url: "https://www.linkedin.com/in/example"
          output_file: "profile.md"
      - name: respond_to_email
        module: AutomatedEmailResponderModule
        method: forward
        args:
          email_message: "Hello, I'd like to discuss a job opportunity."
          linkedin_profile: "{{tasks.fetch_linkedin_profile.output}}"
    """
    workflow_file = tmp_path / "email_responder_workflow.yaml"
    workflow_file.write_text(workflow_content)
    return str(workflow_file)

def test_integration_workflow_execution(sample_workflow_yaml, mock_linkedin_app, mock_email_responder):
    with patch('dspygen.subcommands.wkf_cmd.Workflow.from_yaml') as mock_from_yaml, \
         patch('dspygen.subcommands.wkf_cmd.execute_workflow') as mock_execute, \
         patch('dspygen.pyautomator.linkedin.linkedin_app.LinkedInApp', return_value=mock_linkedin_app), \
         patch('dspygen.dspy_modules.automated_email_responder_module.AutomatedEmailResponderModule', return_value=mock_email_responder):

        # Set up mock returns
        mock_linkedin_app.get_profile_markdown.return_value = "Mocked LinkedIn Profile"
        mock_email_responder.forward.return_value = "Mocked Email Response"

        # Run the workflow
        scheduler = run_workflows_in_directory(os.path.dirname(sample_workflow_yaml))
        
        # Assert that the scheduler was created and has one job
        assert scheduler is not None
        assert len(scheduler.get_jobs()) == 1

        # Trigger the job execution
        job = scheduler.get_jobs()[0]
        job.func()

        # Verify that the LinkedIn profile was fetched
        mock_linkedin_app.get_profile_markdown.assert_called_once_with(
            profile_url="https://www.linkedin.com/in/example",
            output_file="profile.md"
        )

        # Verify that the email responder was called with the correct arguments
        mock_email_responder.forward.assert_called_once_with(
            email_message="Hello, I'd like to discuss a job opportunity.",
            linkedin_profile="Mocked LinkedIn Profile"
        )

def test_integration_cli_trigger(sample_workflow_yaml, mock_linkedin_app, mock_email_responder):
    runner = CliRunner()
    
    with patch('dspygen.subcommands.wkf_cmd.Workflow.from_yaml') as mock_from_yaml, \
         patch('dspygen.subcommands.wkf_cmd.execute_workflow') as mock_execute, \
         patch('dspygen.pyautomator.linkedin.linkedin_app.LinkedInApp', return_value=mock_linkedin_app), \
         patch('dspygen.dspy_modules.automated_email_responder_module.AutomatedEmailResponderModule', return_value=mock_email_responder):

        # Set up mock returns
        mock_linkedin_app.get_profile_markdown.return_value = "Mocked LinkedIn Profile"
        mock_email_responder.forward.return_value = "Mocked Email Response"

        # Trigger the workflow using the CLI
        result = runner.invoke(app, ["trigger", os.path.basename(sample_workflow_yaml)[:-5]])
        
        assert result.exit_code == 0
        assert "Workflow email_responder_workflow triggered" in result.output

        # Verify that the LinkedIn profile was fetched
        mock_linkedin_app.get_profile_markdown.assert_called_once()

        # Verify that the email responder was called
        mock_email_responder.forward.assert_called_once()

def test_integration_error_handling(sample_workflow_yaml, mock_linkedin_app, mock_email_responder):
    with patch('dspygen.subcommands.wkf_cmd.Workflow.from_yaml') as mock_from_yaml, \
         patch('dspygen.subcommands.wkf_cmd.execute_workflow') as mock_execute, \
         patch('dspygen.pyautomator.linkedin.linkedin_app.LinkedInApp', return_value=mock_linkedin_app), \
         patch('dspygen.dspy_modules.automated_email_responder_module.AutomatedEmailResponderModule', return_value=mock_email_responder):

        # Simulate an error in LinkedIn profile fetching
        mock_linkedin_app.get_profile_markdown.side_effect = Exception("Network error")

        # Run the workflow
        scheduler = run_workflows_in_directory(os.path.dirname(sample_workflow_yaml))
        
        # Trigger the job execution
        job = scheduler.get_jobs()[0]
        job.func()

        # Verify that the LinkedIn profile fetch was attempted
        mock_linkedin_app.get_profile_markdown.assert_called_once()

        # Verify that the email responder was not called due to the error
        mock_email_responder.forward.assert_not_called()

        # You might want to add assertions here to check if the error was logged or handled appropriately

if __name__ == "__main__":
    pytest.main()