---
id: memory-mapped-io
title: Memory-Mapped I/O
summary: Memory-mapped I/O places device registers or device memory in an address range so ordinary processor loads and stores become device operations.
type: concept
tags: [os/kernel]
prereqs: [virtual-memory, device-driver]
sources: [https://docs.kernel.org/driver-api/device-io.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Memory-Mapped I/O

## Summary

**Memory-mapped I/O (MMIO)** maps device registers or device memory into an address range, so processor loads and stores to that range are routed to hardware rather than ordinary RAM.

## Grounded explanation

A [[device-driver]] first obtains a device resource range and maps it into the kernel's [[virtual-memory]]. Reading an address in that mapping asks the device for a register value; writing it may configure a queue, acknowledge an event, or ring a command doorbell.

MMIO looks like memory in the instruction stream but has different semantics. Accesses may have side effects, ordering matters, and cached copies could be incorrect. Driver accessors therefore preserve the architecture's required width and ordering instead of treating registers as an ordinary byte array.

### Worked example

Suppose a controller exposes a 32-bit command register at offset `0x20` and a status register at `0x24`. The driver maps the resource base as `B`, writes command value 3 to `B+0x20`, then reads `B+0x24` until a completion bit appears. The write is not storing 3 in RAM; it is a message to the controller. The read obtains current device state.

MMIO is appropriate for control and small windows. Bulk buffers are usually transferred with another mechanism because having the processor load and store every word wastes CPU work.

## Prerequisites

- [[virtual-memory]]
- [[device-driver]]

## Sources

- Linux kernel driver API, “Device I/O access” — resource mapping and ordered register accessors.
