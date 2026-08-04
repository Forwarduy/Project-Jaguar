#!/usr/bin/env python3
"""
Project Jaguar 🐆
Open-source multi-agent platform for solopreneurs
"""
import asyncio
from typing import Annotated, Optional
import typer
from rich import print as rprint

from agents.registry import AGENT_REGISTRY
from agents.result import AgentResult

app = typer.Typer(
    name="jaguar",
    help="Project Jaguar - Multi-agent AI platform for business automation",
    add_completion=False,
)


def _get_and_run_agent(agent_name: str, input_value: Optional[str]) -> None:
    """Helper para instanciar, validar y ejecutar agentes de forma segura."""
    if not input_value or not input_value.strip():
        rprint("[bold red]Error:[/bold red] Debe proporcionar un argumento válido no vacío.")
        raise typer.Exit(code=1)

    clean_input = input_value.strip()
    agent_cls = AGENT_REGISTRY.get(agent_name)

    if not agent_cls:
        rprint(f"[bold red]Error:[/bold red] El agente '{agent_name}' no está registrado en AGENT_REGISTRY.")
        raise typer.Exit(code=1)

    try:
        agent = agent_cls()
        
        # Ejecución asíncrona segura en el loop de eventos si aplica
        if hasattr(agent, "arun") and callable(agent.arun):
            result: AgentResult = asyncio.run(agent.arun(clean_input))
        else:
            result = agent.run(clean_input)

        _print_result(result)
    except Exception as e:
        rprint(f"\n[bold red]Error crítico de ejecución ({agent_name}):[/bold red] {e}")
        raise typer.Exit(code=1)


def _print_result(result: AgentResult) -> None:
    if getattr(result, "success", False):
        rprint("\n[bold green]✔ Result:[/bold green]")
        rprint(result.content)
    else:
        error_msg = getattr(result, "error", "Error desconocido en el agente.")
        rprint(f"\n[bold red]Error:[/bold red] {error_msg}")


@app.command()
def hello():
    """Test if Jaguar is ready 🐆"""
    rprint("[bold green]🐆 Project Jaguar is ready![/bold green]")
    rprint("Stack: Python 3.10+ | Pydantic v2 | Anthropic SDK | Typer | Rich")
    rprint("Run: python main.py --help")


@app.command()
def research(
    topic: Annotated[
        Optional[str], 
        typer.Option("--topic", "-t", help="Research topic to evaluate")
    ] = None
):
    """Run Research Agent with real Claude API"""
    if not topic:
        rprint("[bold red]Error:[/bold red] Falta el parámetro obligatorio `--topic` / `-t`.")
        raise typer.Exit(code=1)
    
    rprint(f"[cyan]🔍 Research Agent: Investigating '{topic}'...[/cyan]")
    _get_and_run_agent("research", topic)


@app.command()
def plan(
    goal: Annotated[
        Optional[str], 
        typer.Option("--goal", "-g", help="Planning goal")
    ] = None
):
    """Run Planning Agent"""
    if not goal:
        rprint("[bold red]Error:[/bold red] Falta el parámetro obligatorio `--goal` / `-g`.")
        raise typer.Exit(code=1)

    rprint(f"[magenta]📋 Planning Agent: Planning for '{goal}'...[/magenta]")
    _get_and_run_agent("plan", goal)


@app.command()
def outreach(
    campaign: Annotated[
        Optional[str], 
        typer.Option("--campaign", "-c", help="Campaign name")
    ] = None
):
    """Run Outreach Agent"""
    if not campaign:
        rprint("[bold red]Error:[/bold red] Falta el parámetro obligatorio `--campaign` / `-c`.")
        raise typer.Exit(code=1)

    rprint(f"[yellow]📧 Outreach Agent: Campaign '{campaign}'...[/yellow]")
    _get_and_run_agent("outreach", campaign)


if __name__ == "__main__":
    app()
