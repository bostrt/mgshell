from os import walk, path, scandir, listdir, getcwd

FIRST_LEVEL='must-gather.local'
SECOND_LEVEL='quay-io-openshift-release'
MGBASE=['audit_logs', 'cluster-scoped-resources', 'host_service_logs', 'namespaces', 'version']

def findMustGather(here=getcwd()):
    # TODO: Limit recursion by 4 or 5
    with scandir(here) as it:
        for entry in it:
            if entry.name.startswith(FIRST_LEVEL):
                return findMustGather(entry)
            if entry.name.startswith(SECOND_LEVEL):
                return findMustGather(entry)
            if entry.name in MGBASE:
                return here
    # TODO: Scan up too!

def findNamespaces(mgbase):
    listing = listdir(path.join(mgbase, 'namespaces'))
    return listing