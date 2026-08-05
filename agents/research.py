from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.result import AgentResult

class ResearchAgent(BaseAgent):
    """Agent responsible for conducting research on a given topic."""

    name: str = "ResearchAgent"

    def run(self, topic: str, **kwargs: Any) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult.fail("ANTHROPIC_API_KEY is not configured", metadata={"topic": topic})

        try:
            client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
            prompt = f"Perform research on the following topic: {topic}"

            response = client.messages.create(
                model=self.settings.anthropic_model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            if not response.content or not hasattr(response.content[0], "text"):
                return AgentResult.fail("Empty or malformed response from Anthropic API", metadata={"topic": topic})

            content = response.content[0].text
            return AgentResult.ok(
                content=content,
                data={"research": content, "topic": topic},
                metadata={"topic": topic},
            )

        except Exception as e:
            return AgentResult.fail(str(e), metadata={"topic": topic})
