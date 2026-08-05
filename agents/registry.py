from typing import Dict, List, Type, Optional
from agents.base import BaseAgent

class AgentRegistry:
    """Central registry for dynamic agent discovery and instantiation."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseAgent]] = {}

    def register(self, name: Optional[str] = None):
        """Decorator to register an agent class automatically."""
        def decorator(subclass: Type[BaseAgent]):
            key = (name or subclass.name or subclass.__name__).lower()
            self._registry[key] = subclass
            return subclass
        return decorator

    def get(self, name: str) -> BaseAgent:
        """Instantiate and return an agent by name."""
        agent_cls = self._registry.get(name.lower())
        if not agent_cls:
            raise ValueError(f"Agent '{name}' is not registered in the system.")
        return agent_cls()

    def list_agents(self) -> List[str]:
        """Return a list of all registered agent names."""
        return list(self._registry.keys())


# Singleton instance used across the system
AGENT_REGISTRY = AgentRegistry()

# Module-level convenience functions to satisfy tests and main.py imports
def get_agent(name: str) -> BaseAgent:
    return AGENT_REGISTRY.get(name)

def list_agents() -> List[str]:
    return AGENT_REGISTRY.list_agents()
