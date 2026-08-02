import os
import anthropic
from dotenv import load_dotenv
from.base import BaseAgent

load_dotenv()

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ResearchAgent")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else None

    def run(self, topic: str) -> str:
        if not self.client:
            return "❌ Error: ANTHROPIC_API_KEY not found in.env (expected in CI, this is ok for test)"
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"You are a market research analyst. Research: {topic}. Give 3 insights."}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Claude API Error: {str(e)}"
