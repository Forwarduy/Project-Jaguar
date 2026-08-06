"""Tests for Project-Jaguar CLI commands and interactive shell."""

from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from agents.base import BaseAgent
from agents.result import AgentResult
from main import app

runner = CliRunner()


class MockAgent(BaseAgent):
    """Mock agent adhering to BaseAgent interface for CLI tests."""

    def __init__(self, agent_id: str = "mock_agent"):
        super().__init__()
        self.agent_id = agent_id
        self.description = "Mock CLI test agent"

    def run(self, prompt: str, **kwargs) -> AgentResult:
        context_str = (
            f" Context: {kwargs.get('message_context')}"
            if "message_context" in kwargs and kwargs.get("message_context") is not None
            else ""
        )
        return AgentResult(
            success=True,
            content=f"Mock response for {self.agent_id} on '{prompt}'{context_str}",
            agent_name=self.agent_id,
        )


def test_hello_command():
    """Test hello command execution."""
    res = runner.invoke(app, ["hello"])
    assert res.exit_code == 0
    assert "Project Jaguar CLI operational." in res.output


def test_health_command_success():
    """Test health command when environment verification passes."""
    with patch("main.verify_runtime_environment"):
        res = runner.invoke(app, ["health"])
        assert res.exit_code == 0
        assert "Status: Operational" in res.output


def test_health_command_failure():
    """Test health command when environment verification fails."""
    with patch("main.verify_runtime_environment", side_effect=Exception("Env error")):
        res = runner.invoke(app, ["health"])
        assert res.exit_code == 1
        assert "Error: Env error" in res.output


def test_agents_command_with_registered_agents():
    """Test agents command listing registered agents."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.list_agents.return_value = ["research", "planning", "outreach"]
        res = runner.invoke(app, ["agents"])
        assert res.exit_code == 0
        assert "• research" in res.output
        assert "• planning" in res.output


def test_agents_command_empty():
    """Test agents command when no agents are registered."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.list_agents.return_value = []
        res = runner.invoke(app, ["agents"])
        assert res.exit_code == 0
        assert "No agents currently registered." in res.output


def test_research_command():
    """Test research command execution."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        # Aceptar kwargs para evitar TypeError al inyectar client=client
        mock_reg.get.return_value = lambda **kwargs: MockAgent("research")
        res = runner.invoke(app, ["research", "quantum computing"])
        assert res.exit_code == 0
        assert "quantum computing" in res.output


def test_plan_command():
    """Test plan command execution."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda **kwargs: MockAgent("planning")
        res = runner.invoke(app, ["plan", "product launch"])
        assert res.exit_code == 0
        assert "product launch" in res.output


def test_outreach_command_with_and_without_context():
    """Test outreach command with and without optional context flag."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda **kwargs: MockAgent("outreach")

        # Without context
        res1 = runner.invoke(app, ["outreach", "client@example.com"])
        assert res1.exit_code == 0
        assert "client@example.com" in res1.output

        # With context
        res2 = runner.invoke(app, ["outreach", "client@example.com", "-c", "Special Promo"])
        assert res2.exit_code == 0
        assert "Special Promo" in res2.output


def test_shell_command_interactive_flow():
    """Test REPL interactive shell with commands and exit conditions."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda **kwargs: MockAgent("research")
        mock_reg.list_agents.return_value = ["research"]

        user_inputs = "agents\nresearch AI\nquit\n"
        res = runner.invoke(app, ["shell"], input=user_inputs)
        assert res.exit_code == 0
        assert "Project-Jaguar REPL Interactive Shell" in res.output
        assert "Exiting Jaguar REPL shell." in res.output
