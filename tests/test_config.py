"""Tests para la configuración centralizada."""
from unittest.mock import patch

from config import Settings


@patch.dict("os.environ", {}, clear=True)
def test_settings_defaults():
    settings = Settings()
    assert settings.anthropic_api_key is None
    assert settings.anthropic_model == "claude-sonnet-5"


@patch.dict("os.environ", {"ANTHROPIC_API_KEY": "abc123", "ANTHROPIC_MODEL": "claude-opus-4-8"}, clear=True)
def test_settings_reads_env_vars():
    settings = Settings()
    assert settings.anthropic_api_key == "abc123"
    assert settings.anthropic_model == "claude-opus-4-8"
