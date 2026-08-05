from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.result import AgentResult

class OutreachAgent(BaseAgent):
    """Agent responsible for drafting outreach communication."""

    def run(self, recipient: str, message_context: str = "", **kwargs: Any) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult.fail("ANTHROPIC_API_KEY is not configured", metadata={"recipient": recipient})

        try:
            client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
            prompt = f"Draft a professional outreach message to {recipient}."
            if message_context:
                prompt += f" Context/Goal: {message_context}"

            response = client.messages.create(
                model=self.settings.anthropic_model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            if not response.content or not hasattr(response.content[0], "text"):
                return AgentResult.fail("Empty or malformed response from Anthropic API", metadata={"recipient": recipient})

            content = response.content[0].text
            return AgentResult.ok(
                content=content,
                data={"message": content, "recipient": recipient},
                metadata={"recipient": recipient, "has_context": bool(message_context)},
            )

        except Exception as e:
            return AgentResult.fail(str(e), metadata={"recipient": recipient})
