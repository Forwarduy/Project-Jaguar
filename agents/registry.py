from typing import Dict, List, Type
from agents.base import BaseAgent
from agents.research import ResearchAgent
from agents.planning import PlanningAgent
from agents.outreach import OutreachAgent

AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
    "research": ResearchAgent,
    "planning": PlanningAgent,
    "outreach": OutreachAgent,
}

class AgentRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[BaseAgent]] = dict(AGENT_REGISTRY)

    def register(self, name: str, agent_cls: Type[BaseAgent]) -> None:
        self._registry[name.lower()] = agent_cls

    def get(self, name: str) -> Type[BaseAgent]:
        key = name.lower()
        if key not in self._registry:
            raise KeyError(f"Agent '{name}' is not registered.")
        return self._registry[key]

# Instancia global por defecto
registry = AgentRegistry()

def get_agent(name: str) -> Type[BaseAgent]:
    return registry.get(name)

def list_agents() -> List[str]:
    return list(AGENT_REGISTRY.keys())
