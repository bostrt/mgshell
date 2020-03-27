from os import path

import click

from mgshell.gps import Locator

def get_namespaces(ctx, args, incomplete):
    locator = Locator()
    if locator.isMGFound():
        namespaces = locator.getNamespaceList()
        if namespaces is not None:
            suggestions = [ns for ns in namespaces if incomplete in ns]
            return suggestions
    return []

@click.command()
@click.argument("namespace", type=click.STRING, autocompletion=get_namespaces)
def ns(namespace):
    locator = Locator()
    click.echo(locator.getNamespacePath(namespace))
