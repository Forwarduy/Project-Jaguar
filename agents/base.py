from abc import ABC, abstractmethod
from typing import Any
from config import get_settings
from agents.result import AgentResult


class BaseAgent(ABC):
    def __init__(self) -> None:
        self.settings = get_settings()
        self.model = self.settings.anthropic_model

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def execute(self, **kwargs: Any) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult(
                success=False,
                error="ANTHROPIC_API_KEY is not configured",
            )
        try:
            return self._execute(**kwargs)
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
            )

    def run(self, topic: str = "General Research", **kwargs: Any) -> AgentResult:
        """Alias para mantener compatibilidad con llamadas legacy en test_resilience."""
        return self.execute(topic=topic, **kwargs)

    @abstractmethod
    def _execute(self, **kwargs: Any) -> AgentResult:
        pass
