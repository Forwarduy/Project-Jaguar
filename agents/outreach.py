from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.registry import AGENT_REGISTRY
from agents.result import AgentResult
from agents.schemas import OutreachOutput


@AGENT_REGISTRY.register("outreach")
class OutreachAgent(BaseAgent):
    """Agent responsible for drafting targeted communication and outreach materials."""

    name: str = "OutreachAgent"

    def run(self, target_audience: str = "", goal: str = "", **kwargs: Any) -> AgentResult:
        if not target_audience or not goal:
            return AgentResult.fail("Parameters 'target_audience' and 'goal' are required.")

        if not self.settings.anthropic_api_key or not getattr(self.settings.anthropic_api_key, "get_secret_value", lambda: self.settings.anthropic_api_key)():
            return AgentResult.fail("ANTHROPIC_API_KEY is not configured")

        try:
            api_key = self.settings.anthropic_api_key.get_secret_value() if hasattr(self.settings.anthropic_api_key, "get_secret_value") else self.settings.anthropic_api_key
            client = anthropic.Anthropic(api_key=api_key)

            system_prompt = (
                "You are an executive communication specialist. Craft concise, high-converting "
                "outreach messages tailored precisely to the target audience and goal."
            )
            prompt = f"Target Audience: {target_audience}\nGoal: {goal}"

            structured_data: OutreachOutput = self._call_llm_structured(
                client=client,
                schema_cls=OutreachOutput,
                prompt=prompt,
                system_prompt=system_prompt,
            )

            return AgentResult.ok(
                data=structured_data.model_dump(),
                metadata={"target_audience": target_audience},
            )
        except Exception as e:
            return AgentResult.fail(f"Outreach execution failed: {str(e)}")
