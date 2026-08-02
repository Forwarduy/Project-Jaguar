#!/usr/bin/env python3
"""
Project Jaguar 🐆
Open-source multi-agent platform for solopreneurs
"""

import typer
from rich import print as rprint
from agents.research import ResearchAgent

app = typer.Typer(
    name="jaguar",
    help="Project Jaguar - Multi-agent AI platform for business automation",
    add_completion=False
)

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
    agent = ResearchAgent()
    result = agent.run(topic)
    rprint("\n[bold white]Result:[/bold white]")
    rprint(result)

@app.command()
def plan(
    goal: str = typer.Option(..., "--goal", "-g", help="Planning goal")
):
    """Run Planning Agent"""
    rprint(f"[magenta]📋 Planning Agent: Planning for {goal}...[/magenta]")
    rprint("[yellow]Coming soon - using same pattern as research.py[/yellow]")

@app.command()
def outreach(
    campaign: str = typer.Option(..., "--campaign", "-c", help="Campaign name")
):
    """Run Outreach Agent"""
    rprint(f"[yellow]📧 Outreach Agent: Campaign {campaign}...[/yellow]")
    rprint("[yellow]Coming soon[/yellow]")

if __name__ == "__main__":
    app()
