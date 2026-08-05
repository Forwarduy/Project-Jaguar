"""Application settings and global configuration management."""

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
    ANTHROPIC_API_KEY: str = Field(..., description="API key for Anthropic services")

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


def load_settings() -> Settings:
    """Instantiate and validate global application settings."""
    return Settings()
