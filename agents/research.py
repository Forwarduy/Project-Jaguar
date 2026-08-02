import os
import anthropic
from dotenv import load_dotenv
from.base import BaseAgent

load_dotenv()

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ResearchAgent")
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def run(self, topic: str) -> str:
        """Run real research with Claude"""
        if not os.getenv("ANTHROPIC_API_KEY"):
            return "❌ Error: ANTHROPIC_API_KEY not found in.env"

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a market research analyst. Research this topic and give 3 key insights with sources: {topic}"
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Claude API Error: {str(e)}"
