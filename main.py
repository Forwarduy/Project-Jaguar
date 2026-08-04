#!/usr/bin/env python3
"""
Project Jaguar 🐆
Open-source multi-agent platform for solopreneurs
"""
from typing import Annotated
import typer
from rich import print as rprint
from agents.registry import AGENT_REGISTRY

app = typer.Typer(
    name="jaguar",
    help="Project Jaguar - Multi-agent AI platform for business automation",
    add_completion=False
)

def _get_and_run_agent(agent_name: str, input_value: str) -> None:
    """Helper para instanciar, validar y ejecutar agentes de forma segura."""
    clean_input = input_value.strip()
    if not clean_input:
        rprint("[bold red]Error:[/bold red] El argumento proporcionado no puede estar vacío.")
        raise typer.Exit(code=1)

    agent_cls = AGENT_REGISTRY.get(agent_name)
    if not agent_cls:
        rprint(f"[bold red]Error:[/bold red] El agente '{agent_name}' no está registrado en AGENT_REGISTRY.")
        raise typer.Exit(code=1)

    try:
        agent = agent_cls()
        result = agent.run(clean_input)
        _print_result(result)
    except Exception as e:
        rprint(f"\n[bold red]Error crítico de ejecución ({agent_name}):[/bold red] {e}")
        raise typer.Exit(code=1)

def _print_result(result) -> None:
    if getattr(result, "success", False):
        rprint("\n[bold white]Result:[/bold white]")
        rprint(result.content)
    else:
        error_msg = getattr(result, "error", "Error desconocido en el agente.")
        rprint(f"\n[bold red]Error:[/bold red] {error_msg}")

@app.command()
def hello():
    """Test if Jaguar is ready 🐆"""
    rprint("[bold green]🐆 Project Jaguar is ready![/bold green]")
    rprint("Stack: Python + LangChain + n8n + Claude")
    rprint("Run: python main.py --help")

@app.command()
def research(
    topic: Annotated[str, typer.Option("--topic", "-t", help="Research topic")]
):
    """Run Research Agent with real Claude API"""
    rprint(f"[cyan]🔍 Research Agent: Investigating {topic}...[/cyan]")
    _get_and_run_agent("research", topic)

@app.command()
def plan(
    goal: Annotated[str, typer.Option("--goal", "-g", help="Planning goal")]
):
    """Run Planning Agent"""
    rprint(f"[magenta]📋 Planning Agent: Planning for {goal}...[/magenta]")
    _get_and_run_agent("plan", goal)

@app.command()
def outreach(
    campaign: Annotated[str, typer.Option("--campaign", "-c", help="Campaign name")]
):
    """Run Outreach Agent"""
    rprint(f"[yellow]📧 Outreach Agent: Campaign {campaign}...[/yellow]")
    _get_and_run_agent("outreach", campaign)

if __name__ == "__main__":
    app()
