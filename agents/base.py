import time
from abc import ABC, abstractmethod
from typing import Any, Optional, Type, TypeVar
import anthropic
from pydantic import BaseModel
from config import get_settings
from agents.result import AgentResult

T = TypeVar("T", bound=BaseModel)


class BaseAgent(ABC):
    name: str = "BaseAgent"

    def __init__(self):
        self.settings = get_settings()

    def _call_llm_with_retry(
        self,
        client: Any,
        model: str,
        messages: list,
        max_tokens: int = 1024,
        system: str = "",
        tools: Optional[list] = None,
        tool_choice: Optional[dict] = None,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ) -> Any:
        """Executes LLM call with retry logic on RateLimitError or APIError."""
        for attempt in range(max_retries):
            try:
                kwargs = {
                    "model": model,
                    "max_tokens": max_tokens,
                    "messages": messages,
                }
                if system:
                    kwargs["system"] = system
                if tools:
                    kwargs["tools"] = tools
                if tool_choice:
                    kwargs["tool_choice"] = tool_choice

                return client.messages.create(**kwargs)
            except (anthropic.RateLimitError, anthropic.APIError) as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(backoff_factor * (2**attempt))

    def _call_llm_structured(
        self,
        schema_cls: Type[T] = None,
        prompt: str = "",
        client: Optional[Any] = None,
        system_prompt: str = "",
        model: str = "claude-3-5-sonnet-20241022",
        **kwargs,
    ) -> T:
        if schema_cls is None and "response_schema" in kwargs:
            schema_cls = kwargs["response_schema"]

        # Only validate API key from settings if a mock client wasn't provided
        if client is None:
            api_key = getattr(self.settings, "anthropic_api_key", None)
            api_key_str = ""
            if api_key and hasattr(api_key, "get_secret_value"):
                api_key_str = api_key.get_secret_value()
            elif api_key:
                api_key_str = str(api_key)

            if not api_key_str:
                raise ValueError("ANTHROPIC_API_KEY is not configured")

        tool_definition = {
            "name": "submit_structured_output",
            "description": f"Submit structured output matching {schema_cls.__name__}",
            "input_schema": schema_cls.model_json_schema(),
        }

        response = self._call_llm_with_retry(
            client=client,
            model=model,
            max_tokens=1024,
            system=system_prompt,
            tools=[tool_definition],
            tool_choice={"type": "tool", "name": "submit_structured_output"},
            messages=[{"role": "user", "content": prompt}],
        )

        for content_block in getattr(response, "content", []):
            if getattr(content_block, "type", None) == "tool_use" and getattr(content_block, "name", None) == "submit_structured_output":
                return schema_cls.model_validate(content_block.input)

        raise ValueError("LLM failed to return structured tool execution output.")

    @abstractmethod
    def run(self, **kwargs) -> AgentResult:
        pass

    def execute(self, **kwargs) -> AgentResult:
        return self.run(**kwargs)
