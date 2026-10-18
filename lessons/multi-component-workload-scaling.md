# Multi-Component Workload Scaling

## Meaning

When one useful service instance spans several roles or machines, the scaling unit is no longer necessarily one Pod. The controller must preserve a viable composition and treat admission, process launch, readiness, and request routing as different events.

## Mechanism

A [[kubernetes-operator]] reconciles desired component counts. [[gang-scheduling]] makes their resource minimums jointly feasible; it does not impose launch order or readiness. Startup dependencies specify which role must become available before another begins, and must not form a cycle. In [[prefill-decode-disaggregation]], prefill capacity alone cannot complete a request if no decode path is available. Hierarchical group definitions can express one model instance’s workers and a larger service’s required roles. Autoscaling may change whole groups while allowing role-specific ratios within a viable configuration. Constraints and exact API support depend on the chosen controller and scheduler.

## One example

One service replica requires one prefill Pod and two decode Pods, each using one GPU. Two replicas need six GPUs. If only five are available, a policy requiring whole three-Pod replicas cannot claim two ready replicas; it can admit one and queue the other. Adding two decode Pods to the first replica is a different decision from adding a second complete replica. A startup rule might wait for workers before launching a leader, even though all were admitted together. Measure end-to-end readiness and successful requests, not just running Pod counts. Test worker failure, restart, downscaling, demand imbalance, dependency cycles, and update behavior while requests are active.

## Check your understanding

Do all members of an admitted gang have to execute their applications simultaneously? No. They may reserve capacity together but follow an explicit initialization order. Readiness still needs application-level evidence.
