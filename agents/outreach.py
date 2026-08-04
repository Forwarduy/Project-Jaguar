from .base import BaseAgent
from .result import AgentResult


class OutreachAgent(BaseAgent):
    """Placeholder — reemplazar run() cuando se implemente de verdad (ver ROADMAP.md)."""

    def __init__(self):
        super().__init__(name="OutreachAgent")

    def run(self, campaign: str, **kwargs) -> AgentResult:
        """
        Maneja la lógica de campañas de comunicación.
        Pendiente de integración con integraciones de correo/n8n.
        """
        return AgentResult.fail("OutreachAgent not implemented yet. Check ROADMAP.md for updates.")
