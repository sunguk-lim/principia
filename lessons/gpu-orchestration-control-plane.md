# GPU Orchestration Control Plane

## Meaning

A GPU platform is not just a scheduler. It combines several decision layers whose outputs must remain consistent even when they are implemented by separate controllers. Modularity is useful only when the boundaries and failure states are explicit.

## Mechanism

A [[workload-structure-contract]] exposes roles and demand. [[hierarchical-resource-quotas]] expresses who may consume resources. [[topology-aware-workload-placement]] chooses compatible locations, while [[gpu-sharing-enforcement]] determines what a running process can actually allocate. Scheduling intent and runtime fact must be reconciled rather than equated. Each controller needs versioned inputs, ownership of its writes, observable status, and an idempotent recovery path. A normalized workload view need not be a scheduler; a quota controller need not enforce device memory. This separation lets components evolve independently but creates cross-layer consistency obligations.

## One example

A project is entitled to four GPUs and submits a two-role job. The workload adapter correctly finds the roles, quota admits four, and placement chooses a compatible node. If the node runtime lacks the required memory-limit support, a fractional-memory job is not safely enforced merely because the first three layers succeeded. The platform should expose the unsupported runtime state and avoid advertising the requested guarantee. Conversely, a driver can enforce a memory cap without knowing the department’s historical fair share. Trace one workload identity across policy, allocation, device preparation, actual usage, and readiness; test stale labels, controller restart, partial reconciliation, and mismatched component versions.

## Check your understanding

Can one component’s success condition stand in for platform correctness? No. Correct entitlement, placement, enforcement, and useful service are separate claims that require linked evidence.
