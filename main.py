"""Main entry point for Project-Jaguar Multi-Agent Orchestrator."""

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

# Expose AGENT_REGISTRY at module level for test patch targets
AGENT_REGISTRY = AgentRegistry()


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
    console.print("Hello from Project-Jaguar!")


@app.command("health")
def health_check():
    """Run environmental checks and verify agent registry state."""
    console.print("[yellow]Running system integrity diagnostics...[/yellow]")
    try:
        verify_runtime_environment()
        settings = get_settings()

        console.print("[bold green]✓ System status:[/bold green] Operational")
        console.print(f"[green]✓ Environment:[/green] {settings.environment}")
        console.print(f"[green]✓ Registered agents:[/green] {len(AGENT_REGISTRY.list_agents())}")
    except SystemValidationError as e:
        console.print(f"[bold red]✗ Environment Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]✗ Boot Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command("agents")
def list_agents():
    """Display all loaded agents in the system registry."""
    available = AGENT_REGISTRY.list_agents()

    if not available:
        console.print("[yellow]No agents currently registered.[/yellow]")
        return

    console.print("[bold cyan]Available Agents:[/bold cyan]")
    for agent_id in available:
        console.print(f"  • [bold]{agent_id}[/bold]")


@app.command("research")
def research_cmd(topic: str = typer.Argument(..., help="Topic to research")):
    """Run the research agent."""
    agent = AGENT_REGISTRY.get("research")
    if not agent:
        console.print("[bold red]Research agent not registered.[/bold red]")
        raise typer.Exit(code=1)
    res = agent.run({"topic": topic})
    console.print(res)


@app.command("plan")
def plan_cmd(goal: str = typer.Argument(..., help="Goal to plan for")):
    """Run the planning agent."""
    agent = AGENT_REGISTRY.get("planning")
    if not agent:
        console.print("[bold red]Planning agent not registered.[/bold red]")
        raise typer.Exit(code=1)
    res = agent.run({"goal": goal})
    console.print(res)


@app.command("outreach")
def outreach_cmd(target: str = typer.Argument(..., help="Outreach target")):
    """Run the outreach agent."""
    agent = AGENT_REGISTRY.get("outreach")
    if not agent:
        console.print("[bold red]Outreach agent not registered.[/bold red]")
        raise typer.Exit(code=1)
    res = agent.run({"target": target})
    console.print(res)


if __name__ == "__main__":
    app()
