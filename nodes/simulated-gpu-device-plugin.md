---
id: simulated-gpu-device-plugin
title: Simulated GPU Device Plugin
summary: A simulated GPU device plugin advertises fake accelerator resources to Kubernetes for testing discovery, scheduling, and operator reconciliation while providing no evidence of real GPU execution or performance.
type: concept
tags: [os/virtualization]
prereqs: [kubernetes-pod, kubernetes-operator, device-driver]
sources: [https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/, https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/, https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Simulated GPU Device Plugin

## Summary

Kubernetes learns about GPU capacity through a **device plugin** that registers extended resources on a node. A simulated plugin can advertise test resources and exercise the platform control plane without owning real accelerator hardware. The boundary matters: successful scheduling is not successful CUDA execution.

## Grounded explanation

A real GPU deployment needs compatible drivers, runtime integration, a vendor plugin, and often operator-managed installation. The plugin reports capacity such as `nvidia.com/gpu`; a [[kubernetes-pod]] requests that resource, and the scheduler places it where capacity is advertised. A [[kubernetes-operator]] can reconcile the supporting components and labels. The [[device-driver]] and actual hardware are the separate execution layer.

In a local test cluster, a simulator or mocked management interface can supply predictable device identities. This is useful for verifying resource discovery, labels and selectors, placement, allocation accounting, operator reconciliation, and failure behavior when a node disappears. It does **not** prove that a kernel can run, memory is isolated, a GPU partition exists physically, or any throughput claim holds. A mock that overstates capacity can make a scheduling test pass while a real deployment fails.

Use the mock for cheap control-plane regression tests and a small real-hardware validation gate for device execution, runtime compatibility, partitioning, and performance. In tests, create Pods requesting one and more GPUs, verify scheduling and unschedulable states, remove a simulated device, and inspect reconciliation and error reporting. Compare resource labels and allocation behavior with Kubernetes and vendor documentation. Cost arithmetic from one person's laptop setup is not a benchmark for production GPU economics.

## Prerequisites

- [[kubernetes-pod]]
- [[kubernetes-operator]]
- [[device-driver]]

## Sources

- [Kubernetes device plugins](https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/): resource registration contract.
- [Kubernetes GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/): GPU extended-resource requests.
- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/): operator-managed GPU software components.
