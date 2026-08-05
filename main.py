"""Main entry point for Project-Jaguar Multi-Agent Orchestrator."""

import typer
from rich.console import Console
from rich.panel import Panel

from config import load_settings
from agents.registry import AgentRegistry
from agents.shell_system import verify_runtime_environment, SystemValidationError

app = typer.Typer(
    name="Project-Jaguar",
    help="Modular Multi-Agent Operational Shell CLI",
    add_completion=False,
)
console = Console()


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


@app.command("health")
def health_check():
    """Run environmental checks and verify agent registry state."""
    console.print("[yellow]Running system integrity diagnostics...[/yellow]")
    try:
        verify_runtime_environment()
        settings = load_settings()
        registry = AgentRegistry()

        console.print("[bold green]✓ System status:[/bold green] Operational")
        console.print(f"[green]✓ Environment:[/green] {settings.ENVIRONMENT}")
        console.print(f"[green]✓ Registered agents:[/green] {len(registry.list_agents())}")
    except SystemValidationError as e:
        console.print(f"[bold red]✗ Environment Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]✗ Boot Error:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command("agents")
def list_agents():
    """Display all loaded agents in the system registry."""
    registry = AgentRegistry()
    available = registry.list_agents()

    if not available:
        console.print("[yellow]No agents currently registered.[/yellow]")
        return

    console.print("[bold cyan]Available Agents:[/bold cyan]")
    for agent_id in available:
        console.print(f"  • [bold]{agent_id}[/bold]")


if __name__ == "__main__":
    app()
