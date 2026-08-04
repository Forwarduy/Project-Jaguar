import anthropic
from .base import BaseAgent
from .result import AgentResult
from config import get_settings


class ResearchAgent(BaseAgent):
    """Agente encargado de realizar investigación de mercado utilizando Claude."""

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

    def run(self, topic: str, **kwargs) -> AgentResult:
        if not self.client:
            return AgentResult.fail("ANTHROPIC_API_KEY not found in environment or .env file")
        
        clean_topic = topic.strip() if topic else ""
        if not clean_topic:
            return AgentResult.fail("topic cannot be empty")

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"You are a market research analyst. Research: {clean_topic}. Give 3 concise insights.",
                    }
                ],
            )

            if not message.content:
                return AgentResult.fail("Empty response from Anthropic API")

            # Extracción segura de texto procesando los bloques de respuesta
            text_outputs = [
                block.text for block in message.content if getattr(block, "type", None) == "text"
            ]

            if not text_outputs:
                return AgentResult.fail("No text block received in model response")

            return AgentResult.ok("\n".join(text_outputs))

        except anthropic.APIError as e:
            return AgentResult.fail(f"Claude API Error: {str(e)}")
        except Exception as e:
            return AgentResult.fail(f"Unexpected error: {str(e)}")
