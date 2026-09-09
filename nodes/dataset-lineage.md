---
id: dataset-lineage
title: Dataset Lineage
summary: Dataset lineage records which input versions and transformation runs produced an output, enabling reproducibility and targeted diagnosis without guaranteeing data quality.
type: concept
tags: [ml/evaluation]
prereqs: [directed-acyclic-graph]
sources: [https://openlineage.io/docs/spec/object-model/, https://doc.dvc.org/user-guide/project-structure/dvc-files]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Dataset Lineage

## Summary

A lineage record connects an output to the particular inputs and execution that produced it. A table name alone is insufficient if its contents change between runs. Lineage identifies what to investigate; it does not certify that labels or transformations are correct.

## Grounded explanation

Represent immutable dataset versions and transformation executions as vertices in a [[directed-acyclic-graph]]. Input-to-run and run-to-output edges express derivation. Versioned outputs prevent a later retraining cycle from becoming a literal cycle back into its own historical input. A graph of unversioned table names can contain cycles, so acyclicity depends on this representation.

Distinguish the transformation definition from its execution: the same job can run many times with different data and outcomes. Record input versions, code revision, parameters, execution identity, and output versions. OpenLineage distinguishes jobs, runs and datasets; DVC can track data through small versionable metadata files pointing to the associated content. Neither replaces preserving the underlying data and execution environment.

### Original example: same schema, different meaning

Training set A contains 100 labeled examples under annotation policy v1. Set B contains 900 under policy v2. Both have identical `text` and `label` columns, but v1 labels borderline cases positive while v2 labels them negative. Appending them preserves the schema and produces 1,000 rows; it does not preserve label semantics.

Record the source dataset and policy version for each row or stable row group. Now an error audit can separate A from B. If a shared audited slice has 20 examples and the two policies disagree on 6, the 30% disagreement is a concrete lead. It is not proof that all of B is wrong or that annotation differences are the only cause of regression.

Train A-only, B-only and combined variants under controlled settings, evaluating all three on the same independent target set. Inspect disagreement cases before changing labels; source-specific performance could also reflect changed input difficulty, class proportions or evaluation leakage. Retain the chosen policy and adjudication outcomes so a later analyst can reconstruct the decision.

### What lineage can and cannot establish

An exact input version and transformation record support reproduction only while their referenced artifacts remain retrievable. A version identifier without retained content is a broken pointer. Repeated execution may also differ when dependencies or nondeterministic operations are uncontrolled.

Use lineage to locate affected downstream outputs, compare versions and narrow investigations. Validate content separately. A complete lineage graph can faithfully document a consistently wrong labeling policy. Conversely, a quality failure does not by itself identify which missing lineage field caused it.

## Sources

- [OpenLineage object model](https://openlineage.io/docs/spec/object-model/): job, run and dataset distinctions.
- [DVC metadata files](https://doc.dvc.org/user-guide/project-structure/dvc-files): versionable references to tracked data.
- Annotation example and diagnostic procedure are independent applications of these distinctions.
