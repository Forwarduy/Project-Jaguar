from unittest.mock import patch
from config import Settings

@patch.dict("os.environ", {}, clear=True)
def test_settings_defaults():
    settings = Settings()
    assert settings.anthropic_api_key is None
    assert settings.anthropic_model == "claude-sonnet-5"

@patch.dict("os.environ", {"ANTHROPIC_MAX_RETRIES": "5"}, clear=True)
def test_settings_max_retries_override():
    settings = Settings()
    assert settings.anthropic_max_retries == 5
