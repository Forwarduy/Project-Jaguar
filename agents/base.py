from abc import ABC, abstractmethod
import time
from typing import Any
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
import anthropic
from config import get_settings
from agents.result import AgentResult

class BaseAgent(ABC):
    """Abstract base class for all agents with built-in retry logic and metrics."""

    name: str = "BaseAgent"

    def __init__(self) -> None:
        self.settings = get_settings()

    @abstractmethod
    def run(self, **kwargs: Any) -> AgentResult:
        """Core execution logic to be implemented by individual agents."""
        pass

    @retry(
        retry=retry_if_exception_type((anthropic.APIConnectionError, anthropic.RateLimitError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _call_llm_with_retry(self, client: anthropic.Anthropic, **kwargs: Any) -> Any:
        """Helper method to invoke LLM API calls with exponential backoff."""
        return client.messages.create(**kwargs)

    def execute(self, **kwargs: Any) -> AgentResult:
        """Execution wrapper that handles performance metrics and exceptions."""
        start_time = time.perf_counter()
        try:
            result = self.run(**kwargs)
            execution_time = round(time.perf_counter() - start_time, 4)
            if result.metadata is not None:
                result.metadata["execution_time_seconds"] = execution_time
            return result
        except Exception as e:
            execution_time = round(time.perf_counter() - start_time, 4)
            return AgentResult.fail(
                error=f"Unhandled exception in {self.name}: {str(e)}",
                metadata={"execution_time_seconds": execution_time},
            )
