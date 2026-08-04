from __future__ import annotations
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-sonnet-5"
    anthropic_max_retries: int = 2
    openai_api_key: Optional[str] = None
    n8n_url: Optional[str] = None
    n8n_api_key: Optional[str] = None

@lru_cache
def get_settings() -> Settings:
    return Settings()
