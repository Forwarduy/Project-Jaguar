"""Tests para ResearchAgent. Usan mocks: no requieren ANTHROPIC_API_KEY real ni red,
así que corren igual de bien en CI que en local."""
from unittest.mock import patch, MagicMock

from agents.research import ResearchAgent


def _mock_response(text="insight 1, insight 2, insight 3"):
    block = MagicMock()
    block.text = text
    response = MagicMock()
    response.content = [block]
    return response


@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}, clear=True)
def test_run_returns_success_result(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.return_value = _mock_response("Insight A")
    mock_anthropic_cls.return_value = mock_client

    agent = ResearchAgent()
    result = agent.run("Uruguay EV market")

    assert result.success is True
    assert result.content == "Insight A"
    assert result.error is None
    _, kwargs = mock_client.messages.create.call_args
    assert kwargs["model"] == agent.model


@patch.dict("os.environ", {}, clear=True)
def test_run_without_api_key_returns_error_result():
    agent = ResearchAgent()
    result = agent.run("cualquier tema")

    assert result.success is False
    assert "ANTHROPIC_API_KEY" in result.error


@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}, clear=True)
def test_run_handles_api_failure_gracefully(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_client.messages.create.side_effect = RuntimeError("simulated failure")
    mock_anthropic_cls.return_value = mock_client

    agent = ResearchAgent()
    result = agent.run("cualquier tema")

    assert result.success is False
    assert result.error is not None


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}, clear=True)
def test_run_rejects_empty_topic():
    agent = ResearchAgent()
    result = agent.run("   ")

    assert result.success is False
    assert "empty" in result.error.lower()


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MODEL": "claude-opus-4-8"}, clear=True)
def test_run_respects_model_override():
    agent = ResearchAgent()
    assert agent.model == "claude-opus-4-8"


@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}, clear=True)
def test_client_configured_with_max_retries(mock_anthropic_cls):
    agent = ResearchAgent()

    _, kwargs = mock_anthropic_cls.call_args
    assert kwargs["max_retries"] == 2
    assert agent.client is not None


@patch("agents.research.anthropic.Anthropic")
@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key", "ANTHROPIC_MAX_RETRIES": "5"}, clear=True)
def test_client_respects_max_retries_override(mock_anthropic_cls):
    ResearchAgent()

    _, kwargs = mock_anthropic_cls.call_args
    assert kwargs["max_retries"] == 5
