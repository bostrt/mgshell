import os

import click

from mgshell.version import __version__
from mgshell.locator import findMustGatherRootDir, dropMarker, findMustGatherRootDirFast

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

PROMPT_PATTERN="[mgshell %s] > "

def prompt():
    cwd = os.getcwd()
    mgbase = findMustGatherRootDirFast()
    if mgbase is None:
        return
    subpath = cwd.replace(mgbase, '')
    subpath = promptFilter(subpath)
    print(PROMPT_PATTERN % (subpath or '/'))

def promptFilter(subpath):
    if subpath is None or subpath == '':
        return ''
    subpath = subpath.replace('amespace', '')
    if 'pods' in subpath:
        subpath = trimContainers(subpath)
    return subpath

def trimContainers(subpath):
    return subpath