from unittest.mock import patch, MagicMock
from agents.research import ResearchAgent
from config import Settings


def test_research_agent_missing_api_key():
    mock_settings = Settings(anthropic_api_key="", anthropic_model="claude-3-7-sonnet-20250219")
    with patch("agents.base.get_settings", return_value=mock_settings):
        agent = ResearchAgent()
        result = agent.execute(topic="AI architecture")
        assert result.success is False
        assert result.error == "ANTHROPIC_API_KEY is not configured"
        assert result.data is None
