---
id: io-interconnect
title: I/O Interconnect
summary: An I/O interconnect is the layered link and switching fabric that transports addressed requests, responses, and data between processors and peripheral devices.
type: concept
tags: [os/kernel]
prereqs: [device-driver]
sources: [https://docs.kernel.org/PCI/pci.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# I/O Interconnect

## Summary

An **I/O interconnect** connects processors to peripheral devices through links and optional switches, carrying addressed requests, completions, and data between a host and the hardware managed by a [[device-driver]].

## Grounded explanation

A [[device-driver]] issues operations to a device, but those operations need a physical and protocol path. An I/O interconnect supplies that path. Endpoints are identified, links have finite width and rate, switches route traffic, and a protocol specifies request and response messages.

### Worked example

A host reads a status register from a storage controller. The processor emits an addressed read request; switches route it toward the controller; the endpoint returns a completion containing the value. A later bulk transfer may use the same fabric for thousands of data-bearing messages. The first operation is latency-sensitive and small; the second is bandwidth-sensitive and large.

The usable throughput is bounded by the narrowest shared link and protocol overhead, not only by the endpoint's internal speed. Multiple devices behind one upstream link contend for that link even if each has a fast local connection.

## Prerequisites

- [[device-driver]]

## Sources

- Linux kernel PCI documentation — host bridges, buses, devices, resources, and driver-visible operation.
