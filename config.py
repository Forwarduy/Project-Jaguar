# tests/test_config.py
from unittest.mock import patch
from config import Settings

@patch.dict("os.environ", {}, clear=True)
def test_settings_defaults():
    settings = Settings()
    assert settings.anthropic_api_key is None
    assert settings.anthropic_model == "claude-3-7-sonnet-20250219"
