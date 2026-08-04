from typing import Any
from agents.base import BaseAgent
from agents.result import AgentResult


class PlanningAgent(BaseAgent):
    name: str = "planning"
    description: str = "Agente para planificación y desglose de tareas."

    def _execute(self, prompt: str, **kwargs: Any) -> AgentResult:
        if not prompt or not prompt.strip():
            return AgentResult(
                success=False,
                content="",
                error="Goal/topic cannot be empty",
            )

        return AgentResult(
            success=False,
            content="",
            error="PlanningAgent is not fully implemented yet.",
        )
