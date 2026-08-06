"""Central registry for managing and dispatching AI agents."""

from typing import Callable, Dict, Type, Any, Optional
import logging

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry to store and retrieve agent classes dynamically."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[Any]] = {}

    def register(self, name: str) -> Callable[[Type[Any]], Type[Any]]:
        """Decorator to register an agent class under a specific name."""
        def decorator(cls: Type[Any]) -> Type[Any]:
            if name in self._registry:
                logger.warning("Overwriting existing agent registration for: %s", name)
            self._registry[name] = cls
            logger.debug("Successfully registered agent: %s -> %s", name, cls.__name__)
            return cls
        return decorator

    def get(self, name: str) -> Optional[Type[Any]]:
        """Retrieve an agent class by its registered name."""
        return self._registry.get(name)

    def list_agents(self) -> list[str]:
        """Return a list of all registered agent names."""
        return list(self._registry.keys())

    def clear(self) -> None:
        """Clear all registered agents (useful for testing)."""
        self._registry.clear()


# Global registry instance used across the application
registry = AgentRegistry()
