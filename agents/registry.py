"""Agent registry for discovering, registering, and managing Project Jaguar agents."""

from typing import Dict, List, Type, Optional, Union, Any
from agents.base import BaseAgent


class AgentRegistry:
    """Registry for managing available agent classes and instances."""

    def __init__(self):
        self._agents: Dict[str, Type[BaseAgent]] = {}

    def register(
        self,
        name_or_cls: Union[str, Type[BaseAgent], None] = None,
        agent_cls: Optional[Type[BaseAgent]] = None
    ):
        """Register an agent class with a given name or via decorator."""
        if agent_cls is not None:
            # Direct call: reg.register("name", Cls)
            self._agents[str(name_or_cls).lower()] = agent_cls
            return agent_cls
        elif isinstance(name_or_cls, str):
            # Decorator with name: @reg.register("name")
            def decorator(cls: Type[BaseAgent]) -> Type[BaseAgent]:
                self._agents[name_or_cls.lower()] = cls
                return cls
            return decorator
        elif callable(name_or_cls):
            # Decorator without args: @reg.register
            cls = name_or_cls
            # Register using both the class name and the class attribute 'name' if available
            self._agents[cls.__name__.lower()] = cls
            if hasattr(cls, "name") and isinstance(cls.name, str):
                self._agents[cls.name.lower()] = cls
            return cls
        else:
            raise TypeError("Invalid arguments for register")

    def get(self, name: str, config: Optional[Dict[str, Any]] = None) -> BaseAgent:
        """Retrieve and instantiate an agent by name."""
        key = name.lower()
        if key not in self._agents:
            raise KeyError(f"Agent '{name}' not found in registry.")
        cls = self._agents[key]
        return cls(config=config)

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


def get_agent(name: str, config: Optional[Dict[str, Any]] = None) -> BaseAgent:
    """Retrieve an agent instance by name from the global registry."""
    return AGENT_REGISTRY.get(name, config)


def list_agents() -> List[str]:
    """List all registered agent names from the global registry."""
    return AGENT_REGISTRY.list_agents()
