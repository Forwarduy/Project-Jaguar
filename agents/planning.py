from typing import Any
from .base import BaseAgent
from .result import AgentResult


class PlanningAgent(BaseAgent):
    """Agente encargado de la planificación estratégica.
    
    Placeholder — reemplazar la implementación de run() cuando se integre el motor de planificación (ver ROADMAP.md).
    """

    def __init__(self):
        super().__init__(name="PlanningAgent")

    def run(self, goal: str, **kwargs: Any) -> AgentResult:
        """Maneja la lógica de planificación estratégica para el objetivo especificado."""
        clean_goal = goal.strip() if goal else ""
        if not clean_goal:
            return AgentResult.fail("goal cannot be empty")

        return AgentResult.fail(
            "PlanningAgent not implemented yet. Check ROADMAP.md for updates.",
            metadata={"status": "not_implemented", "agent": self.name}
        )
