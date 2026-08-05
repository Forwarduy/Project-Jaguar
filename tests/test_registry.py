import pytest
from agents.registry import AgentRegistry
from agents.research import ResearchAgent
from agents.planning import PlanningAgent
from agents.outreach import OutreachAgent

def test_registry_register_and_get():
    reg = AgentRegistry()
    reg.register("research", ResearchAgent)
    reg.register("planning", PlanningAgent)
    reg.register("outreach", OutreachAgent)

    assert reg.get("research") == ResearchAgent
    assert reg.get("planning") == PlanningAgent
    assert reg.get("outreach") == OutreachAgent

def test_registry_get_unknown():
    reg = AgentRegistry()
    with pytest.raises(KeyError):
        reg.get("non_existent_agent")
