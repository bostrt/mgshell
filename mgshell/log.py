import click

from mgshell.gps import Locator, CurrentContext

from os import path

def get_pods(ctx, args, incomplete):
    locator = Locator()
    mgctx = CurrentContext()

    if locator.isMGFound():
        namespace = mgctx.getCurrentNamespace()
        if namespace is None:
            # TODO: Right now we're gonna require you be in a namespace
            return []
        pods = locator.getPodListInNamespace(namespace)
        if pods is None:
            return []
        return [p for p in pods if incomplete in p]
    # We got nothin
    return []

def get_containers(ctx, args, incomplete):
    locator = Locator()
    mgctx = CurrentContext()

    if locator.isMGFound():
        namespace = mgctx.getCurrentNamespace()
        pod = mgctx.getCurrentPod()
        if namespace is None or pod is None:
            return []
        containers = locator.getContainerListInPod(namespace, pod)
        if containers is None:
            return []
        return [c for c in containers if incomplete in c]

@click.command()
@click.argument("container", type=click.STRING, autocompletion=get_containers)
def log(container):
    locator = Locator()
    mgctx = CurrentContext()
    namespace = mgctx.getCurrentNamespace()
    pod = mgctx.getCurrentPod()

    logPath = locator.getContainerLogPath(namespace, pod, container)
    if logPath is None:
        click.echo('Container "%s" not found' % container)
    try:
        stdout = click.get_text_stream('stdout')
        with open(logPath, 'r') as f:
            stdout.write(f.read())
    except FileNotFoundError:
        click.echo('Container "%s" not found' % container)
