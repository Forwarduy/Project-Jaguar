from abc import ABC, abstractmethod
from typing import Any, Dict
from config import get_settings
from agents.result import AgentResult


class BaseAgent(ABC):
    def __init__(self) -> None:
        self.settings = get_settings()
        self.model = self.settings.anthropic_model

    def execute(self, **kwargs: Any) -> AgentResult:
        if not self.settings.anthropic_api_key:
            return AgentResult(
                success=False,
                error="ANTHROPIC_API_KEY is not configured",
                data=None,
            )
        try:
            return self._execute(**kwargs)
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                data=None,
            )

    @abstractmethod
    def _execute(self, **kwargs: Any) -> AgentResult:
        pass
