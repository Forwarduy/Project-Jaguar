"""Tests for CLI commands and shell interfaces in main.py."""

from unittest.mock import MagicMock, patch
import pytest
from typer.testing import CliRunner

from main import app, AGENT_REGISTRY
from agents.base import BaseAgent
from agents.result import AgentResult
from agents.shell_system import SystemValidationError

runner = CliRunner()


class MockAgent(BaseAgent):
    """Mock agent for CLI testing."""

    def __init__(self, name: str = "mock"):
        super().__init__(name=name, description="Mock agent")

    def run(self, topic: str, **kwargs) -> AgentResult:
        ctx = kwargs.get("message_context")
        content = f"Result for {topic}" + (f" with ctx {ctx}" if ctx else "")
        return AgentResult(success=True, content=content, agent_name=self.name)


def test_main_callback():
    """Test global callback execution without subcommand."""
    res = runner.invoke(app, [])
    assert res.exit_code == 0
    assert "Project-Jaguar Multi-Agent Shell Engine" in res.output


def test_hello_command():
    """Test hello command."""
    res = runner.invoke(app, ["hello"])
    assert res.exit_code == 0
    assert "Project Jaguar CLI operational." in res.output


def test_health_command_success():
    """Test health command under normal operation."""
    with patch("main.verify_runtime_environment"):
        res = runner.invoke(app, ["health"])
        assert res.exit_code == 0
        assert "Status: Operational" in res.output


def test_health_command_failure():
    """Test health command when validation fails."""
    with patch("main.verify_runtime_environment", side_effect=SystemValidationError("Env error")):
        res = runner.invoke(app, ["health"])
        assert res.exit_code != 0
        assert "Error: Env error" in res.output


def test_list_agents_populated():
    """Test agents command when agents are present in registry."""
    with patch.object(AGENT_REGISTRY, "list_agents", return_value=["research", "plan"]):
        res = runner.invoke(app, ["agents"])
        assert res.exit_code == 0
        assert "• research" in res.output
        assert "• plan" in res.output


def test_list_agents_empty():
    """Test agents command when registry is empty."""
    with patch.object(AGENT_REGISTRY, "list_agents", return_value=[]):
        res = runner.invoke(app, ["agents"])
        assert res.exit_code == 0
        assert "No agents currently registered." in res.output


def test_research_command():
    """Test research command execution."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda: MockAgent("research")
        res = runner.invoke(app, ["research", "quantum computing"])
        assert res.exit_code == 0
        assert "Result for quantum computing" in res.output


def test_plan_command():
    """Test plan command execution."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda: MockAgent("planning")
        res = runner.invoke(app, ["plan", "product launch"])
        assert res.exit_code == 0
        assert "Result for product launch" in res.output


def test_outreach_command_with_and_without_context():
    """Test outreach command with and without optional context flag."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda: MockAgent("outreach")

        # Without context
        res1 = runner.invoke(app, ["outreach", "client@example.com"])
        assert res1.exit_code == 0
        assert "Result for client@example.com" in res1.output

        # With context
        res2 = runner.invoke(app, ["outreach", "client@example.com", "-c", "Follow-up"])
        assert res2.exit_code == 0
        assert "with ctx Follow-up" in res2.output


def test_get_agent_instance_unregistered():
    """Test error handling when an requested agent does not exist."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = None
        res = runner.invoke(app, ["research", "test"])
        assert res.exit_code != 0
        assert "no está registrado" in res.output or "Error" in res.output


def test_shell_command_interactive_flow():
    """Test REPL interactive shell with commands and exit conditions."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda: MockAgent("research")
        mock_reg.list_agents.return_value = ["research"]

        user_inputs = "agents\nresearch AI\nquit\n"
        res = runner.invoke(app, ["shell"], input=user_inputs)
        assert res.exit_code == 0
        assert "Interactive Session" in res.output
        assert "• research" in res.output
        assert "Result for AI" in res.output
        assert "Exiting Jaguar REPL shell." in res.output
