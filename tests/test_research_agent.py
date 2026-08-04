from unittest.mock import patch, MagicMock
from agents.research import ResearchAgent
from config import Settings


def test_research_agent_success():
    mock_settings = Settings(
        anthropic_api_key="dummy-key",
        anthropic_model="claude-3-7-sonnet-20250219"
    )
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            
            mock_message = MagicMock()
            mock_message.content = [MagicMock(text="Research insights generated")]
            mock_client.messages.create.return_value = mock_message
            
            agent = ResearchAgent()
            result = agent.execute(topic="Quantum Computing")
            
            assert result.success is True
            assert result.data["research"] == "Research insights generated"
            assert result.data["topic"] == "Quantum Computing"
            
            mock_client.messages.create.assert_called_once_with(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": "Perform research on the following topic: Quantum Computing",
                    }
                ],
            )


def test_research_agent_model_override():
    custom_model = "claude-3-5-haiku-20241022"
    mock_settings = Settings(
        anthropic_api_key="dummy-key",
        anthropic_model=custom_model
    )
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.return_value = MagicMock(content=[MagicMock(text="OK")])
            
            agent = ResearchAgent()
            agent.execute(topic="Test")
            
            mock_client.messages.create.assert_called_once_with(
                model=custom_model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": "Perform research on the following topic: Test",
                    }
                ],
            )


def test_research_agent_api_failure():
    mock_settings = Settings(
        anthropic_api_key="dummy-key",
        anthropic_model="claude-3-7-sonnet-20250219"
    )
    with patch("agents.base.get_settings", return_value=mock_settings):
        with patch("anthropic.Anthropic") as mock_anthropic:
            mock_client = MagicMock()
            mock_anthropic.return_value = mock_client
            mock_client.messages.create.side_effect = Exception("API Connection Timeout")
            
            agent = ResearchAgent()
            result = agent.execute(topic="Failure Case")
            
            assert result.success is False
            assert result.error == "API Connection Timeout"
            assert result.data is None
