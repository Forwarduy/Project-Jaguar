import anthropic
from .base import BaseAgent
from config import get_settings


class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ResearchAgent")
        settings = get_settings()
        self.model = settings.anthropic_model
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None

    def run(self, topic: str) -> str:
        if not self.client:
            return "❌ Error: ANTHROPIC_API_KEY not found in .env"
        if not topic or not topic.strip():
            return "❌ Error: topic cannot be empty"
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
                return "⚠️ Empty response from model"
            return message.content[0].text
        except anthropic.APIError as e:
            return f"❌ Claude API Error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
