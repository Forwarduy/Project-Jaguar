from typing import Dict, List, Type
from agents.base import BaseAgent

class AgentRegistry:
    """Central registry for dynamic agent discovery and instantiation."""

    _registry: Dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register an agent class automatically."""
        def decorator(subclass: Type[BaseAgent]):
            cls._registry[name.lower()] = subclass
            return subclass
        return decorator

    @classmethod
    def get(cls, name: str) -> BaseAgent:
        """Instantiate and return an agent by name."""
        agent_cls = cls._registry.get(name.lower())
        if not agent_cls:
            raise ValueError(f"Agent '{name}' is not registered in the system.")
        return agent_cls()

    @classmethod
    def list_agents(cls) -> List[str]:
        """Return a list of all registered agent names."""
        return list(cls._registry.keys())
