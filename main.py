"""Main entry point for Project Jaguar CLI and application execution."""

import sys
from typing import List, Optional
import typer
from agents.registry import AgentRegistry
from agents.shell_system import ShellSystem
from agents.security import CredentialManager, requires_auth
from config import get_settings
from database.session import get_session, init_db
from workflows.market_analizer import MarketAnalyzerWorkflow

app = typer.Typer(help="Project Jaguar CLI System")

AGENT_REGISTRY = AgentRegistry()


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
    """Execute research and market analysis workflow (secured)."""
    # Asegurar que las tablas de la base de datos existan
    init_db()
    typer.echo(f"🚀 Iniciando flujo de análisis para el tema: {topic}")
    
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        workflow = MarketAnalyzerWorkflow()
        result = workflow.run(input_data={"topic": topic}, session=session)
        
        typer.echo("\n✅ ¡Flujo ejecutado y persistido con éxito!")
        typer.echo(f"• ID de Ejecución: {result.get('execution_id')}")
        typer.echo(f"• ID del Artefacto: {result.get('artifact_id')}")
        typer.echo(f"\n📄 Reporte Generado:\n{result.get('result')}")
        
    except Exception as e:
        typer.echo(f"❌ Error crítico en el workflow: {e}", err=True)
        raise typer.Exit(code=1)
    finally:
        session.close()


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
