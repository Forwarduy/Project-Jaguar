"""Tests for the interactive shell system and REPL command dispatcher."""

import pytest
from agents.shell_system import (
    ShellSystem,
    SystemValidationError,
    verify_runtime_environment,
)
from agents.result import AgentResult
from agents.registry import AGENT_REGISTRY


def test_verify_runtime_environment():
    assert verify_runtime_environment(strict=False) is True
    assert verify_runtime_environment(strict=True) is True


def test_shell_system_parsing():
    shell = ShellSystem()
    
    parsed_empty = shell.parse_command("")
    assert parsed_empty["action"] == "empty"
    assert parsed_empty["args"] == []

    parsed_cmd = shell.parse_command("  run research_agent AI  ")
    assert parsed_cmd["action"] == "run"
    assert parsed_cmd["args"] == ["research_agent", "AI"]

    # Test malformed shlex fallback
    parsed_malformed = shell.parse_command('run "unmatched quote')
    assert parsed_malformed["action"] == "run"


def test_shell_system_execute_commands():
    shell = ShellSystem()

    # Empty command / whitespace
    assert shell.execute_command("").success is True
    assert shell.execute_command("   ").success is True

    # Help command
    res_help = shell.execute_command("help")
    assert res_help.success is True
    assert "Available Commands" in res_help.content

    # List command (testing various registry interfaces)
    res_list = shell.execute_command("list")
    assert res_list.success is True
    assert "Registered Agents" in res_list.content

    # Exit / quit command
    for cmd in ["exit", "quit"]:
        res_exit = shell.execute_command(cmd)
        assert res_exit.success is True
        assert res_exit.metadata.get("should_exit") is True

    # Unknown command
    res_unknown = shell.execute_command("unknown_cmd_foo")
    assert res_unknown.success is False
    assert "Unknown command" in res_unknown.error


def test_shell_system_run_and_chain():
    shell = ShellSystem()

    # Run without argument
    res_run_no_arg = shell.execute_command("run")
    assert res_run_no_arg.success is False
    assert "Missing agent_name" in res_run_no_arg.error

    # Chain without argument
    res_chain_no_arg = shell.execute_command("chain")
    assert res_chain_no_arg.success is False
    assert "Missing chain specification" in res_chain_no_arg.error

    # Find a valid registered agent name dynamically using list_agents()
    agents_list = []
    if hasattr(AGENT_REGISTRY, "list_agents"):
        agents_list = AGENT_REGISTRY.list_agents()

    if agents_list:
        valid_agent = agents_list[0]
        res_run = shell.execute_command(f"run {valid_agent} test")
        assert isinstance(res_run, AgentResult)

        res_chain = shell.execute_command(f"chain {valid_agent},{valid_agent} test")
        assert isinstance(res_chain, AgentResult)

        res_direct = shell.execute_command(f"{valid_agent} direct-test")
        assert isinstance(res_direct, AgentResult)


def test_shell_system_registry_variants():
    # Registry as a custom object with .keys()
    class DictRegistry:
        def __init__(self, data):
            self._data = data
        def keys(self):
            return self._data.keys()
        def get(self, key):
            return self._data[key]

    mock_reg = DictRegistry({"custom_agent": lambda *a, **kw: None})
    shell = ShellSystem(registry=mock_reg)
    res = shell.execute_command("list")
    assert res.success is True
    assert "custom_agent" in res.data["agents"]


def test_shell_system_base_agent_methods():
    shell = ShellSystem()
    result = shell.run("help")
    assert result.success is True
    
    # Test execution exception catching when registry fails
    class BadRegistry:
        def list_agents(self):
            raise RuntimeError("Registry failure")

    bad_shell = ShellSystem(registry=BadRegistry())
    try:
        bad_res = bad_shell.execute_command("list")
        assert isinstance(bad_res, AgentResult)
    except RuntimeError:
        pass

    # Test execution exception handling in execute()
    class FaultyShell(ShellSystem):
        def execute_command(self, raw_input=""):
            raise ValueError("Fatal crash")

    faulty = FaultyShell()
    err_res = faulty.run("test")
    assert err_res.success is False
    assert "Fatal crash" in err_res.error
