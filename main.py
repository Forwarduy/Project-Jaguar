"""
Project Jaguar - Multi-Agent AI Platform
Entry point
"""
import os
from dotenv import load_dotenv
import typer
from rich import print

load_dotenv()

app = typer.Typer(help="🐆 Jaguar - Open-source multi-agent AI platform")

@app.command()
def hello():
    print("[bold yellow]🐆 Jaguar v0.1.0[/] - Ready")
    print("Agents: Research, Outreach, Planning, Workflow")

@app.command()
def agents_list():
    print("[green]Available agents:[/]")
    print(" - Research Agent (market research)")
    print(" - Outreach Agent (cold email / LinkedIn)")
    print(" - Planning Agent (OKRs / roadmap)")
    print(" - Workflow Agent (n8n automation)")

if __name__ == "__main__":
    app()
