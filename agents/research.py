import logging
from typing import Any
import anthropic
from agents.base import BaseAgent
from agents.result import AgentResult

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    name: str = "research"
    description: str = "Agente especializado en investigación y análisis de temas."

    def _execute(self, prompt: str, **kwargs: Any) -> AgentResult:
        if not prompt or not prompt.strip():
            return AgentResult(
                success=False,
                content="",
                error="Topic cannot be empty",
            )

        client = anthropic.Anthropic(api_key=self.api_key)

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"Realiza una investigación sobre: {prompt}",
                    }
                ],
            )

            if not response.content:
                return AgentResult(
                    success=False,
                    content="",
                    error="Malformed API response: no text block or content empty",
                )

            text_content = response.content[0].text
            return AgentResult(
                success=True,
                content=text_content,
                metadata={"model": response.model},
            )

        except anthropic.RateLimitError as e:
            logger.warning(f"Rate limit alcanzado en {self.name}: {e}")
            return AgentResult(
                success=False,
                content="",
                error=f"Rate limit exceeded (429): {str(e)}",
            )
        except anthropic.InternalServerError as e:
            logger.error(f"Error de servidor Anthropic en {self.name}: {e}")
            return AgentResult(
                success=False,
                content="",
                error=f"Anthropic server error (529): {str(e)}",
            )
        except anthropic.APIConnectionError as e:
            logger.error(f"Error de conexión en {self.name}: {e}")
            return AgentResult(
                success=False,
                content="",
                error=f"API connection failure: {str(e)}",
            )
        except Exception as e:
            return AgentResult(
                success=False,
                content="",
                error=f"API error: {str(e)}",
            )
