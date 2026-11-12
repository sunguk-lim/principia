---
id: three-way-merge
title: "Three-Way Merge"
summary: "A three-way merge compares a common base with two descendants so unchanged inherited state can be distinguished from competing edits."
type: concept
tags: [software/version-control]
prereqs: [set, measurement]
sources: [https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging]
status: explained
created: 2026-11-13
updated: 2026-11-13
---

# Three-Way Merge

## Meaning

A three-way merge combines two descendants using their common ancestor as evidence of what each side changed. Comparing only the two final snapshots cannot distinguish a deliberate edit from a value one side merely inherited.

## Mechanism

For each stable key, compare base B, current main M and proposed branch P. The [[set]] of keys changed from B to M is one change set; B to P is the other. If only one side changed a key, retain that change. If both produced the same value, it may be accepted once. If both changed it differently, invoke an explicit conflict policy. Creation, deletion and rename require their own identity rules.

Define equality through appropriate [[measurement]] and schema rules. Whole-record comparison is conservative: two different fields changed on one record can still be rejected. Field-level comparison can combine them, but must validate semantic constraints across fields and records. A text merge with no conflict markers does not prove that the resulting program or database is correct.

## One example

An invented base record is {store: Redis, owner: none}. M changes store to Postgres; P changes owner to platform. A field-level three-way merge yields {store: Postgres, owner: platform}, because each unchanged field on one side is inherited rather than an instruction to undo the other edit. A record-level policy can instead flag a conflict for human review. If both sides change store to different values, neither rule should silently infer the intended winner.

## Boundaries and check

A fast-forward is possible when one tip is an ancestor of the other; divergent history requires combination but does not imply a conflict. Test concurrent creation, delete-versus-update, same-value edits and cross-record invariants. Preserve the base and conflict evidence. A three-way merge is a version-combination operation, not an authentication mechanism, transaction protocol or automatic proof of semantic compatibility.

## Prerequisites

- [[set]]
- [[measurement]]

## Sources

- <https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging>
