import os
import pytest

@pytest.fixture(autouse=True)
def set_dummy_env_vars(monkeypatch):
    """Inyecta la API key en os.environ antes de que se instancien las configuraciones."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "dummy-key-for-tests")
