from os import path

import click

from mgshell.locator import findMustGather, findNamespaces

def get_namespaces(ctx, args, incomplete):
    mgbase = findMustGather()
    if mgbase is not None:
        namespaces = findNamespaces(mgbase)
        if namespaces is not None:
            suggestions = [ns for ns in namespaces if incomplete in ns]
            return suggestions
    return []

@click.command()
@click.argument("namespace", type=click.STRING, autocompletion=get_namespaces)
def ns(namespace):
    mgbase = findMustGather()
    p = path.join(mgbase, "namespaces", namespace)
    click.echo(p)
