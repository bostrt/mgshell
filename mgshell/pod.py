import click

from mgshell.locator import findMustGather, findPods, getCurrentNamespace

from os import path

def get_pods(ctx, args, incomplete):
    mgbase = findMustGather()
    namespace = getCurrentNamespace()
    if mgbase is not None:
        pods = findPods(mgbase, namespace)
        if pods is not None:
            return [p for p in pods if incomplete in p]
    return []

@click.command()
@click.argument("pod", type=click.STRING, autocompletion=get_pods)
def pod(pod):
    mgbase = findMustGather()
    p = path.join(mgbase, "namespaces", pod)
    click.echo(p)

# eval "$(_NS_COMPLETE=source_bash ns)"
# function ns() { cd $(~/code/mgshell/v/bin/ns $1); }