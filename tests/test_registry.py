import pytest
from agents.registry import AgentRegistry
from agents.research import ResearchAgent
from agents.planning import PlanningAgent
from agents.outreach import OutreachAgent

def test_registry_get_agent():
    registry = AgentRegistry()
    registry.register("research", ResearchAgent)
    registry.register("planning", PlanningAgent)
    registry.register("outreach", OutreachAgent)

    assert isinstance(registry.get("research")(), ResearchAgent)
    assert isinstance(registry.get("planning")(), PlanningAgent)
    assert isinstance(registry.get("outreach")(), OutreachAgent)

def test_registry_get_nonexistent():
    registry = AgentRegistry()
    with pytest.raises(KeyError):
        registry.get("unknown_agent")
