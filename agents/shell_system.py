"""Tests for the shell system agent and REPL command dispatcher."""

import pytest
import sys
from unittest.mock import patch, MagicMock

from agents.shell_system import (
    ShellSystem,
    verify_runtime_environment,
    SystemValidationError,
)
from agents.result import AgentResult


def test_verify_runtime_environment():
    """Test Python runtime version validation."""
    # Test strict mode failure (mocking python 3.8)
    with patch("sys.version_info", (3, 8)):
        with pytest.raises(SystemValidationError, match="Python 3.9 or higher is required."):
            verify_runtime_environment(strict=True)
        assert not verify_runtime_environment(strict=False)

    # Test success (mocking python 3.10)
    with patch("sys.version_info", (3, 10)):
        assert verify_runtime_environment(strict=True)
        assert verify_runtime_environment(strict=False)


def test_shell_system_initialization():
    """Test standard initialization."""
    shell = ShellSystem()
    assert shell.name == "shell_system"
    assert shell.registry is not None


def test_shell_system_parse_command():
    """Test the parsing of raw user input."""
    shell = ShellSystem()
    
    assert shell.parse_command("") == {"action": "empty", "args": []}
    assert shell.parse_command("   ") == {"action": "empty", "args": []}
    assert shell.parse_command("help") == {"action": "help", "args": []}
    assert shell.parse_command("run agent1 data") == {"action": "run", "args": ["agent1", "data"]}
    
    # Test shlex error fallback (unmatched quotes raise ValueError in shlex)
    # The method catches ValueError and uses a simple split() instead.
    assert shell.parse_command("run agent 'missing quote") == {
        "action": "run",
        "args": ["agent", "'missing", "quote"],
    }


def test_shell_system_execute_command_empty():
    """Test execution of an empty command."""
    shell = ShellSystem()
    res = shell.execute_command("")
    assert res.success is True
    assert res.metadata["action"] == "empty"


def test_shell_system_execute_command_exit():
    """Test 'exit' and 'quit' commands."""
    shell = ShellSystem()
    for cmd in ["exit", "quit"]:
        res = shell.execute_command(cmd)
        assert res.success is True
        assert res.metadata["should_exit"] is True


def test_shell_system_execute_command_help():
    """Test the 'help' command."""
    shell = ShellSystem()
    res = shell.execute_command("help")
    assert res.success is True
    assert "Available Commands:" in res.content


def test_shell_system_execute_command_list():
    """Test the 'list' command across different registry shapes."""
    # Mocking registry with list_agents method
    registry_mock = MagicMock()
    registry_mock.list_agents.return_value = ["agent1", "agent2"]
    shell = ShellSystem(registry=registry_mock)
    res = shell.execute_command("list")
    assert res.success is True
    assert "agent1" in res.content

    # Mocking registry as dict
    registry_dict = {"agentA": 1, "agentB": 2}
    shell2 = ShellSystem(registry=registry_dict)
    res2 = shell2.execute_command("list")
    assert res2.success is True
    assert "agentA" in res2.content
    
    # Test empty registry
    shell3 = ShellSystem(registry={})
    res3 = shell3.execute_command("list")
    assert "No agents registered." in res3.content


@patch("agents.shell_system.AgentPipeline")
def test_shell_system_execute_command_run(mock_pipeline):
    """Test the 'run' command."""
    mock_pipeline_instance = MagicMock()
    mock_pipeline_instance.run_chain.return_value = AgentResult.ok(content="run success")
    mock_pipeline.return_value = mock_pipeline_instance
    
    shell = ShellSystem()
    
    # Missing args
    res = shell.execute_command("run")
    assert res.success is False
    assert "Usage: run <agent_name>" in res.content
    
    # Valid args
    res2 = shell.execute_command("run myagent some input")
    mock_pipeline_instance.run_chain.assert_called_with(chain_spec="myagent", initial_input="some input")
    assert res2.success is True


@patch("agents.shell_system.AgentPipeline")
def test_shell_system_execute_command_chain(mock_pipeline):
    """Test the 'chain' command."""
    mock_pipeline_instance = MagicMock()
    mock_pipeline_instance.run_chain.return_value = AgentResult.ok(content="chain success")
    mock_pipeline.return_value = mock_pipeline_instance
    
    shell = ShellSystem()
    
    # Missing args
    res = shell.execute_command("chain")
    assert res.success is False
    assert "Usage: chain <agent1,agent2,...>" in res.content
    
    # Valid args
    res2 = shell.execute_command("chain a1,a2 input data")
    mock_pipeline_instance.run_chain.assert_called_with(chain_spec="a1,a2", initial_input="input data")
    assert res2.success is True


@patch("agents.shell_system.AgentPipeline")
def test_shell_system_execute_command_direct_agent(mock_pipeline):
    """Test running an agent by directly typing its name."""
    mock_pipeline_instance = MagicMock()
    mock_pipeline_instance.run_chain.return_value = AgentResult.ok(content="direct success")
    mock_pipeline.return_value = mock_pipeline_instance
    
    registry = {"myagent": MagicMock()}
    shell = ShellSystem(registry=registry)
    
    res = shell.execute_command("myagent some data")
    mock_pipeline_instance.run_chain.assert_called_with(chain_spec="myagent", initial_input="myagent some data")
    assert res.success is True


def test_shell_system_execute_command_unknown():
    """Test unknown commands."""
    shell = ShellSystem(registry={})
    res = shell.execute_command("unknowncmd")
    assert res.success is False
    assert "Unknown command: 'unknowncmd'" in res.content


def test_shell_system_execute_exceptions():
    """Test exception handling during execution."""
    shell = ShellSystem()
    with patch.object(shell, "execute_command", side_effect=ValueError("Test error")):
        res = shell.execute("help")
        assert res.success is False
        assert "Test error" in res.error


def test_shell_system_run():
    """Test that run method maps correctly to execute."""
    shell = ShellSystem()
    with patch.object(shell, "execute", return_value=AgentResult.ok(content="run OK")):
        res = shell.run("help")
        assert res.success is True
        assert res.content == "run OK"
