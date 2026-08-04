from typing import Type, Any
from .base import BaseAgent
from .research import ResearchAgent
from .planning import PlanningAgent
from .outreach import OutreachAgent

# Mapeo de identificadores a clases de agentes
AGENT_REGISTRY: dict[str, Type[BaseAgent]] = {
    "research": ResearchAgent,
    "plan": PlanningAgent,
    "planning": PlanningAgent,  # Alias explícito
    "outreach": OutreachAgent,
}

# Agentes principales sin aliases para exposición pública/CLI
CANONICAL_AGENTS: set[str] = {"research", "planning", "outreach"}


def get_agent(name: str, *args: Any, **kwargs: Any) -> BaseAgent:
    """
    Obtiene e instancia el agente solicitado por su nombre.
    Soporta búsquedas no sensibles a mayúsculas/minúsculas y paso de parámetros.
    
    Raises:
        ValueError: Si el nombre del agente no está registrado.
    """
    normalized_name = name.strip().lower()
    agent_cls = AGENT_REGISTRY.get(normalized_name)
    
    if not agent_cls:
        available = ", ".join(sorted(CANONICAL_AGENTS))
        raise ValueError(f"Agente '{name}' no encontrado. Agentes disponibles: {available}")
        
    return agent_cls(*args, **kwargs)


def list_agents(canonical_only: bool = True) -> list[str]:
    """
    Retorna la lista de nombres de agentes registrados.
    Por defecto filtra aliases para devolver solo nombres canónicos.
    """
    if canonical_only:
        return sorted(list(CANONICAL_AGENTS))
    return list(AGENT_REGISTRY.keys())
