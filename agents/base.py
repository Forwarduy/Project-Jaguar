# agents/base.py
from abc import ABC, abstractmethod
from typing import Type, TypeVar
from pydantic import BaseModel
from config import get_settings
from agents.result import AgentResult

T = TypeVar("T", bound=BaseModel)


class BaseAgent(ABC):
    def __init__(self):
        self.settings = get_settings()

    def _call_llm_structured(self, prompt: str, response_schema: Type[T]) -> T:
        raise NotImplementedError("Subclasses or mocks must implement _call_llm_structured")

    @abstractmethod
    def run(self, **kwargs) -> AgentResult:
        """Abstract execution method required by BaseAgent interface."""
        pass
