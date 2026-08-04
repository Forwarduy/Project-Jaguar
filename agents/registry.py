from typing import Type
from .base import BaseAgent
from .research import ResearchAgent
from .planning import PlanningAgent
from .outreach import OutreachAgent

# Mapeo de identificadores a clases de agentes
AGENT_REGISTRY: dict[str, Type[BaseAgent]] = {
    "research": ResearchAgent,
    "plan": PlanningAgent,
    "planning": PlanningAgent,  # Alias para mayor consistencia
    "outreach": OutreachAgent,
}


def get_agent(name: str) -> BaseAgent:
    """
    Obtiene e instancia el agente solicitado por su nombre.
    Soporta búsquedas no sensibles a mayúsculas/minúsculas.
    
    Raises:
        ValueError: Si el nombre del agente no está registrado.
    """
    normalized_name = name.strip().lower()
    agent_cls = AGENT_REGISTRY.get(normalized_name)
    
    if not agent_cls:
        available = ", ".join(sorted(AGENT_REGISTRY.keys()))
        raise ValueError(f"Agente '{name}' no encontrado. Agentes disponibles: {available}")
        
    return agent_cls()


def list_agents() -> list[str]:
    """Retorna la lista de nombres de agentes registrados."""
    return list(AGENT_REGISTRY.keys())
