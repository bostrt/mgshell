import click

from mgshell.locator import findMustGather, findPodsInNamespace, getCurrentNamespace, findAllPods, getCurrentPod, findContainersInPod

from os import path

def get_pods(ctx, args, incomplete):
    mgbase = findMustGather()
    namespace = getCurrentNamespace()
    if mgbase is not None:
        if namespace is None:
            #pods = findAllPods(mgbase)
            return []
        elif namespace is not None:
            pods = findPodsInNamespace(mgbase, namespace)
        if pods is not None:
            return [p for p in pods if incomplete in p]
    return []

def get_containers(ctx, args, incomplete):
    mgbase = findMustGather()
    namespace = getCurrentNamespace()
    pod = getCurrentPod()
    if namespace is None and pod is None:
        return [] # TODO: Handle when no Pod is specified
    containers = findContainersInPod(mgbase, namespace, pod)
    if containers is None:
        return []
    return [c for c in containers if incomplete in c]

@click.command()
@click.argument("container", type=click.STRING, autocompletion=get_containers)
def log(container):
    mgbase = findMustGather()
    namespace = getCurrentNamespace()
    pod = getCurrentPod()
    if namespace is None and pod is None:
        return
    log = 'current.log'
    p = path.join(mgbase, 'namespaces', namespace, 'pods', pod, container, container, 'logs', log)
    try:
        with open(p, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print('Container "%s" not found' % container)