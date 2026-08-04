from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.result import AgentResult


class ResearchAgent(BaseAgent):
    def _execute(self, **kwargs: Any) -> AgentResult:
        topic = kwargs.get("topic", "General Research")
        
        client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
        
        response = client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"Perform research on the following topic: {topic}",
                }
            ],
        )

        content = response.content[0].text if response.content else ""
        return AgentResult(
            success=True,
            data={"research": content, "topic": topic},
            error=None,
        )
