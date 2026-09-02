---
id: pci-express
title: PCI Express
summary: PCI Express is a switched, point-to-point serial I/O interconnect that carries packetized memory, configuration, and completion transactions between a root complex and endpoints.
type: concept
tags: [os/kernel]
prereqs: [io-interconnect, memory-mapped-io, dma]
sources: [https://www.kernel.org/doc/html/latest/PCI/pcieaer-howto.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# PCI Express

## Summary

**PCI Express (PCIe)** is a switched, point-to-point serial [[io-interconnect]] that connects a host root complex to endpoints such as GPUs, network cards, and storage controllers using packetized transactions over one or more lanes.

## Grounded explanation

A PCIe topology is a tree: the root complex connects the processor and memory system; switches fan out; endpoints terminate links. A link contains one or more lanes, written ×1, ×4, ×8, or ×16. More lanes transmit more symbols in parallel, while the negotiated generation determines each lane's rate.

Software discovers an endpoint and assigns address ranges. Control accesses use [[memory-mapped-io]]: a host load or store becomes a transaction-layer packet (TLP) carrying an address, operation, requester identity, and optional payload. Reads return completion TLPs; posted writes need no data completion. Reliability layers add sequence and integrity checks, while the physical layer transmits symbols on the lanes.

For bulk movement, the host gives the device buffer addresses and the endpoint uses [[dma]] to read or write host memory across PCIe. MMIO usually rings the doorbell; DMA carries the large payload.

### Worked example

A host submits a 4-KB GPU input. First it writes a queue-tail register through [[memory-mapped-io]], creating a small posted write TLP. The GPU then performs [[dma]] reads for the buffer, split into legal payload-sized TLPs, and later signals completion. If the endpoint is behind a ×4 link whose effective payload rate is roughly 1 GB/s per lane for the chosen generation, the link ceiling is roughly 4 GB/s before additional overhead; placing a nominally faster device there cannot exceed that path.

PCIe performance therefore depends on topology, negotiated width and rate, payload size, and contention at upstream links. Error reporting distinguishes correctable link errors from uncorrectable transaction or link failures; a working device can still be degraded by retraining to fewer lanes or a lower generation.

## Prerequisites

- [[io-interconnect]]
- [[memory-mapped-io]]
- [[dma]]

## Sources

- Linux kernel, “PCI Express Advanced Error Reporting Driver Guide” — links, transactions, TLP headers, root ports, and error classes.
