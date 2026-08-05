from unittest.mock import MagicMock, patch
import pytest
import anthropic
from agents.research import ResearchAgent
from config import Settings

# Configuración simulada con API Key válida para pasar la validación inicial
MOCK_SETTINGS = Settings(
    anthropic_api_key="dummy-test-key",
    anthropic_model="claude-3-7-sonnet-20250219"
)

@patch("agents.base.get_settings", return_value=MOCK_SETTINGS)
@patch("agents.research.anthropic.Anthropic")
def test_research_agent_handles_rate_limit_error(mock_anthropic, mock_get_settings):
    """Verifica que un error HTTP 429 (Rate Limit) sea capturado de forma limpia."""
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

@patch("agents.base.get_settings", return_value=MOCK_SETTINGS)
@patch("agents.research.anthropic.Anthropic")
def test_research_agent_handles_malformed_response(mock_anthropic, mock_get_settings):
    """Verifica que el agente no explote si la API devuelve contenido vacío o inesperado."""
    mock_client = mock_anthropic.return_value
    mock_response = mock_client.messages.create.return_value
    mock_response.content = []  # Sin bloques de contenido

    agent = ResearchAgent()
    res = agent.run("AI Trends")

    assert not res.success
    assert "no text block" in res.error.lower() or "empty" in res.error.lower()
