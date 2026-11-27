---
id: dataset-versioning
title: "Dataset Versioning"
summary: "Dataset versioning binds a small revisioned manifest to retrievable immutable data content so experiments can select and restore the intended dataset."
type: concept
tags: [ml/systems]
prereqs: [dataset-lineage, hash-map]
sources: [https://doc.dvc.org/start, https://doc.dvc.org/user-guide/project-structure/dvc-files]
status: explained
created: 2026-11-28
updated: 2026-11-28
---

# Dataset Versioning

## Meaning

Dataset versioning gives a dataset revision a recoverable identity. A filename such as `training.csv` is not a version if its bytes can change without a record. The goal is to select the exact intended content alongside code, rather than merely recognize that some file with the same name once existed.

## Mechanism

Separate small revisioned metadata from large artifact content. A manifest names the path and content identity; an artifact store retains the corresponding bytes. A content-addressed store uses a [[hash-map]]-like key-to-content lookup in which the key is derived from the content. Git can version the small manifest while a separate store holds large data. DVC's `.dvc` files provide a concrete implementation with hashes, paths and optional size and remote metadata.

The workflow has two distinct durability operations: save the manifest revision and make the referenced data available to its intended readers. A pushed code commit does not establish that data reached the artifact remote. Restoring an old manifest also does not by itself replace a workspace dataset; the data-management tool must materialize that revision from retained content.

[[dataset-lineage]] records which inputs and transformations produced an output. Versioning supplies stable recoverable inputs to that lineage. Neither mechanism certifies labels, prevents leakage or recreates a deleted external service. Keep code, parameters, split definitions, environment and annotation policy where the experiment's reproduction contract requires them.

## One example

An invented revision A points `training.csv` to content key H1 with 100 records. Revision B points the same path to H2 with 140 records. Checking out A's code but leaving H2 in the workspace mixes revisions. Restore the H1 artifact, verify its identity and split definition, and record the experiment's selected revision. If H1 was removed from every cache and remote, A's manifest is still present but its dataset is no longer recoverable.

## Validation and boundaries

Test restoration in a clean workspace without relying on the original machine's cache. Verify retrieved content, row/split counts and expected transformation outputs; simulate a missing artifact and denied remote access. Distinguish integrity checks from security guarantees: a checksum used for content lookup is not automatically a signature proving trusted authorship.

Artifact retention has storage, access and deletion obligations. Versioning private data does not authorize distributing it. When an artifact must be deleted, record the loss of reproducibility rather than claiming that the remaining metadata can regenerate it. A versioned dataset is a necessary input to many repeatable experiments, not a guarantee of deterministic training or scientifically correct results.

## Prerequisites

- [[dataset-lineage]]
- [[hash-map]]

## Sources

- <https://doc.dvc.org/start>
- <https://doc.dvc.org/user-guide/project-structure/dvc-files>
