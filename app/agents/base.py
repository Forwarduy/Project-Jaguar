from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel
from app.services.anthropic_service import AnthropicService

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)

class BaseAgent(ABC, Generic[InputT, OutputT]):
    def __init__(self, agent_name: str, system_prompt: str):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.anthropic = AnthropicService()

    @abstractmethod
    fmt_input(self, data: dict) -> InputT:
        pass

    def run(self, context_data: dict) -> OutputT:
        validated_input = self.fmt_input(context_data)
        user_prompt = f"Procesa la siguiente entrada de contexto:\n{validated_input.model_dump_json()}"
        
        output_model = self.get_output_schema()
        result = self.anthropic.generate_structured(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            response_model=output_model
        )
        return result

    @abstractmethod
    def get_output_schema(self) -> Type[OutputT]:
        pass
