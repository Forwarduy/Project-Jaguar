"""Application settings and global configuration management."""

from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Central configuration class backed by environment variables."""

    project_name: str = "Project-Jaguar"
    environment: str = Field(default="development", description="env stage")
    debug: bool = Field(default=False)

    # API Configuration
    anthropic_api_key: Optional[str] = Field(
        default=None, description="API key for Anthropic services"
    )
    anthropic_max_retries: int = Field(
        default=2, description="Max retries for Anthropic client calls"
    )

    # Execution defaults
    default_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 0.2
    log_level: str = "INFO"

    # Uppercase aliases for environment variable access compatibility
    @property
    def ANTHROPIC_API_KEY(self) -> Optional[str]:
        return self.anthropic_api_key

    @property
    def ENVIRONMENT(self) -> str:
        return self.environment

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Instantiate and cache global application settings."""
    return Settings()


# Module-level alias expected by some imports
load_settings = get_settings
