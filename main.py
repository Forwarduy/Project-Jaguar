"""Main entry point for Project-Jaguar Multi-Agent Orchestrator."""

from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from config import get_settings
from agents.registry import AgentRegistry
from agents.pipeline import AgentPipeline
from agents.shell_system import verify_runtime_environment, SystemValidationError

app = typer.Typer(
    name="Project-Jaguar",
    help="Modular Multi-Agent Operational Shell CLI",
    add_completion=False,
)
console = Console()

# Exposed at module level for test patch targets
AGENT_REGISTRY = AgentRegistry()


def _get_agent_instance(agent_name: str):
    agent_target = AGENT_REGISTRY.get(agent_name)
    if not agent_target:
        console.print(f"El agente '{agent_name}' no está registrado.")
        raise typer.Exit(code=1)
    return agent_target() if callable(agent_target) else agent_target


def _print_result(result):
    content = getattr(result, "content", result)
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
        console.print(
            f"Status: Operational | Env: {settings.environment} | "
            f"Agents: {len(AGENT_REGISTRY.list_agents())}"
        )
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
    agent = _get_agent_instance("research")
    res = agent.run(topic)
    _print_result(res)


@app.command("plan")
def plan_cmd(goal: str = typer.Argument(..., help="Goal to plan for")):
    """Run the planning agent."""
    agent = _get_agent_instance("planning")
    res = agent.run(goal)
    _print_result(res)


@app.command("outreach")
def outreach_cmd(
    target: str = typer.Argument(..., help="Outreach target"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="Additional context"),
):
    """Run the outreach agent."""
    agent = _get_agent_instance("outreach")
    if context is not None:
        res = agent.run(target, message_context=context)
    else:
        res = agent.run(target)
    _print_result(res)


@app.command("chain")
def chain_cmd(
    pipeline_str: str = typer.Argument(
        ..., help="Comma-separated agent chain (e.g. 'research,plan')"
    ),
    initial_input: str = typer.Argument(..., help="Initial input for the first agent"),
):
    """Run a sequential chain of agents, passing each output to the next."""
    agent_names = [name.strip() for name in pipeline_str.split(",") if name.strip()]
    if not agent_names:
        console.print("Error: No agents specified in pipeline.")
        raise typer.Exit(code=1)

    steps = [{"agent": agent_names[0], "arg": initial_input}]
    for name in agent_names[1:]:
        steps.append({"agent": name})

    pipeline = AgentPipeline(AGENT_REGISTRY)
    res = pipeline.run_chain(steps)
    if not res.success:
        console.print(f"[red]Error:[/red] {res.content}")
        raise typer.Exit(code=1)

    _print_result(res)


if __name__ == "__main__":
    app()
