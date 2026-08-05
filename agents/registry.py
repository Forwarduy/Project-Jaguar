from typing import Dict, Type
from agents.base import BaseAgent

class AgentRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: str, agent_cls: Type[BaseAgent]) -> None:
        self._registry[name.lower()] = agent_cls

    def get(self, name: str) -> Type[BaseAgent]:
        key = name.lower()
        if key not in self._registry:
            raise KeyError(f"Agent '{name}' is not registered.")
        return self._registry[key]

# Instancia global por defecto
registry = AgentRegistry()
