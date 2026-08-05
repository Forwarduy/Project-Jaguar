"""Base agent interface and core execution definitions with LLM integration support."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel
from agents.result import AgentResult
from config import get_settings


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

    def _call_llm_structured(
        self,
        client: Any,
        schema_cls: Type[BaseModel],
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
    ) -> BaseModel:
        """Helper to invoke an LLM and enforce structured JSON output using tool use / schemas."""
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")

        target_model = model or settings.anthropic_model

        messages = [{"role": "user", "content": prompt}]
        tools = [
            {
                "name": "submit_structured_output",
                "description": "Submit the required structured output.",
                "input_schema": schema_cls.schema(),
            }
        ]

        response = client.messages.create(
            model=target_model,
            max_tokens=4096,
            system=system_prompt or "You are a professional enterprise assistant.",
            messages=messages,
            tools=tools,
            tool_choice={"type": "tool", "name": "submit_structured_output"},
        )

        for content_block in response.content:
            if getattr(content_block, "type", None) == "tool_use" and content_block.name == "submit_structured_output":
                return schema_cls(**content_block.input)

        raise ValueError("Model failed to return structured output via tool use.")
