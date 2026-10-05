# Simulated Gpu Device Plugin

## Meaning

Kubernetes learns about GPU capacity through a **device plugin** that registers extended resources on a node. A simulated plugin can advertise test resources and exercise the platform control plane without owning real accelerator hardware. The boundary matters: successful scheduling is not successful CUDA execution.

## Mechanism

A real GPU deployment needs compatible drivers, runtime integration, a vendor plugin, and often operator-managed installation. The plugin reports capacity such as `nvidia.com/gpu`; a [[kubernetes-pod]] requests that resource, and the scheduler places it where capacity is advertised. A [[kubernetes-operator]] can reconcile the supporting components and labels. The [[device-driver]] and actual hardware are the separate execution layer.

In a local test cluster, a simulator or mocked management interface can supply predictable device identities. This is useful for verifying resource discovery, labels and selectors, placement, allocation accounting, operator reconciliation, and failure behavior when a node disappears. It does **not** prove that a kernel can run, memory is isolated, a GPU partition exists physically, or any throughput claim holds. A mock that overstates capacity can make a scheduling test pass while a real deployment fails.

## One example

A local Kubernetes cluster advertises mock GPU resources. A Pod request schedules correctly, but no CUDA kernel can run.

## Check your understanding

**Question:** What does a successful scheduling test leave unproved?

**Answer:** Driver and hardware compatibility, isolation, real partitioning, and performance.
