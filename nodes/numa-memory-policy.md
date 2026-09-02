---
id: numa-memory-policy
title: NUMA Memory Policy
summary: NUMA memory policy controls which NUMA nodes supply the physical pages backing a task or virtual-memory region.
type: concept
tags: [os/memory]
prereqs: [numa-architecture, page, virtual-memory, page-fault]
sources: [https://docs.kernel.org/admin-guide/mm/numa_memory_policy.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# NUMA Memory Policy

## Summary

A **NUMA memory policy** tells the operating system which NUMA node or node set should supply the physical [[page]]s that back a task or region of [[virtual-memory]].

## Grounded explanation

On a [[numa-architecture]], choosing where code runs is only half of locality; the operating system must also choose where newly allocated physical pages reside. Policies commonly express four intentions: use the local node, prefer one node but fall back, bind allocations to a set, or interleave pages across a set.

Policy applies when a physical [[page]] is allocated, often at the first [[page-fault]]. Existing pages normally stay where they are unless explicitly migrated. A [[virtual-memory]] range can therefore span pages on several NUMA nodes even though its addresses look contiguous to the process.

### Worked example

A thread on node 1 allocates and first writes four 4-KB pages under local policy. The allocator places all four on node 1. Under interleave policy across nodes 0 and 1, the pages alternate 0,1,0,1, spreading bandwidth. Under bind-to-node-0, all four come from node 0 even though the thread runs on node 1, creating remote access by construction.

Local policy minimizes distance for the allocating CPU; interleaving can use aggregate bandwidth for a shared scan; binding provides predictability. The correct choice follows the access pattern, and memory pressure may trigger documented fallback behavior.

## Prerequisites

- [[numa-architecture]]
- [[page]]
- [[virtual-memory]]

## Sources

- Linux kernel documentation, “NUMA Memory Policy” — policy scopes, modes, allocation-time behavior, and page migration.
