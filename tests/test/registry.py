from agents.registry import AGENT_REGISTRY
from agents.research import ResearchAgent

def test_registry_has_all_three_commands():
    assert set(AGENT_REGISTRY.keys()) == {"research", "planning", "outreach"}

def test_registry_maps_to_correct_classes():
    assert AGENT_REGISTRY["research"] is ResearchAgent
