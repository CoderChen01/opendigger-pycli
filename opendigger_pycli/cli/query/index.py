import click

from .. import opendigger


@click.command()
def index():
    """List all available dataloaders."""
