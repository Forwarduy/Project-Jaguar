from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from main import app
from agents.result import AgentResult

runner = CliRunner()


@patch("main.Console.input")
@patch("main.AGENT_REGISTRY")
def test_interactive_shell_command(mock_registry, mock_input):
    mock_agent = MagicMock()
    mock_agent.run.return_value = AgentResult(success=True, content="REPL Output")
    mock_registry.get.return_value = lambda: mock_agent
    mock_registry.list_agents.return_value = ["research", "plan"]

    # Simulate sequence: 'agents', 'research AI', 'exit'
    mock_input.side_effect = ["agents", "research AI", "exit"]

    result = runner.invoke(app, ["shell"])
    assert result.exit_code == 0
    assert "• research" in result.stdout
    assert "REPL Output" in result.stdout
    assert "Exiting Jaguar REPL shell." in result.stdout
