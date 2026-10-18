# Dynamic Resource Allocation

## Meaning

Dynamic Resource Allocation (DRA) expresses device needs through structured claims rather than only integer counts of a vendor resource. The reusable idea is separating the workload’s device requirements from discovery, selection, and device-specific preparation.

## Mechanism

A [[device-driver]] publishes available devices through ResourceSlices. Administrators define DeviceClasses; a ResourceClaim or a template describes the workload’s required class, attributes, and configuration. The [[kubernetes-pod]] refers to the claim, and allocation coordinates a device choice with a node where the Pod can use it. Node-side preparation makes the allocated device available to containers. Attribute filtering and explicit claims allow richer compatibility decisions than “one GPU.” DRA does not create physical capacity, make every device safely shareable, or supply gang admission by itself. Sharing and configuration need driver support; capabilities and scheduler limitations remain version-specific.

## One example

A cluster advertises a 24-GiB accelerator on node A and an 80-GiB accelerator on node B. A claim requiring at least 48 GiB filters out A before placement. A one-device integer request without that attribute could select an unsuitable device. Two Pods that reference the same shareable claim need a documented sharing contract; duplicating a claim name is not proof of independent 48-GiB allocations. Test missing classes, incompatible attributes, exhausted capacity, failed node preparation, claim cleanup, and Pod rescheduling. Inspect actual device access inside a running container as well as the allocation record. Do not assume ordinary priority preemption behaves identically for DRA and integer resources.

## Check your understanding

Is a successful ResourceClaim allocation the same as a successful application kernel? No: container preparation, driver compatibility, and actual execution remain necessary checks.
