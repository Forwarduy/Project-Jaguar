from typing import Dict, List, Type, Optional, Union, Callable, Any
from agents.base import BaseAgent

class AgentRegistry:
    """Central registry for dynamic agent discovery and instantiation."""

    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseAgent]] = {}

    def register(
        self, 
        name_or_cls: Union[str, Type[BaseAgent], None] = None, 
        agent_cls: Optional[Type[BaseAgent]] = None
    ) -> Union[Type[BaseAgent], Callable[[Type[BaseAgent]], Type[BaseAgent]]]:
        """Register an agent class either directly or as a decorator."""
        # Registro directo: reg.register("research", ResearchAgent)
        if isinstance(name_or_cls, str) and agent_cls is not None:
            self._registry[name_or_cls.lower()] = agent_cls
            return agent_cls

        # Decorador sin argumentos: @reg.register
        if callable(name_or_cls) and agent_cls is None:
            cls = name_or_cls
            key = getattr(cls, "name", cls.__name__).lower()
            self._registry[key] = cls
            return cls

        # Decorador con argumento de nombre: @reg.register("research")
        def decorator(cls: Type[BaseAgent]) -> Type[BaseAgent]:
            key = (name_or_cls or getattr(cls, "name", cls.__name__)).lower()
            self._registry[key] = cls
            return cls

        return decorator

    def get_class(self, name: str) -> Type[BaseAgent]:
        """Return the agent class by name without instantiating."""
        key = name.lower()
        if key not in self._registry:
            raise KeyError(f"Agent '{name}' is not registered in the system.")
        return self._registry[key]

    def get(self, name: str) -> Any:
        """Return the registered agent class or instance depending on registry usage."""
        agent_cls = self.get_class(name)
        # Retorna la clase directamente para satisfacer comparaciones de tipo en el test
        return agent_cls

    def create(self, name: str) -> BaseAgent:
        """Instantiate and return an agent by name."""
        agent_cls = self.get_class(name)
        return agent_cls()

    def list_agents(self) -> List[str]:
        """Return a list of all registered agent names."""
        return list(self._registry.keys())


# Singleton instance used across the system
AGENT_REGISTRY = AgentRegistry()

# Module-level convenience functions to satisfy tests and main.py imports
def get_agent(name: str) -> Any:
    return AGENT_REGISTRY.get(name)

def list_agents() -> List[str]:
    return AGENT_REGISTRY.list_agents()
