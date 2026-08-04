from .base import BaseAgent
from .result import AgentResult


class OutreachAgent(BaseAgent):
    """Placeholder — reemplazar run() cuando se implemente de verdad (ver ROADMAP.md)."""

    def __init__(self):
        super().__init__(name="OutreachAgent")

    def run(self, campaign: str) -> AgentResult:
        return AgentResult.fail("Not implemented yet")
