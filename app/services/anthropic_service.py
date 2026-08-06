import os
import json
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from anthropic import Anthropic

T = TypeVar("T", bound=BaseModel)

class AnthropicService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("La variable de entorno ANTHROPIC_API_KEY no está configurada.")
        self.client = Anthropic(api_key=self.api_key)
        self.default_model = "claude-3-5-sonnet-20241022"

    def generate_text(self, system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
        response = self.client.messages.create(
            model=self.default_model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text

    def generate_structured(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_model: Type[T], 
        max_tokens: int = 4000
    ) -> T:
        # Forzar a Claude a responder con un JSON válido estructurado según el esquema Pydantic
        json_instruction = (
            f"\n\nResponde ÚNICAMENTE con un objeto JSON válido que cumpla estrictamente "
            f"con el siguiente esquema de Pydantic:\n{response_model.model_json_schema()}"
        )
        
        full_system = system_prompt + json_instruction
        raw_response = self.generate_text(full_system, user_prompt, max_tokens)
        
        # Limpieza defensiva de bloques de código markdown si los hubiera
        cleaned_response = raw_response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
            
        data = json.loads(cleaned_response.strip())
        return response_model.model_validate(data)
