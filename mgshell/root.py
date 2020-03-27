import click

from mgshell.gps import Locator

import os

@click.command()
def root():
    locator = Locator()
    if locator.isMGFound():
        click.echo(locator.getMustGatherRoot())
    else:
        # Don't go anywhere
        click.echo(os.getcwd())