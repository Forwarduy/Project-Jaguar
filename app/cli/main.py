import typer
from sqlmodel import Session
from app.database import engine
from app.workflows.market_workflow import run_market_research_workflow
from app.cli.auth import requires_auth

app = typer.Typer(help="Project Jaguar CLI - Motor de Inteligencia")

@app.command("research")
@requires_auth
def research_command(
    query: str = typer.Option(..., help="Tema o producto a investigar"),
    market: str = typer.Option("Uruguay", help="Mercado objetivo")
):
    """Ejecuta el pipeline de investigación de mercado respaldado por Anthropic y SQLModel."""
    typer.echo(f"Iniciando investigación para: [bold green]{query}[/bold green] en {market}...")
    
    with Session(engine) as session:
        try:
            result = run_market_research_workflow(session, query, market)
            typer.echo("\n[Workflow completado con éxito]")
            typer.echo(result.get("market_analysis", {}))
        except Exception as e:
            typer.echo(f"[Error en la ejecución]: {e}", err=True)
            raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
