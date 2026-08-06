"""Central registry for managing and dispatching AI agents."""

from typing import Callable, Dict, Type, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry to store and retrieve agent classes dynamically."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Any]] = {}

    def register(self, name_or_cls: Union[str, Type[Any]], cls: Optional[Type[Any]] = None) -> Any:
        """Register an agent class either directly or as a decorator."""
        if cls is not None:
            # Direct registration: reg.register("name", AgentClass)
            name = name_or_cls
            if not isinstance(name, str):
                raise TypeError("Agent name must be a string")
            self._registry[name] = cls
            logger.debug("Successfully registered agent: %s -> %s", name, cls.__name__)
            return cls
        
        # Decorator usage
        if isinstance(name_or_cls, str):
            # @reg.register("name")
            name = name_or_cls
            def decorator(agent_cls: Type[Any]) -> Type[Any]:
                self._registry[name] = agent_cls
                logger.debug("Successfully registered agent: %s -> %s", name, agent_cls.__name__)
                return agent_cls
            return decorator
        else:
            # @reg.register (without args, using class name or attribute)
            agent_cls = name_or_cls
            name = getattr(agent_cls, "name", agent_cls.__name__.lower())
            self._registry[name] = agent_cls
            logger.debug("Successfully registered agent: %s -> %s", name, agent_cls.__name__)
            return agent_cls

    def get(self, name: str) -> Type[Any]:
        """Retrieve an agent class by its registered name, raising KeyError if missing."""
        if name not in self._registry:
            raise KeyError(f"Agent '{name}' not found in registry.")
        return self._registry[name]

    def list_agents(self) -> list[str]:
        """Return a list of all registered agent names."""
        return list(self._registry.keys())

    def clear(self) -> None:
        """Clear all registered agents (useful for testing)."""
        self._registry.clear()


# Global registry instance
registry = AgentRegistry()

# Alias and compatibility wrappers expected by existing code and tests
AGENT_REGISTRY = registry

def get_agent(name: str) -> Type[Any]:
    """Compatibility helper to get an agent from the global registry."""
    return registry.get(name)

def list_agents() -> list[str]:
    """Compatibility helper to list agents from the global registry."""
    return registry.list_agents()
