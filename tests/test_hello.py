from typer.testing import CliRunner
from main import app

runner = CliRunner()

def test_hello_command():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Project Jaguar" in result.stdout

def test_help_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "research" in result.stdout.lower()

def test_research_agent_import():
    # Test que el agente real se puede importar (P0 de Anthropic)
    from agents.research import ResearchAgent
    agent = ResearchAgent()
    assert agent.name == "ResearchAgent"
