"""Main entry point for Project Jaguar CLI and application execution."""

import sys
from typing import List, Optional
import typer
import anthropic
from agents.registry import AGENT_REGISTRY
from agents.shell_system import ShellSystem
from agents.security import CredentialManager, requires_auth
from config import get_settings

app = typer.Typer(help="Project Jaguar CLI System")


def verify_runtime_environment() -> bool:
    """Verify runtime environment settings and dependencies using CredentialManager."""
    secrets_status = CredentialManager.validate_environment_secrets()
    if not secrets_status.get("anthropic_api_key", False):
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
        typer.echo("Status: Operational (Secure)")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command("agents")
@requires_auth()
def agents_cmd():
    """List registered agents (secured)."""
    agents = AGENT_REGISTRY.list_agents()
    if not agents:
        typer.echo("No agents currently registered.")
        return
    for name in agents:
        typer.echo(f"• {name}")


@app.command("research")
@requires_auth()
def research_cmd(topic: str):
    """Execute research on a given topic (secured)."""
    settings = get_settings()
    if not settings.anthropic_api_key:
        typer.echo("❌ ANTHROPIC_API_KEY not found in .env", err=True)
        raise typer.Exit(code=1)

    try:
        agent = AGENT_REGISTRY.get("research")
    except KeyError:
        typer.echo("❌ Research agent not registered.", err=True)
        raise typer.Exit(code=1)

    client = anthropic.Anthropic(
        api_key=settings.anthropic_api_key,
        max_retries=settings.anthropic_max_retries,
    )
    result = agent.execute(topic=topic, client=client)
    typer.echo(str(result))


@app.command("plan")
@requires_auth()
def plan_cmd(goal: str):
    """Execute planning for a given goal (secured)."""
    typer.echo(f"Planning for goal: {goal}")


@app.command("outreach")
@requires_auth()
def outreach_cmd(target: str, context: Optional[str] = typer.Option(None, "--context", "-c")):
    """Execute outreach (secured)."""
    msg = f"Outreach to target: {target}"
    if context:
        msg += f" with context: {context}"
    typer.echo(msg)


@app.command("shell")
@requires_auth()
def shell_cmd():
    """Start interactive shell REPL (secured)."""
    shell = ShellSystem()
    typer.echo("Project-Jaguar REPL Interactive Shell")
    while True:
        try:
            user_input = input("jaguar> ").strip()
            if not user_input:
                continue
            if user_input in ("exit", "quit"):
                typer.echo("Exiting Jaguar REPL shell.")
                break
            result = shell.execute_command(user_input)
            if result.content:
                typer.echo(result.content)
            if result.metadata and result.metadata.get("should_exit"):
                typer.echo("Exiting Jaguar REPL shell.")
                break
        except (KeyboardInterrupt, EOFError):
            typer.echo("\nExiting Jaguar REPL shell.")
            break


def main(argv: Optional[List[str]] = None) -> int:
    """Main application entry point."""
    if argv is not None:
        sys.argv = [sys.argv[0]] + argv
    try:
        app()
    except PermissionError as pe:
        typer.echo(f"Access Denied: {pe}", err=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
