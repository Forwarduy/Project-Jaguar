from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.registry import AGENT_REGISTRY
from agents.result import AgentResult
from agents.schemas import ResearchOutput


@AGENT_REGISTRY.register("research")
class ResearchAgent(BaseAgent):
    """Agent responsible for gathering and synthesizing technical research."""

    name: str = "ResearchAgent"

    def run(self, topic: str = "", **kwargs: Any) -> AgentResult:
        if not topic:
            return AgentResult.fail("Parameter 'topic' is required for ResearchAgent.")

        if not self.settings.anthropic_api_key or not getattr(self.settings.anthropic_api_key, "get_secret_value", lambda: self.settings.anthropic_api_key)():
            return AgentResult.fail("ANTHROPIC_API_KEY is not configured")

        try:
            api_key = self.settings.anthropic_api_key.get_secret_value() if hasattr(self.settings.anthropic_api_key, "get_secret_value") else self.settings.anthropic_api_key
            client = anthropic.Anthropic(api_key=api_key)

            system_prompt = (
                "You are an expert technical researcher. Analyze the given topic thoroughly "
                "and provide key findings, potential sources, and a confidence score."
            )
            prompt = f"Research the following topic in detail: {topic}"

            structured_data: ResearchOutput = self._call_llm_structured(
                client=client,
                schema_cls=ResearchOutput,
                prompt=prompt,
                system_prompt=system_prompt,
            )

            return AgentResult.ok(
                data=structured_data.model_dump(),
                metadata={"topic": topic, "model_used": self.settings.anthropic_model},
            )
        except Exception as e:
            return AgentResult.fail(f"Research execution failed: {str(e)}")
