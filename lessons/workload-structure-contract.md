# Workload Structure Contract

## Meaning

Different AI workloads encode similar ideas in different custom resources. A structure contract describes where those ideas live, so schedulers, dashboards, and policy tools can share a reviewed interpretation instead of each hardcoding every workload schema.

## Mechanism

A [[kubernetes-operator]] manages a custom resource whose nested fields describe groups of [[kubernetes-pod]] templates, replica counts, roles, and status. A descriptor maps these fields into a standard structural view. Workload Map provides a concrete example using declarative path expressions and an offline Go library. Consumers can extract the view and translate supported scheduling instructions into their own primitives. The descriptor is not itself a scheduler, autoscaler, or distributed runtime. A field mapping must preserve semantic meaning: desired replicas are not ready replicas, and the existence of a group does not by itself establish its minimum viable gang.

## One example

One resource describes two model replicas, each with one leader and three workers. Its structural view contains two groups and eight Pods: 2×(1+3). Another resource stores the leader template and worker count under different paths. Two descriptors can expose the same roles to a dashboard without changing that dashboard. But mapping a total worker count as “workers per group” would double-count or misconfigure capacity. Version descriptors with resource schemas, test empty and partial objects, and verify round-trip updates leave unrelated fields intact. Validate observed status against live Pods and preserve unknown states instead of presenting them as healthy.

## Check your understanding

Does a common descriptor remove all per-workload expertise? No. Someone must author and validate each mapping and the meaning of its roles, status, and group constraints.
