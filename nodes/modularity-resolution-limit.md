---
id: modularity-resolution-limit
title: Modularity Resolution Limit
summary: The modularity resolution limit is the tendency of modularity optimization to merge small, well-defined communities when their scale is too small relative to the whole graph.
type: concept
tags: [ml/information-retrieval]
prereqs: [graph-rag, graph]
sources:
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC1765466/
  - https://www.nature.com/articles/s41598-019-41695-z
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Modularity Resolution Limit

## Summary

The **modularity resolution limit** is a failure mode of community detection: a partition that maximizes modularity can merge a small, internally coherent group into a larger neighbor because modularity evaluates groups against a null model for the entire graph.

## Grounded explanation

[[Graph-rag]] uses communities to make corpus-wide questions tractable, but a community is an index structure rather than ground truth. A common way to construct such groups is to optimize **modularity**, a score that prefers more edges inside a group than a randomized graph with the same degree pattern would predict. The score is global: its baseline depends on the total number of edges in the graph, not only on the candidate group being examined.

That global baseline produces the resolution limit. Consider a small, tightly linked topic with one connection to a neighboring topic. Locally, separating the two topics is meaningful: each has its own dense internal evidence. In a sufficiently large graph, however, the modularity gain from keeping the small topic separate can be smaller than the gain from merging it with its neighbor. The optimizer then selects the merged partition even when the small topic is unambiguous by direct inspection. Fortunato and Barthélemy showed that the limiting scale changes with overall graph size and how communities connect, so there is no single community size that is always safe.

For a retrieval index, this means a community summary can blur a niche topic into a broad one before the language model sees it. Increasing the nominal quality score does not establish that the partition matches users' query granularity. A resolution parameter can produce finer or coarser partitions, but changing it only chooses a different scale; it does not discover a uniquely correct scale. Leiden improves an important separate property—avoiding poorly connected communities—but it does not remove the need to test whether the chosen resolution serves the task.

Use a concrete evaluation loop. Create queries whose answers depend on a small, known subtopic; build indexes across a sweep of resolution settings; and compare evidence recall, citation support, answer accuracy, latency, and summary cost with a text-retrieval baseline. Preserve cross-community retrieval so a query is not trapped by one partition. If a small topic repeatedly loses its supporting evidence at a particular resolution, use a finer scale or query-time expansion rather than treating the modularity optimum as semantic truth.

## Prerequisites

- [[graph-rag]]
- [[graph]]

## Sources

- [Fortunato and Barthélemy, “Resolution limit in community detection”](https://pmc.ncbi.nlm.nih.gov/articles/PMC1765466/): demonstrates that modularity optimization can fail to resolve modules below a scale determined by the overall network and interconnections.
- [Traag, Waltman, and van Eck, “From Louvain to Leiden: guaranteeing well-connected communities”](https://www.nature.com/articles/s41598-019-41695-z): defines a resolution parameter and distinguishes the resolution-limit issue from connectivity guarantees.
