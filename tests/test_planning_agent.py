from unittest.mock import MagicMock, patch
import pytest
from agents.planning import PlanningAgent
from config import Settings

def test_planning_agent_missing_api_key():
    mock_settings = Settings(anthropic_api_key="", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        agent = PlanningAgent()
        result = agent.execute(goal="Build agent pipeline")
        assert result.success is False
        assert result.error == "ANTHROPIC_API_KEY is not configured"

def test_planning_agent_success():
    mock_settings = Settings(anthropic_api_key="dummy-key", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_message = MagicMock()
            mock_message.content = [MagicMock(text="1. Setup repository\n2. Define architecture")]
            mock_client.messages.create.return_value = mock_message

            agent = PlanningAgent()
            result = agent.execute(goal="Build agent pipeline")

            assert result.success is True
            assert "1. Setup repository" in result.data["plan"]
            assert result.data["goal"] == "Build agent pipeline"

def test_planning_agent_empty_response():
    mock_settings = Settings(anthropic_api_key="dummy-key", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.return_value = MagicMock(content=[])

            agent = PlanningAgent()
            result = agent.execute(goal="Build agent pipeline")

            assert result.success is False
            assert "Empty response" in result.error

def test_planning_agent_api_exception():
    mock_settings = Settings(anthropic_api_key="dummy-key", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.side_effect = Exception("API Error")

            agent = PlanningAgent()
            result = agent.execute(goal="Build agent pipeline")

            assert result.success is False
            assert result.error == "API Error"
