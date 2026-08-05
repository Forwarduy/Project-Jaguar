import sys
from typing import Optional
from typing_extensions import Annotated
import typer
from rich import print as rprint

from agents.registry import AGENT_REGISTRY

app = typer.Typer(
    name="jaguar",
    help="Project Jaguar - Production-grade Multi-Agent System CLI",
    add_completion=False,
)

def _get_and_run_agent(agent_name: str, primary_arg: str, **kwargs):
    """Helper para resolver el agente en el registry y ejecutarlo limpiamente."""
    try:
        agent_cls = AGENT_REGISTRY.get(agent_name)
        if not agent_cls:
            rprint(f"[bold red]Error:[/bold red] El agente '{agent_name}' no está registrado en AGENT_REGISTRY.")
            raise typer.Exit(code=1)
        
        agent = agent_cls()
        result = agent.run(primary_arg, **kwargs)
        
        if result.success:
            rprint(f"[bold green]Success:[/bold green]\n{result.content or result.data}")
        else:
            rprint(f"[bold red]Agent Error:[/bold red] {result.error}")
            raise typer.Exit(code=1)
    except Exception as e:
        rprint(f"[bold red]System Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def hello():
    """Comando de prueba del CLI."""
    rprint("[bold blue]Project Jaguar CLI operational.[/bold blue]")

@app.command()
def research(
    topic: Annotated[str, typer.Argument(help="Topic to research")]
):
    """Run research on a given topic using ResearchAgent."""
    _get_and_run_agent("research", topic)

@app.command()
def plan(
    goal: Annotated[str, typer.Argument(help="Goal or objective to plan for")]
):
    """Generate an execution plan for a given goal using PlanningAgent."""
    _get_and_run_agent("planning", goal)

@app.command()
def outreach(
    recipient: Annotated[str, typer.Argument(help="Target recipient or organization")],
    context: Annotated[Optional[str], typer.Option("--context", "-c", help="Additional message context or goal")] = None
):
    """Draft an outreach message for a specific recipient using OutreachAgent."""
    kwargs = {"message_context": context} if context else {}
    _get_and_run_agent("outreach", recipient, **kwargs)

if __name__ == "__main__":
    app()
