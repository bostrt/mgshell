import click

from mgshell.locator import findMustGather, findPods

from os import path

def get_pods(ctx, args, incomplete):
    # TODO: Support tabbing Pod and then Container
    mgbase = findMustGather()
    if mgbase is not None:
        pods = findPods(mgbase)
        if pods is not None:
            return [p for p in pods if incomplete in p]
    return []

@click.command()
@click.argument("pod", type=click.STRING, autocompletion=get_pods)
def log(pod):
    mgbase = findMustGather()
    p = path.join(mgbase, "namespaces", pod)
    click.echo(p)
    # TODO: Support -p flag for previous log and -k for insecure