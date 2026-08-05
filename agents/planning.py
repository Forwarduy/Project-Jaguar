import anthropic
from typing import Any, Optional
from config import get_settings
from agents.base import BaseAgent
from agents.result import AgentResult

class PlanningAgent(BaseAgent):
    name: str = "PlanningAgent"

    def __init__(self):
        super().__init__()
        api_key = self.settings.anthropic_api_key or ""
        self.client = anthropic.Anthropic(
            api_key=api_key or "dummy-key",
            max_retries=self.settings.anthropic_max_retries,
        )
        self.model = self.settings.anthropic_model

    def run(self, goal: str, **kwargs: Any) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult.fail(
                error="ANTHROPIC_API_KEY is not configured",
                data=None,
                metadata={"goal": goal},
            )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": f"Create a step-by-step execution plan for the following goal: {goal}",
                    }
                ],
            )

            if not response.content:
                return AgentResult.fail(
                    error="Empty response or no text block returned from API",
                    data=None,
                    metadata={"goal": goal},
                )

            content = response.content[0].text
            return AgentResult.ok(
                content=content,
                data={
                    "plan": content,
                    "goal": goal,
                },
                metadata={"goal": goal},
            )
        except Exception as e:
            return AgentResult.fail(
                error=str(e),
                data=None,
                metadata={"goal": goal},
            )
