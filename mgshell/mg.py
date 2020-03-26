import os
from pathlib import Path

from mgshell.version import __version__

MARKER_SEARCH_LIMIT=10
MARKER='.mgshell'


class Locator:
    def __init__(self, cwd=os.getcwd()):
        self.cwd = cwd
        self.mgbase = self._findMustGatherRoot()
    
    def _findMustGatherRoot(self):
        # Attempt the fast marker file based search
        dir = self._findMustGatherRootFast()
        if dir is not None:
            return dir
        # Attempt slower root search
        dir = self._findMustGatherRootSlow()
        if dir is not None:
            # Drop marker for fast lookup later
            self._dropMarker(dir)
            return dir
        return None

    def _findMustGatherRootFast(self):
        depth = 0
        dir = self.cwd
        while depth < MARKER_SEARCH_LIMIT:
            if self._detectMarker(dir):
                return dir
            dir = os.path.dirname(dir)
            depth = depth + 1

    def _detectMarker(self, dir):
        try:
            os.stat(os.path.join(dir, MARKER))
            return True
        except:
            return False
    
    def _dropMarker(self, dir):
        """Create marker file inside must gather."""
        new = os.path.join(dir, MARKER)
        try:
            p = Path(new)
            p.touch()
            p.write_text(__version__)
            return new
        except FileExistsError:
            return new
        except FileNotFoundError:
            return None

    def _findMustGatherRootSlow(self):
        depth = 0
        dir = self.cwd
        while depth < MARKER_SEARCH_LIMIT:
            listing = os.listdir(dir)
            if 'namespaces' in listing:
                return dir
            dir = os.path.dirname(dir)
            depth = depth + 1

    def isMGFound(self):
        return self.mgbase is not None

    def getMustGatherRoot(self):
        return self.mgbase
    
    def getNamespaceList(self):
        """Return a list of Namespace names in must gather."""
        try:
            listing = os.listdir(os.path.join(self.mgbase, 'namespaces'))
            return listing
        except FileNotFoundError:
            return None

    def getPodList(self):
        """Return a list of namespace and Pod names in that namespace.
        Return list form:
        ["openshift-sdn/sdn-mb3ban", "openshift-sdn/ovs-kg4rs", ...]
        """
        try:
            ret = []
            listing = os.listdir(os.path.join(self.mgbase, 'namespaces'))
            for ns in listing:
                pods = self.getPodListInNamespace(ns)
                if pods is not None:
                    # Append to return list, but with ns prepending to each pod
                    ret = ret + [ns + '/' + p for p in pods]
            return ret
        except FileNotFoundError:
            return None

    def getPodListInNamespace(self, namespace):
        """Return a list of Pod names in a namespace. 
        If namespace is None, returns None. 
        If namespace is specified but no Pods found, returns empty list.
        TODO: Should this return empty list even when ns is None?
        """
        if namespace is not None:
            try:
                listing = os.listdir(os.path.join(self.mgbase, 'namespaces', namespace, 'pods'))
                return listing
            except FileNotFoundError:
                return None
        else:
            return None

    def getNamespacePath(self, namespace):
        return os.path.join(self.mgbase, 'namespaces', namespace)

    def getPodPath(self, pod, namespace=None):
        if namespace is None:
            try:
                ns, pname = pod.split('/')
                p = os.path.join(self.mgbase, 'namespaces', '%s/pods/%s' % (ns, pname))
                return p
            except ValueError:
                #click.echo('Invalid pod name "%s"' % pod)
                return None
        else:
            p = os.path.join(self.mgbase, 'namespaces', namespace, 'pods', pod)
            return p


class CurrentContext:
    def __init__(self, locator):
        self.locator = locator

    def getCurrentNamespace(self, here=os.getcwd()):
        """Return the namespace name for input. Default input is current working directory."""
        if 'namespaces' in here:
            basename = os.path.basename(here)
            parentDir = os.path.dirname(here)
            parentBasename = os.path.basename(parentDir)
            if parentBasename == 'namespaces':
                return basename
            else:
                return self.getCurrentNamespace(parentDir)
        else:
            return None

