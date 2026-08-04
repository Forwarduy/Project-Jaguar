from .base import BaseAgent
from .result import AgentResult


class PlanningAgent(BaseAgent):
    """Placeholder — reemplazar run() cuando se implemente de verdad (ver ROADMAP.md)."""

    def __init__(self):
        super().__init__(name="PlanningAgent")

    def run(self, goal: str) -> AgentResult:
        return AgentResult.fail("Not implemented yet - using same pattern as research.py")
