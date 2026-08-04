from unittest.mock import MagicMock, patch
import anthropic
from agents.research import ResearchAgent


@patch("config.get_settings")
@patch("agents.research.anthropic.Anthropic")
def test_research_agent_handles_rate_limit_error(mock_anthropic, mock_settings):
    """Verifica que un error HTTP 429 (Rate Limit) sea capturado de forma limpia."""
    mock_settings.return_value.anthropic_api_key = "dummy-key"
    mock_client = mock_anthropic.return_value
    mock_response = MagicMock()
    mock_response.status_code = 429

    mock_client.messages.create.side_effect = anthropic.RateLimitError(
        message="Rate limit exceeded",
        response=mock_response,
        body={"error": {"message": "Rate limit exceeded"}},
    )

    agent = ResearchAgent()
    res = agent.run("AI Trends")

    assert not res.success
    assert res.error is not None
    assert "rate limit" in res.error.lower() or "429" in res.error


@patch("config.get_settings")
@patch("agents.research.anthropic.Anthropic")
def test_research_agent_handles_api_connection_error(mock_anthropic, mock_settings):
    """Verifica el comportamiento ante caídas de red o timeouts."""
    mock_settings.return_value.anthropic_api_key = "dummy-key"
    mock_client = mock_anthropic.return_value
    mock_client.messages.create.side_effect = anthropic.APIConnectionError(
        request=MagicMock()
    )

    agent = ResearchAgent()
    res = agent.run("AI Trends")

    assert not res.success
    assert res.error is not None


@patch("config.get_settings")
@patch("agents.research.anthropic.Anthropic")
def test_research_agent_handles_overloaded_error(mock_anthropic, mock_settings):
    """Verifica el comportamiento cuando los servidores de Anthropic están sobrecargados (529)."""
    mock_settings.return_value.anthropic_api_key = "dummy-key"
    mock_client = mock_anthropic.return_value
    mock_response = MagicMock()
    mock_response.status_code = 529

    mock_client.messages.create.side_effect = anthropic.InternalServerError(
        message="Overloaded",
        response=mock_response,
        body={"error": {"message": "Overloaded"}},
    )

    agent = ResearchAgent()
    res = agent.run("AI Trends")

    assert not res.success
    assert res.error is not None


@patch("config.get_settings")
@patch("agents.research.anthropic.Anthropic")
def test_research_agent_handles_malformed_response(mock_anthropic, mock_settings):
    """Verifica que el agente no explote si la API devuelve contenido vacío o inesperado."""
    mock_settings.return_value.anthropic_api_key = "dummy-key"
    mock_client = mock_anthropic.return_value
    mock_response = mock_client.messages.create.return_value
    mock_response.content = []  # Sin bloques de contenido

    agent = ResearchAgent()
    res = agent.run("AI Trends")

    assert not res.success
    assert "no text block" in res.error.lower() or "empty" in res.error.lower()
