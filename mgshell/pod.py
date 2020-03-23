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
def pod(pod):
    mgbase = findMustGather()
    namespace = getCurrentNamespace()
    if namespace is None:
        try:
            ns, pname = pod.split('/')
            p = path.join(mgbase, 'namespaces', '%s/pods/%s' % (ns, pname))
            click.echo(p)
        except ValueError:
            #click.echo('Invalid pod name "%s"' % pod)
            return
    else:
        p = path.join(mgbase, 'namespaces', namespace, 'pods', pod)
        click.echo(p)
