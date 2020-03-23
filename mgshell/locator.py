import os
from pathlib import Path
import stat

from mgshell.version import __version__

FIRST_LEVEL='must-gather.local'
SECOND_LEVEL='quay-io-openshift-release'
MGDIRS={'audit_logs', 'cluster-scoped-resources', 'host_service_logs', 'namespaces', 'version'}
MARKER='.mgshell'

def findMustGatherRootDir(here=os.getcwd(), depth=0):
    """Return root directory of must gather.
       The root of must gather is the directory containing folks such as:
       - namespaces
       - audit_logs
       - etc...
    """
    if detectMarker(here):
        # Always do the quickest check for the marker file
        return here
    if depth > 3 or depth < -10:
        # Emergency give up.
        # 3 because we typically won't see a must gather 
        # outside of must-gather.xxx/quay-io-xxxx/
        # -10 because the deepest location we can be coming from
        # is a Pod's log directories, 9 or 10 down from must-gather.xxxx
        return None
    if SECOND_LEVEL in here:
        # We are either in the proper directory of too deep
        # TODO: Place a marker file for quicker detection later.
        listing = set(os.listdir(here))
        if len(listing & MGDIRS) > 0:
            # We're there
            return here
        # Continue checking up directories
        return findMustGatherRootDir(os.path.dirname(here), depth-1)
    elif FIRST_LEVEL in here:
        # If we're in this block, there's no mention of quay-io-blah
        # in the CWD, meaning we need to dig in more:
        with os.scandir(here) as it:
            for entry in it:
                return findMustGatherRootDir(entry.name, depth+1)

def findMustGather(here=os.getcwd()):
    """Return root directory of must gather and drop marker file.
       The root of must gather is the directory containing folks such as:
       - namespaces
       - audit_logs
       - etc...
    """
    rootDir = findMustGatherRootDir(here)
    if rootDir is not None:
        dropMarker(rootDir)
    return rootDir

def dropMarker(mgbase):
    """Create marker file inside must gather."""
    new = os.path.join(mgbase, MARKER)
    try:
        p = Path(new)
        p.touch()
        p.write_text(__version__)
        return new
    except FileExistsError:
        return new
    except FileNotFoundError:
        return None

def detectMarker(dir):
    """Return True if marker file is present inside must gather."""
    try:
        result = os.stat(os.path.join(dir, MARKER))
        return stat.S_ISREG(result)
    except:
        return False

def findNamespaces(mgbase):
    """Return a list of Namespace names in must gather."""
    try:
        listing = os.listdir(os.path.join(mgbase, 'namespaces'))
        return listing
    except FileNotFoundError:
        return None

def findAllPods(mgbase):
    """Return a list of namespace and Pod names in that namespace.
       Return list form:
       ["openshift-sdn/sdn-mb3ban", "openshift-sdn/ovs-kg4rs", ...]
    """
    try:
        ret = []
        listing = os.listdir(os.path.join(mgbase, 'namespaces'))
        for ns in listing:
            pods = findPodsInNamespace(mgbase, ns)
            if pods is not None:
                # Append to return list, but with ns prepending to each pod
                ret = ret + [ns + '/' + p for p in pods]
        return ret
    except FileNotFoundError:
        return None

def findPodsInNamespace(mgbase, namespace):
    """Return a list of Pod names in a namespace. 
       If namespace is None, returns None. 
       If namespace is specified but no Pods found, returns empty list.
       TODO: Should this return empty list even when ns is None?
    """
    if namespace is not None:
        try:
            listing = os.listdir(os.path.join(mgbase, 'namespaces', namespace, 'pods'))
            return listing
        except FileNotFoundError:
            return None
    else:
        return None

def findContainers(mgbase, namespace, pod):
    pass

def findContainerLogs(mgbase, namespace, pod, container, previous, insecure):
    pass

def getCurrentNamespace(here=os.getcwd()):
    """Return the namespace name for input. Default input is current working directory."""
    if 'namespaces' in here:
        basename = os.path.basename(here)
        parentDir = os.path.dirname(here)
        parentBasename = os.path.basename(parentDir)
        if parentBasename == 'namespaces':
            return basename
        else:
            return getCurrentNamespace(parentDir)
    else:
        return None
