"""Tests for agents/shell_system.py covering shell execution functionality."""

from unittest.mock import MagicMock, patch
import pytest

from agents.result import AgentResult
from agents.shell_system import ShellSystemAgent


@pytest.fixture
def shell_agent():
    return ShellSystemAgent()


def test_shell_agent_initialization(shell_agent):
    """Test standard initialization of ShellSystemAgent."""
    assert shell_agent.description is not None


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
    assert result.error is not None or "Command not found" in result.content


@patch("subprocess.run", side_effect=Exception("Subprocess exception"))
def test_shell_agent_exception_handling(mock_run, shell_agent):
    """Test shell agent handling execution exceptions cleanly."""
    result = shell_agent.run("ls")

    assert isinstance(result, AgentResult)
    assert result.success is False
    assert "Subprocess exception" in str(result.error or result.content)
