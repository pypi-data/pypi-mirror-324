import click

from src.commands import auth_group, run
from src.version import __version__


@click.group()
@click.version_option(version=__version__)
def cli():
    """Steev CLI - Command line interface for Steev"""


cli.add_command(auth_group)
cli.add_command(run)


if __name__ == "__main__":
    cli()
