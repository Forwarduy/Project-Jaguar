import anthropic
from .base import BaseAgent
from .result import AgentResult
from config import get_settings


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ResearchAgent")
        settings = get_settings()
        self.model = settings.anthropic_model
        self.client = (
            anthropic.Anthropic(
                api_key=settings.anthropic_api_key,
                max_retries=settings.anthropic_max_retries,
            )
            if settings.anthropic_api_key
            else None
        )

    def run(self, topic: str) -> AgentResult:
        if not self.client:
            return AgentResult.fail("ANTHROPIC_API_KEY not found in .env")
        if not topic or not topic.strip():
            return AgentResult.fail("topic cannot be empty")
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a market research analyst. Research: {topic}. Give 3 insights.",
                    }
                ],
            )
            if not message.content:
                return AgentResult.fail("Empty response from model")
            return AgentResult.ok(message.content[0].text)
        except anthropic.APIError as e:
            return AgentResult.fail(f"Claude API Error: {str(e)}")
        except Exception as e:
            return AgentResult.fail(f"Unexpected error: {str(e)}")
