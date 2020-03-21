import click

from mgshell.version import __version__
from mgshell.findmg import findMustGather, findNamespaces

from os import path

def get_namespaces(ctx, args, incomplete):
    mgbase = findMustGather()
    if mgbase is not None:
        namespaces = findNamespaces(mgbase)
        if namespaces is not None:
            return [ns for ns in namespaces if incomplete in ns]

@click.command()
@click.argument("namespace", type=click.STRING, autocompletion=get_namespaces)
def ns(namespace):
    mgbase = findMustGather()
    p = path.join(mgbase, "namespaces", namespace)
    click.echo(p)

# eval "$(_NS_COMPLETE=source_bash ns)"
# function ns() { cd $(~/code/mgshell/v/bin/ns $1); }