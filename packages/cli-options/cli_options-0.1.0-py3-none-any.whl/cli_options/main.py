import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.callback()
def callback():
    """
    First package buid.
    """
   

@app.command()
def create(name: Annotated[str, typer.Argument(...)]):
    """
    Create a new user.
    """
    typer.echo(f"Creating {name}")

@app.command()
def delete(name: Annotated[str, typer.Argument(...)]):
    """
    Delete a user.
    """
    typer.echo(f"Deleting {name}")

