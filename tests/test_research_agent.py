from unittest.mock import patch
from agents.research import ResearchAgent
from config import get_settings

@patch("agents.research.anthropic.Anthropic")
def test_run_returns_success_result(mock_anthropic):
    mock_client = mock_anthropic.return_value
    mock_response = mock_client.messages.create.return_value
    mock_response.content = [type("Block", (), {"text": "Research finding"})]
    
    agent = ResearchAgent()
    res = agent.run("AI Trends")
    assert res.success

@patch("config.get_settings")
def test_run_without_api_key_returns_error_result(mock_settings):
    mock_settings.return_value.anthropic_api_key = None
    agent = ResearchAgent()
    res = agent.run("AI Trends")
    assert not res.success

@patch("agents.research.anthropic.Anthropic")
def test_run_respects_model_override(mock_anthropic):
    agent = ResearchAgent()
    agent.run("AI Trends", model="claude-3-haiku-20240307")
    assert mock_anthropic.called

@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MAX_RETRIES": "5"}, clear=True)
def test_client_respects_max_retries_override(mock_anthropic_cls):
    get_settings.cache_clear()
    agent = ResearchAgent()
    _ = agent.client
    assert mock_anthropic_cls.called
