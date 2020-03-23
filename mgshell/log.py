import click

from mgshell.locator import findMustGather, findPodsInNamespace, getCurrentNamespace, findAllPods

from os import path

def get_pods(ctx, args, incomplete):
    mgbase = findMustGather()
    namespace = getCurrentNamespace()
    if mgbase is not None:
        if namespace is None:
            pods = findAllPods(mgbase)
        elif namespace is not None:
            pods = findPodsInNamespace(mgbase, namespace)
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