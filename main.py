#!/usr/bin/env python3
"""
Project Jaguar 🐆
Open-source multi-agent platform for solopreneurs
"""
import typer
from rich import print as rprint
from agents.registry import AGENT_REGISTRY

app = typer.Typer(
    name="jaguar",
    help="Project Jaguar - Multi-agent AI platform for business automation",
    add_completion=False
)

def _print_result(result) -> None:
    if result.success:
        rprint("\n[bold white]Result:[/bold white]")
        rprint(result.content)
    else:
        rprint(f"\n[bold red]Error:[/bold red] {result.error}")

@app.command()
def hello():
    """Test if Jaguar is ready 🐆"""
    rprint("[bold green]🐆 Project Jaguar is ready![/bold green]")
    rprint("Stack: Python + LangChain + n8n + Claude")
    rprint("Run: python main.py --help")

@app.command()
def research(
    topic: str = typer.Option(..., "--topic", "-t", help="Research topic")
):
    """Run Research Agent with real Claude API"""
    rprint(f"[cyan]🔍 Research Agent: Investigating {topic}...[/cyan]")
    agent = AGENT_REGISTRY["research"]()
    _print_result(agent.run(topic))

@app.command()
def plan(
    goal: str = typer.Option(..., "--goal", "-g", help="Planning goal")
):
    """Run Planning Agent"""
    rprint(f"[magenta]📋 Planning Agent: Planning for {goal}...[/magenta]")
    agent = AGENT_REGISTRY["plan"]()
    _print_result(agent.run(goal))

@app.command()
def outreach(
    campaign: str = typer.Option(..., "--campaign", "-c", help="Campaign name")
):
    """Run Outreach Agent"""
    rprint(f"[yellow]📧 Outreach Agent: Campaign {campaign}...[/yellow]")
    agent = AGENT_REGISTRY["outreach"]()
    _print_result(agent.run(campaign))

if __name__ == "__main__":
    app()
