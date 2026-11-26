---
id: gpu-interprocess-memory-sharing
title: "GPU Interprocess Memory Sharing"
summary: "GPU interprocess memory sharing exports a device-allocation handle so another process can map the same underlying storage under explicit lifetime and synchronization rules."
type: concept
tags: [gpu/programming-models]
prereqs: [process, gpu-data-flow]
sources: [https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html, https://docs.pytorch.org/docs/2.15/multiprocessing.html]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# GPU Interprocess Memory Sharing

## Meaning

GPU interprocess sharing lets two processes access one compatible device allocation without serializing its entire payload through a host message. It shares storage identity, not a numeric pointer value. A [[process]] has its own address space, so sending an address alone does not establish a usable mapping in the receiver.

## Mechanism

The producer allocates supported GPU memory and exports an interprocess handle. It sends that handle and the necessary shape, layout and ownership metadata over a permitted host communication path. The consumer imports the handle and receives a pointer valid in its own process. That pointer may differ numerically from the producer's while referring to the same underlying allocation.

Access still needs ordering. The [[gpu-data-flow]] execution model is asynchronous: a handle arriving does not prove that an earlier device write has completed. Establish the required completion dependency before reading, prevent conflicting writes, and keep storage alive until every consumer has finished. Close imported mappings before the producer frees the backing allocation, following the runtime's supported lifetime contract. Recovery from an abnormal exit needs its own policy.

NVIDIA's CUDA runtime documents export, open and close operations. PyTorch's CUDA tensor-sharing documentation additionally requires the producer to remain alive while a consumer retains the tensor, and specifies supported process start methods. These implementation rules must not be generalized to arbitrary allocators, operating systems or accelerators.

## One example

Producer A owns a 16 MiB buffer containing four equal 4 MiB blocks. Consumer B imports its handle and reads block 3 after A signals that the write is complete. Both mappings refer to that same block; the protocol did not need to send another 16 MiB payload merely to establish B's view. B acknowledges completion and closes its mapping before A reclaims the buffer. Freeing it immediately after sending the handle would race B's future read.

## Boundaries and validation

Avoiding a process-boundary payload copy does not eliminate device-to-host restoration or remote-device traffic. Sharing across devices depends on the supported topology and runtime; it is not automatic zero-copy access between every pair of GPUs. Test producer/consumer exit, delayed writes, stale handles, concurrent reuse and invalid layouts. Trace actual copies and compare checksums or numerical results with an explicit-copy baseline.

**Check:** Does importing a handle also synchronize previous writes? Not by that fact alone. Mapping, completion and lifetime are separate obligations.

## Sources

- <https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html>
- <https://docs.pytorch.org/docs/2.15/multiprocessing.html>
