from abc import ABC, abstractmethod
import json
import time
from typing import Any, Type, TypeVar
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
import anthropic
from pydantic import BaseModel
from config import get_settings
from agents.result import AgentResult

T = TypeVar("T", bound=BaseModel)

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

    def _call_llm_structured(
        self,
        client: anthropic.Anthropic,
        schema_cls: Type[T],
        prompt: str,
        system_prompt: str = "",
        model: str = "claude-3-5-sonnet-20241022",
    ) -> T:
        """Forces Anthropic LLM to return structured data validated against a Pydantic schema."""
        tool_definition = {
            "name": "submit_structured_output",
            "description": f"Submit structured output matching {schema_cls.__name__}",
            "input_schema": schema_cls.model_json_schema(),
        }

        response = self._call_llm_with_retry(
            client,
            model=model,
            max_tokens=1024,
            system=system_prompt,
            tools=[tool_definition],
            tool_choice={"type": "tool", "name": "submit_structured_output"},
            messages=[{"role": "user", "content": prompt}],
        )

        for content_block in response.content:
            if content_block.type == "tool_use" and content_block.name == "submit_structured_output":
                return schema_cls.model_validate(content_block.input)

        raise ValueError("LLM failed to return structured tool execution output.")

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
