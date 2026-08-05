"""Agent registry for discovering, registering, and managing Project Jaguar agents."""

from typing import Dict, List, Type, Optional
from agents.base import BaseAgent


class AgentRegistry:
    """Registry for managing available agent classes and instances."""

    def __init__(self):
        self._agents: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: str, agent_cls: Type[BaseAgent]) -> None:
        """Register an agent class with a given name."""
        self._agents[name.lower()] = agent_cls

    def get(self, name: str) -> Optional[Type[BaseAgent]]:
        """Retrieve an agent class by name."""
        return self._agents.get(name.lower())

    def list_agents(self) -> List[str]:
        """List all registered agent names."""
        return sorted(list(self._agents.keys()))

    def unregister(self, name: str) -> None:
        """Unregister an agent by name."""
        key = name.lower()
        if key in self._agents:
            del self._agents[key]


# Global default registry instance and helper functions for convenience
AGENT_REGISTRY = AgentRegistry()


def get_agent(name: str) -> Optional[Type[BaseAgent]]:
    """Retrieve an agent class by name from the global registry."""
    return AGENT_REGISTRY.get(name)


def list_agents() -> List[str]:
    """List all registered agent names from the global registry."""
    return AGENT_REGISTRY.list_agents()
