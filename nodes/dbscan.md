---
id: dbscan
title: "DBSCAN"
summary: "DBSCAN forms clusters from connected dense neighborhoods, attaches nearby border points and labels unsupported observations as noise."
type: concept
tags: [ml/training]
prereqs: [arithmetic, graph]
sources: ["https://scikit-learn.org/stable/modules/clustering.html#dbscan", "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html"]
status: explained
created: 2026-11-22
updated: 2026-11-22
---

# DBSCAN

## Meaning

DBSCAN groups density-connected observations rather than choosing a fixed number of centroids. Its output can include noise. The distance metric, neighborhood radius eps and minimum neighborhood population define what counts as locally dense.

## Mechanism

For each observation, find all points within eps under the chosen distance. In scikit-learn, min_samples counts the point itself. A point meeting that count is core. Connect core points within eps; connected core regions define clusters, a [[graph]] interpretation. A noncore point within eps of a core point is a border point; remaining points are noise. A border point does not by itself join two separate core components. [[arithmetic]] supplies distance/count comparisons, not a claim that one radius suits every dataset.

This neighborhood rule can capture curved shapes without requiring each cluster to be compact around one mean. But a single global radius can merge dense groups through a bridge or discard a lower-density group. Feature scales and the metric determine neighborhoods, so preprocessing is part of the clustering contract.

## One example

On the line, take [0,.1,.2,2,2.1,2.2,8], eps=.15 and min_samples=3 including self. Points .1 and 2.1 each have three neighbors and are core. Their respective nearby endpoints are border points. The result has two clusters and a noise point at 8. Choosing eps=.05 would make all points noise for this population threshold. This invented example illustrates why cluster count is an output but meaningful parameters are still required.

## Boundaries and check

A border point near two core components can receive an order-dependent assignment; numeric cluster labels are arbitrary. Test core membership and partitions, not label numbers alone. Exact neighborhood construction can have quadratic memory or work in unfavorable settings, depending on implementation and data. Compare geometry, density variation, noise stability and resource use. Validate rare structures and parameter sensitivity rather than equating “no need to choose K” with “no tuning.”

**Check:** If two core clusters share a nearby noncore border point, must they merge? No. Border membership does not create a connecting core path.

## Prerequisites

- [[arithmetic]]
- [[graph]]

## Sources

- <https://scikit-learn.org/stable/modules/clustering.html#dbscan>
- <https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html>
