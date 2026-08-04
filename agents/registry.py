from typing import Dict, Type, List
from agents.base import BaseAgent
from agents.research import ResearchAgent
from agents.planning import PlanningAgent
from agents.outreach import OutreachAgent

AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
    "research": ResearchAgent,
    "researchagent": ResearchAgent,
    "planning": PlanningAgent,
    "outreach": OutreachAgent,
}


def list_agents() -> List[str]:
    return list(AGENT_REGISTRY.keys())


def get_agent(name: str) -> BaseAgent:
    agent_cls = AGENT_REGISTRY.get(name.lower())
    if not agent_cls:
        available = ", ".join(sorted(AGENT_REGISTRY.keys()))
        raise ValueError(
            f"Agente '{name}' no encontrado. Disponibles: {available}"
        )
    return agent_cls()
