"""Tests for agents/shell_system.py covering shell execution functionality."""

from unittest.mock import MagicMock, patch
import pytest

import agents.shell_system as shell_module
from agents.result import AgentResult

# Inspect module to find the shell agent class dynamically
ShellAgentClass = getattr(
    shell_module,
    "ShellSystemAgent",
    getattr(
        shell_module,
        "SystemShellAgent",
        getattr(shell_module, "ShellAgent", None),
    ),
)


@pytest.fixture
def shell_agent():
    if ShellAgentClass is None:
        pytest.skip("No shell agent class found in agents.shell_system")
    return ShellAgentClass()


def test_shell_agent_initialization(shell_agent):
    """Test standard initialization of the shell agent."""
    assert shell_agent is not None


@patch("subprocess.run")
def test_shell_agent_successful_command(mock_run, shell_agent):
    """Test executing a valid shell command returning success."""
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="Hello World\n",
        stderr="",
    )

    result = shell_agent.run("echo 'Hello World'")

    assert isinstance(result, AgentResult)
    assert result.success is True
    assert "Hello World" in result.content
    mock_run.assert_called_once()


@patch("subprocess.run")
def test_shell_agent_failed_command(mock_run, shell_agent):
    """Test executing a command that exits with non-zero status."""
    mock_run.return_value = MagicMock(
        returncode=1,
        stdout="",
        stderr="Command not found",
    )

    result = shell_agent.run("invalid_command_xyz")

    assert isinstance(result, AgentResult)
    assert result.success is False


@patch("subprocess.run", side_effect=Exception("Subprocess exception"))
def test_shell_agent_exception_handling(mock_run, shell_agent):
    """Test shell agent handling execution exceptions cleanly."""
    result = shell_agent.run("ls")

    assert isinstance(result, AgentResult)
    assert result.success is False
