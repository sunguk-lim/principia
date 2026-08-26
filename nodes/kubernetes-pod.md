---
id: kubernetes-pod
title: Kubernetes Pod
summary: A Kubernetes Pod is the smallest deployable unit Kubernetes schedules: one or more co-located containers that share one network identity and lifecycle boundary.
type: concept
tags: [os/virtualization]
prereqs: [container, container-networking]
sources:
  - https://kubernetes.io/docs/concepts/workloads/pods/
status: explained
created: 2026-08-26
updated: 2026-08-26
---

# Kubernetes Pod

## Summary

A **Kubernetes Pod** is the smallest unit Kubernetes schedules onto a machine. A Pod contains one or
more tightly coupled [[container]]s that must run together. Those containers share one network
identity supplied by [[container-networking]]: one IP address, one set of ports, and `localhost`
between them. Kubernetes creates, places, and replaces the Pod as one lifecycle unit rather than
treating each contained process as an independently located machine.

## Grounded explanation

### Why Kubernetes needs a unit above a container

A [[container]] isolates and limits a process, but it does not say which other processes must be
placed beside it or which network identity those processes should share. Kubernetes needs a unit it
can schedule: something that can be assigned to one machine, started, observed, and replaced as a
whole. That unit is the Pod.

Most Pods contain one application container. A Pod may contain additional **sidecar containers** when
those helpers are meaningful only beside that application—for example, a helper that reads the
application's local output and exports it. Because every container in the Pod is co-located, the
application and helper begin from the same placement decision and disappear when that Pod is
replaced.

### One shared network identity

[[container-networking]] can give isolated containers separate interfaces and addresses. A Pod draws
a different boundary: all containers inside it participate in one shared network world. They see the
same Pod IP address and the same port space, so two containers in one Pod cannot both claim the same
port. They can reach each other through `localhost` because, from the network's point of view, they
occupy one host-like endpoint.

Containers in different Pods do not share that identity. Each Pod receives its own address, and
traffic between Pods crosses the cluster network. The Pod is therefore both a scheduling boundary
and a network endpoint.

### Worked instance: application plus helper

Consider a Pod assigned IP `10.42.1.17`. Its application container listens on port `8080`. A helper
container in the same Pod reads from the application on `localhost:8080`; it does not need to discover
another address because both containers share the Pod's network identity. From outside the Pod, the
application is reached as `10.42.1.17:8080`.

If the machine hosting this Pod fails, Kubernetes may create a replacement Pod elsewhere. The new Pod
contains the same container definitions but receives a different identity, perhaps `10.42.3.9`.
Kubernetes does not move the old Pod's identity into the new object; it replaces one disposable Pod
with another. This replacement behavior is why clients should not treat a particular Pod IP as a
durable application address. A higher-level mechanism must provide continuity across changing Pods.

### The boundary

A Pod is not a long-lived server and not merely another name for a container. It is the wrapper that
tells Kubernetes which containers are inseparable for placement and lifecycle, and gives that group
one shared network identity. Independent application replicas normally occupy separate Pods so each
replica can be placed, replaced, and addressed independently.

## Prerequisites

- [[container]]
- [[container-networking]]

## Sources

- [Kubernetes documentation — Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
