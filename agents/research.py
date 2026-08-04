import anthropic
from typing import Optional, Any
from .base import BaseAgent
from .result import AgentResult
from config import get_settings


class ResearchAgent(BaseAgent):
    """Agente encargado de realizar investigación de mercado utilizando Claude."""

    def __init__(self, model: Optional[str] = None):
        super().__init__(name="ResearchAgent")
        self._custom_model = model

    @property
    def settings(self):
        return get_settings()

    @property
    def model(self) -> str:
        return self._custom_model or self.settings.anthropic_model

    def _get_client(self) -> Optional[anthropic.Anthropic]:
        api_key = self.settings.anthropic_api_key
        if not api_key:
            return None
        
        max_retries = int(self.settings.anthropic_max_retries) if self.settings.anthropic_max_retries is not None else 2
        return anthropic.Anthropic(
            api_key=api_key,
            max_retries=max_retries,
        )

    def run(self, topic: str, **kwargs: Any) -> AgentResult:
        client = self._get_client()
        if not client:
            return AgentResult.fail("ANTHROPIC_API_KEY not found in environment or .env file")
        
        clean_topic = topic.strip() if topic else ""
        if not clean_topic:
            return AgentResult.fail("topic cannot be empty")

        # Extracción de parámetros opcionales
        max_tokens = kwargs.get("max_tokens", 1024)
        temperature = kwargs.get("temperature", 0.7)
        system_prompt = kwargs.get(
            "system", 
            "You are a market research analyst. Provide concise, highly structured insights."
        )

        try:
            message = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Research topic: {clean_topic}. Give 3 concise insights.",
                    }
                ],
            )

            if not message.content:
                return AgentResult.fail("Empty response from Anthropic API")

            # Extracción segura de texto procesando los bloques de respuesta
            text_outputs = [
                block.text for block in message.content 
                if getattr(block, "type", None) == "text" and hasattr(block, "text")
            ]

            if not text_outputs:
                return AgentResult.fail("No text block received in model response")

            return AgentResult.ok("\n".join(text_outputs))

        except anthropic.APIError as e:
            return AgentResult.fail(f"Claude API Error: {str(e)}")
        except Exception as e:
            return AgentResult.fail(f"Unexpected error: {str(e)}")
