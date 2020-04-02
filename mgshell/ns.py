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
@click.pass_context
@click.argument("namespace", type=click.STRING, autocompletion=get_namespaces)
def ns(ctx, namespace):
    locator = Locator()
    if locator.isMGFound():
        try:
            click.echo(locator.getNamespacePath(namespace))
        except:
            # I don't know what could happen here but be prepared
            click.echo('Failure locating Namespace "%s"' % namespace, err=True)
            ctx.exit(1)
    else:
        # Namespace couldn't be found. Log an error and set exit code.
        click.echo('Namespace "%s" not found' % namespace, err=True)
        ctx.exit(1)
    