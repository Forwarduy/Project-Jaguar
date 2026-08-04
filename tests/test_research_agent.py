from unittest.mock import MagicMock, patch
import pytest

from agents.research import ResearchAgent
from config import get_settings


def _mock_response(text: str):
    block = MagicMock()
    block.type = "text"
    block.text = text
    response = MagicMock()
    response.content = [block]
    return response


@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}, clear=True)
def test_run_returns_success_result(mock_anthropic_cls):
    get_settings.cache_clear()
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response("Insight A")
    mock_anthropic_cls.return_value = mock_client

    agent = ResearchAgent()
    result = agent.run("Uruguay EV market")

    assert result.success is True
    assert result.content == "Insight A"


@patch.dict("os.environ", {}, clear=True)
def test_run_without_api_key_returns_error_result():
    get_settings.cache_clear()
    agent = ResearchAgent()
    result = agent.run("cualquier tema")

    assert result.success is False
    assert any(err in result.error for err in ["ANTHROPIC_API_KEY", "authentication_error", "401", "invalid x-api-key"])


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MODEL": "claude-opus-4-8"}, clear=True)
def test_run_respects_model_override():
    get_settings.cache_clear()
    agent = ResearchAgent()
    assert agent.model == "claude-opus-4-8"


@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MAX_RETRIES": "5"}, clear=True)
def test_client_respects_max_retries_override(mock_anthropic_cls):
    get_settings.cache_clear()
    ResearchAgent()

    _, kwargs = mock_anthropic_cls.call_args
    assert int(kwargs["max_retries"]) == 5
