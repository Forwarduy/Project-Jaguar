"""Tests for pipeline orchestration and CLI chain command."""

from unittest.mock import MagicMock, patch
from typer.testing import CliRunner

from main import app
from agents.pipeline import AgentPipeline
from agents.result import AgentResult

runner = CliRunner()


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


def test_pipeline_missing_agent():
    mock_registry = MagicMock()
    mock_registry.get.return_value = None

    pipeline = AgentPipeline(mock_registry)
    result = pipeline.run_chain([{"agent": "nonexistent", "arg": "test"}])

    assert result.success is False
    assert "not found" in result.content


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
