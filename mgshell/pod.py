import click

from mgshell.locator import findMustGather, findPodsInNamespace, getCurrentNamespace, findAllPods
from mgshell.mg import Locator, CurrentContext

from os import path

def get_pods(ctx, args, incomplete):
    locator = Locator()
    mgctx = CurrentContext(locator)

    if locator.isMGFound():
        namespace = mgctx.getCurrentNamespace()
        if namespace is None:
            pods = locator.getPodList()
        else:
            pods = locator.getPodListInNamespace(namespace)
        if pods is None:
            return []
        else:
            return [p for p in pods if incomplete in p]

@click.command()
@click.argument("pod", type=click.STRING, autocompletion=get_pods)
def pod(pod):

    locator = Locator()
    mgctx = CurrentContext(locator)
    namespace = mgctx.getCurrentNamespace()

    click.echo(locator.getPodPath(pod, namespace))