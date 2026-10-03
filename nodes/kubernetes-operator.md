---
id: kubernetes-operator
title: Kubernetes Operator
summary: A Kubernetes Operator combines a custom resource with a controller that repeatedly reconciles declared application state against observed cluster state.
type: concept
tags: [os/virtualization]
prereqs: [kubernetes-pod]
sources: [https://kubernetes.io/docs/concepts/extend-kubernetes/operator/, https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Kubernetes Operator

## Summary

A **Kubernetes Operator** extends the cluster with an application-specific declarative API and a controller. The user states a desired configuration; the controller observes the cluster and repeatedly works to make actual state match it.

## Grounded explanation

A custom resource is an API object for a type not built into the base installation. A controller watches those objects and related cluster resources, compares desired and observed state, then creates, updates, or removes dependent objects. Reconciliation must be repeatable: a retry after a crash should not duplicate effects, and drift after a manual change should be detectable. The operator can manage the lifecycle of a [[kubernetes-pod]] and related resources without requiring a user to issue every low-level change.

An observability operator, for example, might watch a monitoring custom resource, install collection components, and arrange instrumentation for selected new Pods. The operator pattern does not guarantee that every workload is instrumented: selector scope, webhook admission failures, version compatibility, permissions, and update order matter. A mutating webhook or a CSI driver is an optional implementation mechanism, not the definition of an operator.

Prefer an operator when application lifecycle knowledge and recurring reconciliation justify adding a cluster controller. A static manifest or a simple deployment job is easier to operate for a fixed configuration. Validate convergence after creation and drift, retry/idempotency after controller restart, rollout and rollback, coverage of newly scheduled workloads, resource use, and failure reporting. Separate operator health from the health of the application it manages.

## Prerequisites

- [[kubernetes-pod]]

## Sources

- [Kubernetes Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/): controller and custom-resource architecture.
- [Kubernetes custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/): desired state and custom-controller responsibilities.
