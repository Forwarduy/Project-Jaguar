"""Base agent interface and core execution definitions."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from agents.result import AgentResult


class BaseAgent(ABC):
    """Abstract base class for all Project Jaguar agents."""

    def __init__(self, name: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.name = name or self.__class__.__name__
        self.config = config or {}

    @abstractmethod
    def run(self, input_data: Any = None) -> AgentResult:
        """Execute the agent's primary logic."""
        pass

    def execute(self, input_data: Any = None) -> AgentResult:
        """Wrapper for execution matching alternative signatures with error catching."""
        try:
            return self.run(input_data)
        except Exception as e:
            return AgentResult.fail(content=f"Agent execution failed: {str(e)}", error=str(e))
