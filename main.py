"""Main entry point for Project Jaguar CLI and application execution."""

import sys
from typing import List, Optional
import typer
from agents.registry import AgentRegistry
from agents.shell_system import ShellSystem
from config import get_settings

app = typer.Typer(help="Project Jaguar CLI System")

AGENT_REGISTRY = AgentRegistry()


def verify_runtime_environment() -> bool:
    """Verify runtime environment settings and dependencies."""
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")
    return True


@app.command("hello")
def hello_cmd():
    """Print a greeting message."""
    typer.echo("Project Jaguar CLI operational.")


@app.command("health")
def health_cmd():
    """Verify runtime environment health."""
    try:
        verify_runtime_environment()
        typer.echo("Status: Operational")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command("agents")
def agents_cmd():
    """List registered agents."""
    agents = AGENT_REGISTRY.list_agents()
    if not agents:
        typer.echo("No agents currently registered.")
        return
    for name in agents:
        typer.echo(f"• {name}")


@app.command("research")
def research_cmd(topic: str):
    """Execute research on a given topic."""
    typer.echo(f"Researching topic: {topic}")


@app.command("plan")
def plan_cmd(goal: str):
    """Execute planning for a given goal."""
    typer.echo(f"Planning for goal: {goal}")


@app.command("outreach")
def outreach_cmd(target: str, context: Optional[str] = typer.Option(None, "--context", "-c")):
    """Execute outreach."""
    msg = f"Outreach to target: {target}"
    if context:
        msg += f" with context: {context}"
    typer.echo(msg)


@app.command("shell")
def shell_cmd():
    """Start interactive shell REPL."""
    shell = ShellSystem()
    typer.echo("Project-Jaguar REPL Interactive Shell")
    while True:
        try:
            user_input = input("jaguar> ").strip()
            if not user_input:
                continue
            if user_input in ("exit", "quit"):
                break
            result = shell.execute_command(user_input)
            if result.content:
                typer.echo(result.content)
            if result.metadata and result.metadata.get("should_exit"):
                break
        except (KeyboardInterrupt, EOFError):
            typer.echo("\nExiting session.")
            break


def main(argv: Optional[List[str]] = None) -> int:
    """Main application entry point."""
    if argv is not None:
        sys.argv = [sys.argv[0]] + argv
    app()
    return 0


if __name__ == "__main__":
    sys.exit(main())
