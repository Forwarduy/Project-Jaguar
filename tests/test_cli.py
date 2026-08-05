from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from main import app
from agents.result import AgentResult

runner = CliRunner()

def test_cli_hello_command():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Project Jaguar CLI operational." in result.stdout

@patch("main.AGENT_REGISTRY")
def test_cli_research_command_success(mock_registry):
    mock_agent_cls = MagicMock()
    mock_agent_instance = MagicMock()
    mock_agent_instance.run.return_value = AgentResult(success=True, content="Research output data")
    mock_agent_cls.return_value = mock_agent_instance
    mock_registry.get.return_value = mock_agent_cls

    result = runner.invoke(app, ["research", "Quantum Computing"])
    assert result.exit_code == 0
    assert "Research output data" in result.stdout
    mock_registry.get.assert_called_with("research")

@patch("main.AGENT_REGISTRY")
def test_cli_plan_command_success(mock_registry):
    mock_agent_cls = MagicMock()
    mock_agent_instance = MagicMock()
    mock_agent_instance.run.return_value = AgentResult(success=True, content="Execution Plan OK")
    mock_agent_cls.return_value = mock_agent_instance
    mock_registry.get.return_value = mock_agent_cls

    result = runner.invoke(app, ["plan", "Launch new product"])
    assert result.exit_code == 0
    assert "Execution Plan OK" in result.stdout
    mock_registry.get.assert_called_with("planning")

@patch("main.AGENT_REGISTRY")
def test_cli_outreach_command_success(mock_registry):
    mock_agent_cls = MagicMock()
    mock_agent_instance = MagicMock()
    mock_agent_instance.run.return_value = AgentResult(success=True, content="Outreach Draft OK")
    mock_agent_cls.return_value = mock_agent_instance
    mock_registry.get.return_value = mock_agent_cls

    result = runner.invoke(app, ["outreach", "Acme Corp", "--context", "Partnership Q3"])
    assert result.exit_code == 0
    assert "Outreach Draft OK" in result.stdout
    mock_registry.get.assert_called_with("outreach")
    mock_agent_instance.run.assert_called_with("Acme Corp", message_context="Partnership Q3")

@patch("main.AGENT_REGISTRY")
def test_cli_unregistered_agent_error(mock_registry):
    mock_registry.get.return_value = None

    result = runner.invoke(app, ["plan", "Unknown goal"])
    assert result.exit_code == 1
    assert "El agente 'planning' no está registrado" in result.stdout
