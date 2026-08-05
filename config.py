"""Application settings and global configuration management."""

from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Central configuration class backed by environment variables."""

    PROJECT_NAME: str = "Project-Jaguar"
    ENVIRONMENT: str = Field(default="development", description="env stage")
    DEBUG: bool = Field(default=False)

    # API Configuration
    ANTHROPIC_API_KEY: str = Field(
        default="dummy_key_for_tests", description="API key for Anthropic services"
    )

    # Execution defaults
    DEFAULT_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.2
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Retrieve cached global settings instance (expected by agents/base.py)."""
    return Settings()


# Alias load_settings for backwards compatibility and CLI loader
load_settings = get_settings
