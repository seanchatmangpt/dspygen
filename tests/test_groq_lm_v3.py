"""
Tests for Groq LM backend (DSPy 3.1.3+)

Run with:
    pytest tests/test_groq_lm_v3.py -v
    # or with GROQ_API_KEY set:
    GROQ_API_KEY=your-key pytest tests/test_groq_lm_v3.py -v
"""

import os
from unittest.mock import Mock, patch, MagicMock

import pytest
import dspy

from dspygen.lm.groq_lm_v3 import Groq, init_groq


class TestGroqLM:
    """Test Groq LM functionality"""

    def test_init_requires_api_key(self):
        """Test that Groq LM requires API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GROQ_API_KEY"):
                Groq()

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_init_with_api_key(self):
        """Test Groq LM initialization with API key"""
        lm = Groq(model="llama3-70b-8192")
        assert lm.model == "llama3-70b-8192"
        assert lm.api_key == "test-key"
        assert lm.provider == "groq"

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_init_with_custom_params(self):
        """Test Groq LM initialization with custom parameters"""
        lm = Groq(
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1000,
            top_p=0.9,
        )
        assert lm.model == "mixtral-8x7b-32768"
        assert lm.model_kwargs["temperature"] == 0.7
        assert lm.model_kwargs["max_tokens"] == 1000
        assert lm.top_p == 0.9

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @patch("dspygen.lm.groq_lm_v3.GroqClient")
    def test_generate_returns_predictions(self, mock_client_class):
        """Test that _generate returns dspy.Prediction objects"""
        # Mock the Groq client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.usage = Mock(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
        )

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_client_class.return_value = mock_client

        # Create LM and generate
        lm = Groq(model="llama3-70b-8192")
        predictions = lm._generate("Test prompt")

        assert len(predictions) == 1
        assert predictions[0].text == "Test response"
        assert predictions[0].usage["total_tokens"] == 30

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @patch("dspygen.lm.groq_lm_v3.GroqClient")
    def test_call_returns_text_list(self, mock_client_class):
        """Test that __call__ returns list of text strings"""
        # Mock the Groq client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated text"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_client_class.return_value = mock_client

        # Create LM and call
        lm = Groq(model="llama3-70b-8192")
        results = lm("Test prompt")

        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0] == "Generated text"

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_get_model_info(self):
        """Test get_model_info returns correct configuration"""
        lm = Groq(
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=2000,
            top_p=0.8,
        )
        info = lm.get_model_info()

        assert info["provider"] == "groq"
        assert info["model"] == "llama3-8b-8192"
        assert info["temperature"] == 0.5
        assert info["max_tokens"] == 2000
        assert info["top_p"] == 0.8

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_from_config(self):
        """Test creating Groq instance from config dict"""
        config = {
            "model": "llama3-70b-8192",
            "temperature": 0.3,
            "max_tokens": 1500,
            "top_p": 0.95,
        }
        lm = Groq.from_config(config)

        assert lm.model == "llama3-70b-8192"
        assert lm.model_kwargs["temperature"] == 0.3
        assert lm.model_kwargs["max_tokens"] == 1500
        assert lm.top_p == 0.95


class TestInitGroq:
    """Test init_groq convenience function"""

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @patch("dspygen.lm.groq_lm_v3.dspy")
    def test_init_groq_configures_dspy(self, mock_dspy):
        """Test that init_groq configures DSPy settings"""
        lm = init_groq(model="llama3-70b-8192", max_tokens=2000)

        assert isinstance(lm, Groq)
        assert lm.model == "llama3-70b-8192"
        mock_dspy.settings.configure.assert_called_once()

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    def test_init_groq_with_custom_params(self):
        """Test init_groq with custom parameters"""
        lm = init_groq(
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1000,
            experimental=False,
        )

        assert lm.model == "llama3-8b-8192"
        assert lm.model_kwargs["temperature"] == 0.7
        assert lm.model_kwargs["max_tokens"] == 1000


class TestDspyIntegration:
    """Test DSPy 3.x integration with Groq"""

    @patch.dict(os.environ, {"GROQ_API_KEY": "test-key"})
    @patch("dspygen.lm.groq_lm_v3.GroqClient")
    def test_dspy_predict_with_groq(self, mock_client_class):
        """Test using Groq LM with dspy.Predict"""
        # Mock the Groq client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "42"
        mock_response.usage = Mock(
            prompt_tokens=5,
            completion_tokens=1,
            total_tokens=6,
        )

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_client_class.return_value = mock_client

        # Configure DSPy with Groq
        lm = Groq(model="llama3-70b-8192")
        dspy.settings.configure(lm=lm)

        # Use DSPy Predict
        predict = dspy.Predict("question -> answer")
        result = predict(question="What is 2+2?")

        assert hasattr(result, "answer")
        assert result.answer == "42"


@pytest.mark.integration
class TestGroqIntegration:
    """
    Integration tests that require real API calls.

    Run with: GROQ_API_KEY=your-key pytest tests/test_groq_lm_v3.py::TestGroqIntegration -v
    """

    @pytest.fixture(autouse=True)
    def skip_without_api_key(self):
        """Skip integration tests if GROQ_API_KEY is not set"""
        if not os.environ.get("GROQ_API_KEY"):
            pytest.skip("GROQ_API_KEY not set - skipping integration test")

    def test_real_groq_request(self):
        """Test real Groq API request"""
        lm = Groq(model="llama3-8b-8192", max_tokens=100)
        results = lm("Say 'Hello, Groq!'")
        assert len(results) == 1
        assert isinstance(results[0], str)

    def test_init_groq_real_call(self):
        """Test init_groq with real API call"""
        lm = init_groq(model="llama3-8b-8192", max_tokens=100)
        results = lm("What is 1+1?")
        assert len(results) == 1
        assert "2" in results[0].lower()
