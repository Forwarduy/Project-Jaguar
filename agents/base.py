"""Abstract base class interface for all Project-Jaguar agents."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Type, TypeVar
from config import Settings, get_settings
from agents.result import AgentResult

T = TypeVar("T")


class BaseAgent(ABC):
    """Base abstract agent class.

    Subclasses must allow initialization without positional arguments to ensure
    registry factories can instantiate them seamlessly.
    """

    def __init__(self, description: str = "Base Agent"):
        self.description = description

    @property
    def settings(self) -> Settings:
        """Provides access to application configuration."""
        return get_settings()

    @abstractmethod
    def run(self, input_data: str = "", **kwargs: Any) -> AgentResult:
        """Executes the agent's core responsibility and returns an AgentResult."""
        pass

    def execute(self, **kwargs: Any) -> AgentResult:
        """Execution wrapper providing backwards compatibility across test suites."""
        return self.run(**kwargs)

    def _call_llm_structured(
        self,
        schema_cls: Optional[Type[T]] = None,
        prompt: str = "",
        client: Optional[Any] = None,
        system_prompt: str = "",
        model: str = "claude-3-5-sonnet-20241022",
        **kwargs: Any,
    ) -> T:
        """Helper method for structured LLM calls used by domain agents."""
        if schema_cls is None and "response_schema" in kwargs:
            schema_cls = kwargs["response_schema"]

        if client is None:
            api_key = getattr(self.settings, "anthropic_api_key", None)
            api_key_str = ""
            if api_key and hasattr(api_key, "get_secret_value"):
                api_key_str = api_key.get_secret_value()
            elif api_key:
                api_key_str = str(api_key)

            if not api_key_str:
                raise ValueError("ANTHROPIC_API_KEY is not configured")

        if client and hasattr(client, "messages"):
            response = client.messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                system=system_prompt,
                **kwargs,
            )
            for block in getattr(response, "content", []):
                if getattr(block, "type", None) == "tool_use":
                    tool_input = getattr(block, "input", {})
                    if schema_cls:
                        return schema_cls(**tool_input)
                    return tool_input

        raise NotImplementedError("LLM provider integration requires an active client or mock adapter.")
