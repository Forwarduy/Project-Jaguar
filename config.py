from __future__ import annotations
from functools import lru_cache
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_max_retries: int = 2
    openai_api_key: Optional[str] = None
    n8n_url: Optional[str] = None
    n8n_api_key: Optional[str] = None

    @field_validator("anthropic_max_retries", mode="before")
    @classmethod
    def parse_max_retries(cls, v: object) -> int:
        """Asegura que valores vacíos o inválidos no rompan la inicialización."""
        if v is None or v == "":
            return 2
        try:
            return int(v)
        except (ValueError, TypeError):
            return 2


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reload_settings() -> Settings:
    """Limpia el caché y recarga la configuración (útil para tests e integración continua)."""
    get_settings.cache_clear()
    return get_settings()
