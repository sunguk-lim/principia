---
id: training-data-minimization
title: Training-Data Minimization
summary: Training-data minimization limits sensitive or unnecessary records before model fitting, reducing exposure while preserving a measured task-utility and provenance record.
type: concept
tags: [ml/data]
prereqs: [dataset-lineage, training-data-extraction-risk, measurement]
sources: [https://www.nist.gov/privacy-framework, https://arxiv.org/abs/2012.07805]
status: explained
created: 2026-10-01
updated: 2026-10-01
---

# Training-Data Minimization

## Summary

A model cannot be made safe merely by asking it not to reveal data that should never have been in its training corpus. **Training-data minimization** asks which records and fields are necessary for a defined objective, removes or transforms the rest before training, and tests both utility and residual disclosure risk. It reduces exposure; it does not prove that a trained model cannot memorize remaining examples.

## Grounded explanation

Specify the task, retention period, provenance, and permitted uses. Use [[dataset-lineage]] to record which source versions supplied the run. Inventory direct identifiers, quasi-identifiers, secrets, license restrictions, and duplicative records. Exclude unneeded fields and sources; redact or pseudonymize only when the task still works under that transformation. Simple regex redaction can miss contextual identifiers and can remove task signal, so audit a labeled sample and inspect residual sensitive spans.

For example, a support summarizer may need issue category and resolution steps but not full payment-card numbers. Strip the numbers before building training examples; do not depend on later refusal tuning to erase them. If historical training included prohibited content, that is a remediation problem involving a different dataset or measured unlearning/retraining, not a claim that redaction of future inputs rewrote existing weights. [[training-data-extraction-risk]] explains why a clean safety benchmark does not settle exposure.

Use [[measurement]] to compare models trained on original and minimized data under a controlled task, with disclosure-canary tests, false-removal/false-retention rates, downstream utility, and slice performance. Restrict audit artifacts themselves, since logs and examples can recreate the same exposure. Minimize collection and retention across the whole pipeline, including caches and evaluation sets. Data minimization is one defense layer; authorization at inference time and output inspection address different paths.

## Prerequisites

- [[dataset-lineage]]
- [[training-data-extraction-risk]]
- [[measurement]]

## Sources

- [NIST Privacy Framework](https://www.nist.gov/privacy-framework): privacy-risk management and data-processing scope.
- [Carlini et al., “Extracting Training Data from Large Language Models”](https://arxiv.org/abs/2012.07805): evidence that model outputs can expose training examples under some conditions.
