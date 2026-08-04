from typing import Any
from agents.base import BaseAgent
from agents.result import AgentResult


class OutreachAgent(BaseAgent):
    name: str = "outreach"
    description: str = "Agente para comunicación y generación de alcance."

    def _execute(self, prompt: str, **kwargs: Any) -> AgentResult:
        if not prompt or not prompt.strip():
            return AgentResult(
                success=False,
                content="",
                error="Campaign/topic cannot be empty",
            )

        return AgentResult(
            success=False,
            content="",
            error="OutreachAgent is not fully implemented yet.",
        )
