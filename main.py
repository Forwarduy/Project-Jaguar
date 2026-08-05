"""Main entry point for Project-Jaguar Multi-Agent Orchestrator."""

from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from config import get_settings
from agents.registry import AgentRegistry
from agents.shell_system import verify_runtime_environment, SystemValidationError

app = typer.Typer(
    name="Project-Jaguar",
    help="Modular Multi-Agent Operational Shell CLI",
    add_completion=False,
)
console = Console()

AGENT_REGISTRY = AgentRegistry()


def _get_agent_and_execute(agent_name: str, payload: dict):
    agent_target = AGENT_REGISTRY.get(agent_name)
    if not agent_target:
        console.print(f"El agente '{agent_name}' no está registrado.")
        raise typer.Exit(code=1)

    # Instantiate if a class/factory mock was returned by the registry lookup
    if callable(agent_target) and not hasattr(agent_target, "run"):
        agent_instance = agent_target()
    else:
        agent_instance = agent_target

    res = agent_instance.run(payload)
    content = getattr(res, "content", res)
    console.print(content)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
):
    """Global initializer and runtime health validation."""
    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                "[bold cyan]Project-Jaguar Multi-Agent Shell Engine[/bold cyan]\n"
                "[dim]Run 'python main.py --help' for available commands.[/dim]",
                title="System Ready",
                border_style="cyan",
            )
        )


@app.command("hello")
def hello():
    """Greeting command for CLI verification."""
    console.print("Project Jaguar CLI operational.")


@app.command("health")
def health_check():
    """Run environmental checks and verify agent registry state."""
    try:
        verify_runtime_environment()
        settings = get_settings()
        console.print(f"Status: Operational | Env: {settings.environment} | Agents: {len(AGENT_REGISTRY.list_agents())}")
    except (SystemValidationError, Exception) as e:
        console.print(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command("agents")
def list_agents():
    """Display all loaded agents in the system registry."""
    available = AGENT_REGISTRY.list_agents()
    if not available:
        console.print("No agents currently registered.")
        return
    for agent_id in available:
        console.print(f"• {agent_id}")


@app.command("research")
def research_cmd(topic: str = typer.Argument(..., help="Topic to research")):
    """Run the research agent."""
    _get_agent_and_execute("research", {"topic": topic})


@app.command("plan")
def plan_cmd(goal: str = typer.Argument(..., help="Goal to plan for")):
    """Run the planning agent."""
    _get_agent_and_execute("planning", {"goal": goal})


@app.command("outreach")
def outreach_cmd(
    target: str = typer.Argument(..., help="Outreach target"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="Additional context"),
):
    """Run the outreach agent."""
    payload = {"target": target}
    if context:
        payload["context"] = context
    _get_agent_and_execute("outreach", payload)


if __name__ == "__main__":
    app()
