from unittest.mock import MagicMock, patch
import pytest
from agents.outreach import OutreachAgent
from config import Settings

def test_outreach_agent_missing_api_key():
    mock_settings = Settings(anthropic_api_key="", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        agent = OutreachAgent()
        result = agent.execute(recipient="Partner")
        assert result.success is False
        assert result.error == "ANTHROPIC_API_KEY is not configured"

def test_outreach_agent_success_with_context():
    mock_settings = Settings(anthropic_api_key="dummy-key", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_message = MagicMock()
            mock_message.content = [MagicMock(text="Hello Partner, glad to connect.")]
            mock_client.messages.create.return_value = mock_message

            agent = OutreachAgent()
            result = agent.execute(recipient="Partner", message_context="Project updates")

            assert result.success is True
            assert result.data["message"] == "Hello Partner, glad to connect."
            assert result.data["recipient"] == "Partner"

def test_outreach_agent_empty_response():
    mock_settings = Settings(anthropic_api_key="dummy-key", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.return_value = MagicMock(content=[])

            agent = OutreachAgent()
            result = agent.execute(recipient="Partner")

            assert result.success is False
            assert "Empty response" in result.error

def test_outreach_agent_api_exception():
    mock_settings = Settings(anthropic_api_key="dummy-key", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.side_effect = Exception("Outreach Error")

            agent = OutreachAgent()
            result = agent.execute(recipient="Partner")

            assert result.success is False
            assert result.error == "Outreach Error"
