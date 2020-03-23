import os

import click

from mgshell.version import __version__
from mgshell.locator import findMustGatherRootDir, dropMarker

@click.group()
def cli():
    pass

@cli.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True), default='.')
def init(path):
    #  TODO: Accept directories other than must-gather-xxx/quay-io-xxxx/
    path = os.path.abspath(path)
    mgbase = findMustGatherRootDir(path)
    if mgbase is not None and mgbase == path:
        dropMarker(mgbase)
    else:
        click.echo("Unable to initialize must gather")

@cli.command()
def version():
    click.echo("mgshell %s" % __version__)
