## Commands Needed

- cvo (cat cluster version operators and format)
- co (cat cluster operators and format)
- logs pod (get logs from first container)
- logs pod/container
- logs pod -p (previous logs)
- TODO: What about previous insecure log? (ingress-operator has example of this)


## REDESIGN

There's a ton of code duplication. I think this can all be cleaned up a lot. Specifically, the commands that move around directories can use some abstraction. The commands that simply print files too. I think these two types of commands are where I'll start:

### Commands

- `ChdirCommand`
	+ Abstract Method
		* 


- ChdirCommands
    + `NsChdir`
	    * Parameters:
		    - Namespace name
	    * Autocomplete
		    - List of namespaces
    + `PodChdir`
	    * Parameters
		    - Namespace name [optional]
		    - Pod name
	    * Autocomplete
		    - If no NS, list NS name and Pod name
		    - If NS, list Pod names within NS
- PrintCommands
	+ `ContainerLogPrint`
		* Parameters:
			- NOTE: Required to be in NS?
			- Pod name [optional if in Pod]
			- Container name 
		* Autocomplete
			- If in Pod, list of Container names
			- If not in Pod, list of Pod names and container names 
	+ `CVOPrint`
		* Parameters
			- None
		* Autocomplete
			- None
	+ `COPrint`
		* Parameters
			- Cluster Operator name [optional]
		* Autocomplete
			- List of CO names


### Utils

- `MGLocator`
	+ Functions
		* `dropMarker`
			- Drops a marker filter for quicker MG detection later
		* `detectMarker`
			- Checks if a marker has been dropped before
		* `getMustGatherRoot`
			- Locate the MG root where the namespaces, and cluster\_scoped\_resources live. 
				+ Once found, drop marker file
			- If a marker file is present, also use that
		* `getNamespaceList`
			- Get a list of all namespaces in  MG
		* `getPodList`
			- Get a list of pods in the given namespace or all namespaces if none is provided
		* `getContainerList`
			- Get a list of all containers in a given Pod or all Containers in all Pods if none is given