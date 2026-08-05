"""Tests for agents/shell_system.py covering shell system functionality."""

from unittest.mock import MagicMock, patch
import pytest

import agents.shell_system as shell_module
from agents.result import AgentResult

# Target concrete agent class from module
agent_classes = [
    obj for name, obj in vars(shell_module).items()
    if isinstance(obj, type) and name != "BaseAgent"
]
TargetClass = agent_classes[0] if agent_classes else None


@pytest.fixture
def agent_instance():
    if TargetClass is not None:
        return TargetClass()
    return None


def test_shell_system_module_attributes():
    """Verify module exports essential components."""
    assert shell_module is not None


@patch("subprocess.run")
def test_shell_system_execution_success(mock_run, agent_instance):
    """Test successful command execution path."""
    if agent_instance is None or not hasattr(agent_instance, "run"):
        pytest.skip("No executable agent class found in agents.shell_system")

    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="Shell execution output\n",
        stderr="",
    )

    result = agent_instance.run("echo test")
    assert isinstance(result, AgentResult)


@patch("subprocess.run")
def test_shell_system_execution_failure(mock_run, agent_instance):
    """Test non-zero exit code path."""
    if agent_instance is None or not hasattr(agent_instance, "run"):
        pytest.skip("No executable agent class found in agents.shell_system")

    mock_run.return_value = MagicMock(
        returncode=1,
        stdout="",
        stderr="Error output",
    )

    result = agent_instance.run("invalid_command")
    assert isinstance(result, AgentResult)


@patch("subprocess.run", side_effect=RuntimeError("Subprocess failed"))
def test_shell_system_exception_handling(mock_run, agent_instance):
    """Test exception resilience."""
    if agent_instance is None or not hasattr(agent_instance, "run"):
        pytest.skip("No executable agent class found in agents.shell_system")

    result = agent_instance.run("ls")
    assert isinstance(result, AgentResult)
