---
id: gang-scheduling
title: Gang Scheduling
summary: Gang scheduling admits a minimum viable group of cooperating tasks only when their joint resource constraints can be satisfied.
type: concept
tags: [os/virtualization]
prereqs: [kubernetes-pod]
sources: [https://github.com/kai-scheduler/KAI-Scheduler/blob/main/docs/batch/README.md, https://github.com/ai-dynamo/grove]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# Gang Scheduling

## Meaning

A distributed application may need several workers before any can make useful progress. Gang scheduling treats its minimum runnable group as an admission unit instead of independently granting resources to whichever task fits first.

## Mechanism

Each [[kubernetes-pod]] still has a concrete placement, but the scheduler evaluates the whole group against currently available resources and constraints. A prescheduling simulation can tentatively place group members in memory, then accept or abandon that plan before reserving real resources. This avoids needless partial reservations or evictions; the simulation is only as accurate as its capacity snapshot and constraints. Admission is logically all-or-nothing, not a claim that processes start in the same clock tick or cannot subsequently fail. Hierarchical gangs express nested minimums: workers may form one model instance, while a service requires both a prefill instance and a decode instance.

## Worked example

There are six free GPUs. Job A requires four workers with two GPUs each; job B requires two one-GPU workers. Independent allocation could give A three workers and consume all six GPUs without a runnable A. Gang admission rejects A for now because 4×2=8 exceeds six, then can admit B using two GPUs. If topology requires all eight of A’s GPUs within one domain, aggregate cluster capacity of eight elsewhere still does not suffice. Elastic jobs may declare a smaller valid minimum, but the scheduler must not invent it. Validate group infeasibility, stale plans, preemption, worker loss, and retry behavior; measure queue wait and useful completion, not only allocated GPUs.

## Check your understanding

Does a successful gang admission prove the service is ready? No: image loading, weight loading, startup dependencies, health checks, and later failures remain separate.

## Prerequisites

- [[kubernetes-pod]]

## Sources

- <https://github.com/kai-scheduler/KAI-Scheduler/blob/main/docs/batch/README.md>
- <https://github.com/ai-dynamo/grove>
