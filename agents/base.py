from abc import ABC, abstractmethod
import logging
from typing import Any, Optional
from config import get_settings
from agents.result import AgentResult

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Clase base para todos los agentes de Project-Jaguar."""

    name: str = "base_agent"
    description: str = "Base agent implementation"

    def __init__(self, api_key: Optional[str] = None):
        settings = get_settings()
        self.api_key = api_key or getattr(settings, "anthropic_api_key", None)

    def _validate_api_key(self) -> Optional[AgentResult]:
        if not self.api_key:
            return AgentResult(
                success=False,
                content="",
                error="ANTHROPIC_API_KEY not found in environment or .env file",
            )
        return None

    @abstractmethod
    def _execute(self, prompt: str, **kwargs: Any) -> AgentResult:
        """Lógica concreta que debe implementar cada agente."""
        pass

    def run(self, prompt: str, **kwargs: Any) -> AgentResult:
        """Punto de entrada principal con validaciones base."""
        key_error = self._validate_api_key()
        if key_error:
            return key_error

        if not prompt or not prompt.strip():
            return AgentResult(
                success=False,
                content="",
                error="Input prompt/topic cannot be empty",
            )

        try:
            return self._execute(prompt.strip(), **kwargs)
        except Exception as e:
            logger.exception(f"Error inesperado ejecutando {self.name}: {e}")
            return AgentResult(
                success=False,
                content="",
                error=f"Unhandled agent error: {str(e)}",
            )
