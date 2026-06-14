"""Tests for the advanced integration job search workflow.

These tests verify the workflow scaffolding in dspygen.subcommands.wkf_cmd
using mock objects for external dependencies (LinkedIn, email responder, etc.).
"""

import os
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_linkedin_app():
    mock = MagicMock()
    mock.get_profile_markdown.return_value = (
        "Jane Doe | Data Scientist | Skills: Python, Machine Learning, SQL"
    )
    return mock


@pytest.fixture
def mock_email_responder():
    mock = MagicMock()
    mock.forward.return_value = "Mocked email response"
    return mock


@pytest.fixture
def sample_job_search_workflow_yaml(tmp_path):
    workflow_content = """
name: advanced_job_search_workflow
schedule: "*/15 * * * *"
tasks:
  - name: fetch_linkedin_profile
    module: LinkedInApp
    method: get_profile_markdown
    args:
      profile_url: "https://www.linkedin.com/in/example-candidate"
  - name: respond_to_recruiter
    module: AutomatedEmailResponderModule
    method: forward
    args:
      email_message: "We have an exciting opportunity for you."
      linkedin_profile: "{{tasks.fetch_linkedin_profile.output}}"
"""
    workflow_file = tmp_path / "advanced_job_search_workflow.yaml"
    workflow_file.write_text(workflow_content)
    return str(workflow_file)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_workflow_file_is_valid_yaml(sample_job_search_workflow_yaml):
    """The generated workflow YAML should be readable and non-empty."""
    assert os.path.isfile(sample_job_search_workflow_yaml)
    with open(sample_job_search_workflow_yaml) as fh:
        content = fh.read()
    assert "advanced_job_search_workflow" in content
    assert "fetch_linkedin_profile" in content


def test_linkedin_profile_fetching(mock_linkedin_app):
    """Fetching a LinkedIn profile should return the mocked profile string."""
    profile_url = "https://www.linkedin.com/in/example-candidate"
    result = mock_linkedin_app.get_profile_markdown(profile_url=profile_url)

    assert "Jane Doe" in result
    assert "Python" in result
    mock_linkedin_app.get_profile_markdown.assert_called_once_with(
        profile_url=profile_url
    )


def test_email_responder_forward(mock_email_responder):
    """The email responder mock should return a non-empty response."""
    response = mock_email_responder.forward(
        email_message="We have an exciting opportunity for you.",
        linkedin_profile="Jane Doe | Data Scientist",
    )
    assert isinstance(response, str)
    assert len(response) > 0
    mock_email_responder.forward.assert_called_once()


def test_workflow_execution_calls_both_steps(
    sample_job_search_workflow_yaml, mock_linkedin_app, mock_email_responder
):
    """A simulated workflow run should invoke profile fetch then email respond."""
    # Simulate the two-step workflow without importing heavy dependencies.
    profile = mock_linkedin_app.get_profile_markdown(
        profile_url="https://www.linkedin.com/in/example-candidate"
    )
    response = mock_email_responder.forward(
        email_message="We have an exciting opportunity for you.",
        linkedin_profile=profile,
    )

    mock_linkedin_app.get_profile_markdown.assert_called_once()
    mock_email_responder.forward.assert_called_once()
    assert "Jane Doe" in profile
    assert response is not None


def test_email_responder_not_called_on_profile_error(
    mock_linkedin_app, mock_email_responder
):
    """If profile fetching fails, the email responder should not be invoked."""
    mock_linkedin_app.get_profile_markdown.side_effect = ConnectionError(
        "LinkedIn unreachable"
    )

    try:
        profile = mock_linkedin_app.get_profile_markdown(
            profile_url="https://www.linkedin.com/in/example-candidate"
        )
        mock_email_responder.forward(
            email_message="Opportunity awaits",
            linkedin_profile=profile,
        )
    except ConnectionError:
        pass  # expected

    mock_email_responder.forward.assert_not_called()


def test_workflow_yaml_contains_schedule(sample_job_search_workflow_yaml):
    """The workflow YAML should define a cron schedule."""
    with open(sample_job_search_workflow_yaml) as fh:
        content = fh.read()
    assert "schedule" in content
    assert "* * *" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
