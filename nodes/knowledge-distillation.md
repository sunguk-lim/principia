---
id: knowledge-distillation
title: Knowledge Distillation
summary: Knowledge distillation trains a smaller student model to match a teacher model's output distribution, transferring information about relative alternatives that one-hot labels omit.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, probability-distribution, loss-function]
sources: [https://arxiv.org/abs/1503.02531]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Knowledge Distillation

## Summary

**Knowledge distillation** trains a student to reproduce a teacher's output distribution, so the student can retain distinctions among alternatives while being cheaper to deploy.

## Grounded explanation

A trained teacher [[neural-network]] maps an input to a [[probability-distribution]] over classes. Ordinary supervised training supplies one target class, but a teacher's complete distribution also says which wrong alternatives it considers similar. Distillation makes that distribution a target for a student network and adds a discrepancy between teacher and student outputs to the student's [[loss-function]]. The student may also retain the ordinary label loss; the trade-off is a design choice rather than a guarantee that either objective is always better.

For an image whose label is *cat*, a teacher might assign probabilities `(cat: 0.70, fox: 0.25, dog: 0.05)`. A one-hot label communicates only that *cat* is correct. A student that predicts `(0.70, 0.25, 0.05)` reproduces the teacher's information that fox is more confusable than dog; a student that predicts `(0.70, 0.05, 0.25)` has the same top class but misses that relation. Temperature can soften output scores before normalization, making small non-top probabilities easier for the student to learn; it does not create information absent from the teacher.

Distillation is useful when an ensemble or large model is costly to serve and a smaller student can approximate its behavior. It can also transfer a teacher's errors, calibration defects, biases, and blind spots. Evaluate the student against held-out ground-truth labels as well as teacher agreement, and compare end-to-end latency, memory, throughput, and failure slices with the teacher and an equally sized model trained without distillation.

## Prerequisites

- [[neural-network]]
- [[probability-distribution]]
- [[loss-function]]

## Sources

- [Hinton, Vinyals, and Dean, “Distilling the Knowledge in a Neural Network”](https://arxiv.org/abs/1503.02531): motivates compressing ensemble behavior into a deployable model and introduces specialist ensembles.
