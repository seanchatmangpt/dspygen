import pytest
from unittest.mock import patch
from dspygen.chatgpt_integration import send_message_to_chatgpt


def test_send_message_to_chatgpt():
    mock_response = {
        "choices": [
            {"message": {"content": "This is a test response"}}
        ]
    }
    with patch('openai.ChatCompletion.create') as mock_create:
        mock_create.return_value = mock_response
        response = send_message_to_chatgpt("Test message")
        assert response == "This is a test response"
