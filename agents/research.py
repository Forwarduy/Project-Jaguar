import anthropic
from config import get_settings
from agents.base import BaseAgent
from agents.result import AgentResult

class ResearchAgent(BaseAgent):
    name: str = "ResearchAgent"

    def __init__(self):
        super().__init__()
        api_key = self.settings.anthropic_api_key or ""
        self.client = anthropic.Anthropic(
            api_key=api_key or "dummy-key",
            max_retries=self.settings.anthropic_max_retries
        )
        self.model = self.settings.anthropic_model

    def run(self, topic: str, **kwargs) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult.fail(
                error="API key is missing or empty",
                metadata={"topic": topic}
            )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": f"Investiga el siguiente tema: {topic}"}]
            )
            
            if not response.content:
                return AgentResult.fail(
                    error="Empty response or no text block returned from API",
                    metadata={"topic": topic}
                )

            content = response.content[0].text
            return AgentResult.ok(
                content=content,
                metadata={"topic": topic}
            )
        except Exception as e:
            return AgentResult.fail(
                error=str(e),
                metadata={"topic": topic}
            )
