import anthropic
from config import settings
from agents.result import AgentResult

class ResearchAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=settings.anthropic_api_key or "dummy-key",
            max_retries=settings.anthropic_max_retries
        )
        self.model = settings.anthropic_model

    def run(self, topic: str) -> AgentResult:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": f"Investiga el siguiente tema: {topic}"}]
            )
            
            if not response.content:
                return AgentResult.fail(
                    error="Respuesta vacía o malformada de la API",
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
