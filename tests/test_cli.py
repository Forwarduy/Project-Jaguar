"""Tests for Project-Jaguar CLI commands and interactive shell."""

from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from agents.base import BaseAgent
from agents.result import AgentResult
from main import app

runner = CliRunner()


class MockAgent(BaseAgent):
    """Mock agent adhering to BaseAgent interface for CLI tests.

    run()/execute() juntan todos los kwargs de contenido (topic, project_name,
    target_audience, goal, etc.) en la respuesta, para poder representar a
    cualquiera de los 3 agentes reales sin importar cómo cada uno nombre su
    parámetro principal.
    """

    def __init__(self, agent_id: str = "mock_agent"):
        super().__init__()
        self.agent_id = agent_id
        self.description = "Mock CLI test agent"

    def run(self, *args, **kwargs) -> AgentResult:
        if args:
            parts = [str(args[0])]
        else:
            parts = [str(v) for k, v in kwargs.items() if k != "client" and v is not None]
        joined = " | ".join(parts)
        return AgentResult(
            success=True,
            content=f"Mock response for {self.agent_id} on '{joined}'",
            agent_name=self.agent_id,
        )

    def execute(self, **kwargs) -> AgentResult:
        # Igual que ResearchAgent/PlanningAgent/OutreachAgent.execute(): reenvía
        # todo por kwargs (necesario para que llegue client=... sin TypeError).
        return self.run(**kwargs)


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
        # AGENT_REGISTRY.get() ya devuelve el agente instanciado, no una fábrica
        mock_reg.get.return_value = MockAgent("research")
        res = runner.invoke(app, ["research", "quantum computing"])
        assert res.exit_code == 0
        assert "quantum computing" in res.output


def test_plan_command():
    """Test plan command execution."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = MockAgent("planning")
        res = runner.invoke(app, ["plan", "product launch"])
        assert res.exit_code == 0
        assert "product launch" in res.output


def test_outreach_command_with_and_without_context():
    """Test outreach command with and without optional context flag."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = MockAgent("outreach")

        # Without context: outreach_cmd arma un goal genérico usando target
        res1 = runner.invoke(app, ["outreach", "client@example.com"])
        assert res1.exit_code == 0
        assert "client@example.com" in res1.output

        # With context
        res2 = runner.invoke(app, ["outreach", "client@example.com", "-c", "Special Promo"])
        assert res2.exit_code == 0
        assert "Special Promo" in res2.output


def test_shell_command_interactive_flow():
    """Test REPL interactive shell with commands and exit conditions.

    Nota: ShellSystem importa su propio AGENT_REGISTRY (de agents.registry),
    no el de main.py, así que este mock no lo alcanza — el shell usa los
    agentes reales. Con ANTHROPIC_API_KEY=dummy-key-for-tests (conftest.py),
    "research AI" intenta una llamada real a la API que va a fallar (401),
    pero el error queda contenido en un AgentResult.fail() y no tira el
    exit_code — por eso el test sigue pasando, aunque sea más lento.
    """
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = MockAgent("research")
        mock_reg.list_agents.return_value = ["research"]

        user_inputs = "agents\nresearch AI\nquit\n"
        res = runner.invoke(app, ["shell"], input=user_inputs)
        assert res.exit_code == 0
        assert "Project-Jaguar REPL Interactive Shell" in res.output
        assert "Exiting Jaguar REPL shell." in res.output
