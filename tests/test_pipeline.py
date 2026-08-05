"""Tests for pipeline orchestration and CLI chain execution."""

from unittest.mock import MagicMock, patch
from typer.testing import CliRunner

from main import app
from agents.pipeline import AgentPipeline
from agents.result import AgentResult

runner = CliRunner()


def test_pipeline_empty_steps():
    mock_registry = MagicMock()
    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([])

    assert result.success is False
    assert "no steps provided" in result.content


def test_pipeline_missing_agent_name():
    mock_registry = MagicMock()
    pipeline = AgentPipeline(mock_registry)
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
    mock_agent_1.run.return_value = AgentResult(success=True, content="Research Data")

    mock_agent_2 = MagicMock()
    mock_agent_2.run.return_value = AgentResult(success=True, content="Final Plan")

    mock_registry.get.side_effect = lambda name: {
        "research": lambda: mock_agent_1,
        "plan": lambda: mock_agent_2,
    }.get(name)

    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([
        {"agent": "research", "arg": "Market Trends"},
        {"agent": "plan"},
    ])

    assert result.success is True
    assert result.content == "Final Plan"
    mock_agent_1.run.assert_called_once_with("Market Trends")
    mock_agent_2.run.assert_called_once_with("Research Data")


def test_pipeline_agent_kwargs_execution():
    mock_registry = MagicMock()
    mock_agent = MagicMock()
    mock_agent.run.return_value = AgentResult(success=True, content="Outreach result")

    mock_registry.get.return_value = lambda: mock_agent

    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([
        {"agent": "outreach", "arg": "Target", "kwargs": {"message_context": "Urgent"}}
    ])

    assert result.success is True
    mock_agent.run.assert_called_once_with("Target", message_context="Urgent")


def test_pipeline_agent_exception_handling():
    mock_registry = MagicMock()
    mock_agent = MagicMock()
    mock_agent.run.side_effect = RuntimeError("Execution error")

    mock_registry.get.return_value = lambda: mock_agent

    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([{"agent": "research", "arg": "Topic"}])

    assert result.success is False
    assert "Pipeline failed at step 1" in result.content


@patch("main.AGENT_REGISTRY")
def test_cli_chain_command_success(mock_registry):
    mock_agent_1 = MagicMock()
    mock_agent_1.run.return_value = AgentResult(success=True, content="Intermediate output")

    mock_agent_2 = MagicMock()
    mock_agent_2.run.return_value = AgentResult(success=True, content="Final chained output")

    mock_registry.get.side_effect = lambda name: {
        "research": lambda: mock_agent_1,
        "plan": lambda: mock_agent_2,
    }.get(name)

    result = runner.invoke(app, ["chain", "research,plan", "Quantum Computing"])
    assert result.exit_code == 0
    assert "Final chained output" in result.stdout


@patch("main.AGENT_REGISTRY")
def test_cli_chain_command_failure(mock_registry):
    mock_agent = MagicMock()
    mock_agent.run.side_effect = RuntimeError("Failed step")
    mock_registry.get.return_value = lambda: mock_agent

    result = runner.invoke(app, ["chain", "research", "Test Topic"])
    assert result.exit_code == 1
    assert "Error:" in result.stdout
