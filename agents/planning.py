from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.result import AgentResult

class PlanningAgent(BaseAgent):
    """Agent responsible for creating execution plans for goals."""

    name: str = "PlanningAgent"

    def run(self, goal: str, **kwargs: Any) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult.fail("ANTHROPIC_API_KEY is not configured", metadata={"goal": goal})

        try:
            client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
            prompt = f"Create a step-by-step strategic execution plan for the following goal: {goal}"

            response = client.messages.create(
                model=self.settings.anthropic_model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            if not response.content or not hasattr(response.content[0], "text"):
                return AgentResult.fail("Empty response or malformed response from Anthropic API", metadata={"goal": goal})

            content = response.content[0].text
            return AgentResult.ok(
                content=content,
                data={"plan": content, "goal": goal},
                metadata={"goal": goal},
            )

        except Exception as e:
            return AgentResult.fail(str(e), metadata={"goal": goal})
