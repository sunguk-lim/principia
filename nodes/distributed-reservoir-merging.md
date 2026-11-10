---
id: distributed-reservoir-merging
title: Distributed Reservoir Merging
summary: Distributed reservoir merging preserves a global uniform sample by combining compatible local sampling state rather than treating equal-sized samples from unequal partitions as equal populations.
type: concept
tags: [math/probability]
prereqs: [reservoir-sampling]
sources: [https://beam.apache.org/releases/pydoc/current/_modules/apache_beam/transforms/combiners.html]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Distributed Reservoir Merging

## Meaning

A uniform sample from each partition is not automatically a uniform sample of their union. The merge needs state compatible with a proven global rule. One exact design gives every event an independent random priority, retains the largest k priorities locally and repeats that top-k operation when merging.

## Mechanism

Let k be the positive target sample size and N the number of distinct event positions seen across disjoint partitions. Give each event an independent priority from the same continuous distribution. Keep its identity, value and original priority. Each worker retains at most k records; a merge takes the largest k priorities from the union of its inputs. This is a mergeable way to obtain the uniform-prefix objective of [[reservoir-sampling]], not Algorithm R's replacement rule with keys added afterward.

Why can discarded local records never be global winners? A record below local rank k already has at least k larger priorities in its own partition. Adding more candidates cannot move it into the global top k. Therefore merging local winners gives exactly the same result as taking top k from all events. With independent continuous priorities, all event orderings are equally likely, so every size-k subset is equally likely and each event's inclusion probability is k/N when N is at least k.

Apache Beam's SampleCombineFn pairs incoming elements with random numbers and delegates accumulation and merging to a top combiner. Finite pseudorandom priorities introduce ties; an implementation needs a deliberate tie policy and sufficient entropy rather than claiming exact continuous behavior from finite bits.

## One example

Set k=2. Partition A has priorities A1=0.91, A2=0.14, A3=0.77, A4=0.22; it retains A1 and A3. Partition B has B1=0.83 and B2=0.31; it retains both. Merging returns A1 and B1, the same global winners as sorting all six priorities. A2 cannot reappear because two A records already beat it. Equal-size local reservoirs alone do not carry this ordering evidence; assigning new priorities only after local sampling would give the two small-partition survivors too much influence.

## Check your understanding

Can arbitrary Algorithm R reservoirs be merged using this rule? Not without compatible metadata or a different proven count-aware algorithm. Preserve priorities across retries, checkpoint them with identities, and define whether duplicate delivery denotes the same event or a second population member. Test unequal partitions, merge-tree order, tiny partitions, ties and replay. Uniform event sampling still does not guarantee user balance, recency or unbiased model training.

## Prerequisites

- [[reservoir-sampling]]

## Sources

- <https://beam.apache.org/releases/pydoc/current/_modules/apache_beam/transforms/combiners.html>
