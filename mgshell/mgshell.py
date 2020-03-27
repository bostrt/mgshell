import os

import click

from mgshell.version import __version__

@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo("mgshell %s" % __version__)
