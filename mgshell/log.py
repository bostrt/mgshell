import click

from mgshell.gps import Locator, CurrentContext

from os import path

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
    # We got nothin
    return []

@click.command()
@click.pass_context
@click.argument("container", type=click.STRING, autocompletion=get_containers)
def log(ctx, container):
    locator = Locator()

    if not locator.isMGFound():
        click.echo('Container "%s" not found' % container, err=True)
        ctx.exit(2)
    
    mgctx = CurrentContext()
    namespace = mgctx.getCurrentNamespace()
    pod = mgctx.getCurrentPod()

    logPath = locator.getContainerLogPath(namespace, pod, container)
    if logPath is None:
        click.echo('Container "%s" not found' % container, err=True)
        ctx.exit(1)
    else:
        try:
            stdout = click.get_text_stream('stdout')
            with open(logPath, 'r') as f:
                stdout.write(f.read())
        except FileNotFoundError:
            click.echo('Container "%s" not found' % container, err=True)
            ctx.exit(1)
