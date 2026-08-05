"""Tests for pipeline orchestration and CLI chain execution."""

from unittest.mock import MagicMock, patch
from typer.testing import CliRunner

from main import app
from agents.pipeline import AgentPipeline
from agents.result import AgentResult

runner = CliRunner()


def test_pipeline_empty_steps():
    pipeline = AgentPipeline(MagicMock())
    result = pipeline.run_chain([])
    assert result.success is False
    assert "no steps provided" in result.content


def test_pipeline_missing_agent_name():
    pipeline = AgentPipeline(MagicMock())
    result = pipeline.run_chain([{"arg": "test_input"}])
    assert result.success is False
    assert "missing agent name" in result.content


def test_pipeline_missing_agent_in_registry():
    mock_registry = MagicMock()
    mock_registry.get.return_value = None
    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([{"agent": "nonexistent", "arg": "test_input"}])
    assert result.success is False
    assert "not found" in result.content


def test_pipeline_chain_success():
    mock_registry = MagicMock()
    mock_agent_1 = MagicMock()
    mock_agent_1.run.return_value = AgentResult(success=True, content="Intermediate output")

    mock_agent_2 = MagicMock()
    mock_agent_2.run.return_value = AgentResult(success=True, content="Final output")

    mock_registry.get.side_effect = lambda name: {
        "research": lambda: mock_agent_1,
        "plan": lambda: mock_agent_2,
    }.get(name)

    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([
        {"agent": "research", "arg": "Topic"},
        {"agent": "plan"},
    ])

    assert result.success is True
    assert result.content == "Final output"


def test_pipeline_agent_exception():
    mock_registry = MagicMock()
    mock_agent = MagicMock()
    mock_agent.run.side_effect = RuntimeError("Agent crash")
    mock_registry.get.return_value = lambda: mock_agent

    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([{"agent": "research", "arg": "Topic"}])
    assert result.success is False
    assert "Pipeline failed at step 1" in result.content


@patch("main.Console.input")
@patch("main.AGENT_REGISTRY")
def test_interactive_shell_command(mock_registry, mock_input):
    mock_agent = MagicMock()
    mock_agent.run.return_value = AgentResult(success=True, content="REPL Output")
    mock_registry.get.return_value = lambda: mock_agent
    mock_registry.list_agents.return_value = ["research", "plan"]

    mock_input.side_effect = ["agents", "research AI", "exit"]

    result = runner.invoke(app, ["shell"])
    assert result.exit_code == 0
    assert "Exiting Jaguar REPL shell." in result.stdout
