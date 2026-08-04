from .base import BaseAgent
from .result import AgentResult


class PlanningAgent(BaseAgent):
    """Placeholder — reemplazar run() cuando se implemente de verdad (ver ROADMAP.md)."""

    def __init__(self):
        super().__init__(name="PlanningAgent")

    def run(self, goal: str, **kwargs) -> AgentResult:
        """
        Maneja la lógica de planificación estratégica para el objetivo especificado.
        Pendiente de integración con los modelos de lenguaje.
        """
        return AgentResult.fail("PlanningAgent not implemented yet. Check ROADMAP.md for updates.")
