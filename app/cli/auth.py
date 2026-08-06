import os
import functools
import typer

def requires_auth(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            typer.echo("Error de Autenticación: La variable de entorno ANTHROPIC_API_KEY no está definida.", err=True)
            raise typer.Exit(code=1)
        return f(*args, **kwargs)
    return wrapper
