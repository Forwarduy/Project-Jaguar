import pytest
from unittest.mock import patch, MagicMock
from agents.research import ResearchAgent
from agents.planning import PlanningAgent
from agents.outreach import OutreachAgent
from agents.registry import AGENT_REGISTRY, get_agent, list_agents


def test_research_agent_empty_topic():
    agent = ResearchAgent()
    res = agent.run("   ")
    assert not res.success
    assert res.error == "topic cannot be empty"


@patch("config.get_settings")
def test_research_agent_missing_api_key(mock_settings):
    mock_settings.return_value.anthropic_api_key = None
    agent = ResearchAgent()
    res = agent.run("AI trends")
    assert not res.success
    assert "ANTHROPIC_API_KEY not found" in res.error


@patch("anthropic.Anthropic")
@patch("config.get_settings")
def test_research_agent_success(mock_settings, mock_anthropic):
    mock_settings.return_value.anthropic_api_key = "test-key"
    mock_settings.return_value.anthropic_model = "claude-3-5-sonnet-20241022"
    mock_settings.return_value.anthropic_max_retries = 2

    mock_block = MagicMock()
    mock_block.type = "text"
    mock_block.text = "Insight 1: Growth is high."

    mock_response = MagicMock()
    mock_response.content = [mock_block]

    mock_client_instance = MagicMock()
    mock_client_instance.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client_instance

    agent = ResearchAgent()
    res = agent.run("AI market")

    assert res.success
    assert res.content == "Insight 1: Growth is high."


def test_planning_agent_not_implemented():
    agent = PlanningAgent()
    res = agent.run("Expand to LATAM")
    assert not res.success
    assert "not implemented" in res.error
    assert res.metadata.get("status") == "not_implemented"


def test_planning_agent_empty_goal():
    agent = PlanningAgent()
    res = agent.run("")
    assert not res.success
    assert res.error == "goal cannot be empty"


def test_outreach_agent_not_implemented():
    agent = OutreachAgent()
    res = agent.run("Q3 Email Push")
    assert not res.success
    assert "not implemented" in res.error
    assert res.metadata.get("status") == "not_implemented"


def test_outreach_agent_empty_campaign():
    agent = OutreachAgent()
    res = agent.run("   ")
    assert not res.success
    assert res.error == "campaign cannot be empty"


def test_registry_lookup():
    assert "research" in list_agents()
    assert "plan" in list_agents()
    assert "outreach" in list_agents()

    agent_cls = get_agent("research")
    assert agent_cls == ResearchAgent
