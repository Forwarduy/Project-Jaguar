from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    anthropic_api_key: str | None = None
    # Identificador válido de la API de Anthropic
    anthropic_model: str = "claude-3-7-sonnet-20250219"
    anthropic_max_retries: int = 2
    openai_api_key: str | None = None
    n8n_url: str | None = None
    n8n_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Retorna una instancia singleton cacheada de las configuraciones."""
    return Settings()
