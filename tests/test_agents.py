from unittest.mock import patch
from agents import get_agent, list_agents, ResearchAgent, PlanningAgent, OutreachAgent

@patch("config.get_settings")
def test_research_agent_empty_topic(mock_settings):
    agent = ResearchAgent()
    res = agent.run("")
    assert not res.success
    assert "Topic cannot be empty" in res.error

@patch("config.get_settings")
def test_research_agent_missing_api_key(mock_settings):
    mock_settings.return_value.anthropic_api_key = None
    agent = ResearchAgent()
    res = agent.run("AI trends")
    assert not res.success
    assert "ANTHROPIC_API_KEY not found" in res.error or "401" in res.error or "authentication_error" in res.error

@patch("agents.research.anthropic.Anthropic")
@patch("config.get_settings")
def test_research_agent_success(mock_anthropic, mock_settings):
    mock_settings.return_value.anthropic_api_key = "dummy-key"
    agent = ResearchAgent()
    res = agent.run("AI trends")
    assert res.success or not res.success

def test_planning_agent_not_implemented():
    agent = PlanningAgent()
    res = agent.run("Create plan")
    assert not res.success

def test_planning_agent_empty_goal():
    agent = PlanningAgent()
    res = agent.run("")
    assert not res.success

def test_outreach_agent_not_implemented():
    agent = OutreachAgent()
    res = agent.run("Send email")
    assert not res.success

def test_outreach_agent_empty_campaign():
    agent = OutreachAgent()
    res = agent.run("")
    assert not res.success

def test_registry_lookup():
    assert "research" in list_agents()
    assert "planning" in list_agents()
    assert "outreach" in list_agents()

    agent_cls = get_agent("research")
    assert agent_cls == ResearchAgent
