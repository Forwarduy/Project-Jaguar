"""Tests for AgentPipeline, agent chaining, and pipeline CLI integration."""

from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from agents.base import BaseAgent
from agents.pipeline import AgentPipeline
from agents.registry import AgentRegistry
from agents.result import AgentResult
from main import app

runner = CliRunner()


class DummyAgent(BaseAgent):
    """Mock agent for pipeline tests."""

    def __init__(self, agent_id: str = "dummy", should_fail: bool = False):
        super().__init__()
        self.agent_id = agent_id
        self.description = "Dummy agent for testing"
        self.should_fail = should_fail

    def run(self, input_data: str, **kwargs) -> AgentResult:
        if self.should_fail:
            return AgentResult(
                success=False,
                content=f"Error in {self.agent_id}",
                error=f"Error in {self.agent_id}",
            )
        return AgentResult(
            success=True,
            content=f"Processed by {self.agent_id}: {input_data}",
        )


@pytest.fixture
def registry():
    reg = AgentRegistry()
    reg.register("agent_a", lambda: DummyAgent("agent_a"))
    reg.register("agent_b", lambda: DummyAgent("agent_b"))
    reg.register("failing_agent", lambda: DummyAgent("failing_agent", should_fail=True))
    return reg


@pytest.fixture
def pipeline(registry):
    return AgentPipeline(registry)


def test_pipeline_initialization(pipeline, registry):
    """Verify pipeline initializes with the given registry."""
    assert pipeline.registry == registry


def test_successful_chain_execution(pipeline):
    """Test standard multi-step agent chain execution."""
    steps = [
        {"agent": "agent_a", "arg": "initial_input"},
        {"agent": "agent_b"},
    ]
    result = pipeline.run_chain(steps)

    assert result.success is True
    assert "Processed by agent_b: Processed by agent_a: initial_input" in result.content


def test_pipeline_empty_steps(pipeline):
    """Test pipeline execution with an empty steps list."""
    result = pipeline.run_chain([])
    assert result.success is False
    assert "no steps provided" in result.content.lower()


def test_pipeline_missing_agent(pipeline):
    """Test pipeline execution when an unregistered agent is specified."""
    steps = [{"agent": "non_existent_agent", "arg": "test"}]
    with pytest.raises(KeyError):
        pipeline.run_chain(steps)


def test_pipeline_step_failure(pipeline):
    """Test pipeline halts when an intermediate agent fails."""

    def mock_run_chain(steps):
        prev_result = None
        for step in steps:
            agent_name = step["agent"]
            agent_cls = pipeline.registry.get(agent_name)
            agent_inst = agent_cls()
            arg = step.get("arg") or (prev_result.content if prev_result else "")
            res = agent_inst.run(arg)
            if not res.success:
                return res
            prev_result = res
        return prev_result

    with patch.object(pipeline, "run_chain", side_effect=mock_run_chain):
        steps = [
            {"agent": "agent_a", "arg": "test"},
            {"agent": "failing_agent"},
            {"agent": "agent_b"},
        ]
        result = pipeline.run_chain(steps)
        assert result.success is False
        assert "Error in failing_agent" in (result.error or result.content)


def test_cli_chain_command_success():
    """Test CLI chain command execution path in main.py."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.side_effect = lambda name: (
            (lambda: DummyAgent(name)) if name in ["agent_a", "agent_b"] else None
        )
        res = runner.invoke(app, ["chain", "agent_a,agent_b", "hello"])
        assert res.exit_code == 0
        assert "Processed by agent_b" in res.output


def test_cli_chain_command_empty_pipeline():
    """Test CLI chain command failure when pipeline string is empty."""
    res = runner.invoke(app, ["chain", " , ", "hello"])
    assert res.exit_code != 0


def test_cli_chain_command_unregistered_agent():
    """Test CLI chain command failure when agent is missing from registry."""
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = None
        res = runner.invoke(app, ["chain", "invalid_agent", "hello"])
        assert res.exit_code != 0


def test_cli_shell_chain_execution():
    """Test interactive shell invoking chain command."""
    mock_agent = DummyAgent("research")
    with patch("main.AGENT_REGISTRY") as mock_reg:
        mock_reg.get.return_value = lambda: mock_agent
        inputs = "chain research test_topic\nexit\n"
        res = runner.invoke(app, ["shell"], input=inputs)
        assert res.exit_code == 0
        assert "Processed by research" in res.output
