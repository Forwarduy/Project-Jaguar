from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()  # carga .env en variables de entorno reales, una sola vez


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-5"  # claude-3-5-sonnet-20241022 fue retirado el 28/10/2025
    anthropic_max_retries: int = 2  # mismo default que el SDK: reintenta rate limits/conexión/5xx con backoff
    openai_api_key: str | None = None
    n8n_url: str | None = None
    n8n_api_key: str | None = None


def get_settings() -> Settings:
    return Settings()
