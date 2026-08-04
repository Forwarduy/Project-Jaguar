from typing import Any
from .base import BaseAgent
from .result import AgentResult


class OutreachAgent(BaseAgent):
    """Agente encargado de la ejecución de campañas de comunicación y prospección.

    Placeholder — reemplazar la implementación de run() cuando se integren los conectores de correo/n8n (ver ROADMAP.md).
    """

    def __init__(self):
        super().__init__(name="OutreachAgent")

    def run(self, campaign: str, **kwargs: Any) -> AgentResult:
        """Maneja la lógica de campañas de comunicación."""
        clean_campaign = campaign.strip() if campaign else ""
        if not clean_campaign:
            return AgentResult.fail("campaign cannot be empty")

        return AgentResult.fail(
            "OutreachAgent not implemented yet. Check ROADMAP.md for updates.",
            metadata={"status": "not_implemented", "agent": self.name},
        )
