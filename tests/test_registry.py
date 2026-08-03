"""Tests para el registro de agentes."""
from agents.registry import AGENT_REGISTRY
from agents.research import ResearchAgent
from agents.planning import PlanningAgent
from agents.outreach import OutreachAgent
from agents.base import BaseAgent


def test_registry_has_all_three_commands():
    assert set(AGENT_REGISTRY.keys()) == {"research", "plan", "outreach"}


def test_registry_maps_to_correct_classes():
    assert AGENT_REGISTRY["research"] is ResearchAgent
    assert AGENT_REGISTRY["plan"] is PlanningAgent
    assert AGENT_REGISTRY["outreach"] is OutreachAgent


def test_all_registered_agents_extend_base_agent():
    for agent_cls in AGENT_REGISTRY.values():
        assert issubclass(agent_cls, BaseAgent)


def test_planning_agent_stub_runs():
    agent = PlanningAgent()
    result = agent.run("Q1 goals")
    assert "Coming soon" in result


def test_outreach_agent_stub_runs():
    agent = OutreachAgent()
    result = agent.run("launch campaign")
    assert "Coming soon" in result
