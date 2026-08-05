from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.registry import AGENT_REGISTRY
from agents.result import AgentResult
from agents.schemas import PlanningOutput


@AGENT_REGISTRY.register("planning")
class PlanningAgent(BaseAgent):
    """Agent responsible for breaking down projects into executable step-by-step plans."""

    name: str = "PlanningAgent"

    def run(self, project_name: str = "", requirements: str = "", **kwargs: Any) -> AgentResult:
        if not project_name:
            return AgentResult.fail("Parameter 'project_name' is required for PlanningAgent.")

        if not self.settings.anthropic_api_key or not getattr(self.settings.anthropic_api_key, "get_secret_value", lambda: self.settings.anthropic_api_key)():
            return AgentResult.fail("ANTHROPIC_API_KEY is not configured")

        try:
            api_key = self.settings.anthropic_api_key.get_secret_value() if hasattr(self.settings.anthropic_api_key, "get_secret_value") else self.settings.anthropic_api_key
            client = anthropic.Anthropic(api_key=api_key)

            system_prompt = (
                "You are a principal software architect and project planner. Break down the project "
                "requirements into actionable, sequential steps with estimated effort."
            )
            prompt = f"Project: {project_name}\nRequirements: {requirements}"

            structured_data: PlanningOutput = self._call_llm_structured(
                client=client,
                schema_cls=PlanningOutput,
                prompt=prompt,
                system_prompt=system_prompt,
            )

            return AgentResult.ok(
                data=structured_data.model_dump(),
                metadata={"project_name": project_name, "total_steps": len(structured_data.steps)},
            )
        except Exception as e:
            return AgentResult.fail(f"Planning execution failed: {str(e)}")
