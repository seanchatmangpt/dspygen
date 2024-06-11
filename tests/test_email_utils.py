import os

import pytest
from unittest.mock import MagicMock, patch
from dspygen.email_utils import create_message, send_email, login_to_smtp, main


@pytest.fixture
def email_env_vars(monkeypatch):
    """
    Fixture to set environment variables for email address and password.
    Uses monkeypatch to temporarily set environment variables for testing.
    """
    monkeypatch.setenv('EMAIL_ADDRESS', 'your_email@example.com')
    monkeypatch.setenv('EMAIL_PASSWORD', 'your_password')


def test_create_message(email_env_vars):
    """
    Test creating an email message.
    """
    from_email = os.getenv('EMAIL_ADDRESS')
    to_email = 'test@example.com'
    msg = create_message("Test Subject", "Test Body", from_email, to_email)

    assert msg['Subject'] == 'Test Subject'
    assert msg['From'] == from_email
    assert msg['To'] == to_email
    assert msg.get_payload() == 'Test Body'


def test_send_email(mocker, email_env_vars):
    """
    Test sending an email using the send_email function.
    """
    mock_server = MagicMock()
    from_email = os.getenv('EMAIL_ADDRESS')
    to_email = 'test@example.com'
    msg = create_message("Test Subject", "Test Body", from_email, to_email)

    send_email(mock_server, msg, from_email, to_email)

    mock_server.sendmail.assert_called_once_with(from_email, to_email, msg.as_string())


def test_login_to_smtp(mocker, email_env_vars):
    """
    Test logging in to the SMTP server.
    """
    mock_smtp = mocker.patch('smtplib.SMTP_SSL', autospec=True)
    mock_instance = mock_smtp.return_value

    server = login_to_smtp()

    mock_smtp.assert_called_once_with('smtp.gmail.com', 465)
    mock_instance.login.assert_called_once_with('your_email@example.com', 'your_password')
    assert server == mock_instance


def test_main(mocker, email_env_vars):
    """
    Comprehensive test for the main function.
    Verifies the creation of the message, SMTP login, and sending of the email.
    """
    mock_smtp = mocker.patch('smtplib.SMTP_SSL', autospec=True)
    mock_instance = mock_smtp.return_value
    mock_instance.sendmail = MagicMock()

    main("Test Subject", "Test Body", "test@example.com")

    mock_smtp.assert_called_once_with('smtp.gmail.com', 465)
    mock_instance.login.assert_called_once_with('your_email@example.com', 'your_password')
    mock_instance.sendmail.assert_called_once()
    mock_instance.quit.assert_called_once()
