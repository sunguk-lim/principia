---
id: knowledge-distillation
title: Knowledge Distillation
summary: "Knowledge distillation trains a student on selected outputs or distributions from a teacher, transferring behavior without requiring that teacher during student inference."
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, probability-distribution, loss-function]
sources: [https://arxiv.org/abs/1503.02531, https://arxiv.org/abs/1606.07947, https://arxiv.org/abs/2211.17192]
status: explained
created: 2026-09-10
updated: 2026-11-07
---

# Knowledge Distillation

## Summary

**Knowledge distillation** trains a student using selected teacher behavior as supervision. Output distributions can convey relative alternatives that a one-hot label omits; teacher-generated answers offer a different signal. Lower serving cost is a goal to test, not part of the definition.

## Grounded explanation

A trained teacher [[neural-network]] maps an input to a [[probability-distribution]] over classes. Ordinary supervised training supplies one target class, but a teacher's complete distribution also says which wrong alternatives it considers similar. Distillation makes that distribution a target for a student network and adds a discrepancy between teacher and student outputs to the student's [[loss-function]]. The student may also retain the ordinary label loss; the trade-off is a design choice rather than a guarantee that either objective is always better.

For an image whose label is *cat*, a teacher might assign probabilities `(cat: 0.70, fox: 0.25, dog: 0.05)`. A one-hot label communicates only that *cat* is correct. A student that predicts `(0.70, 0.25, 0.05)` reproduces the teacher's information that fox is more confusable than dog; a student that predicts `(0.70, 0.05, 0.25)` has the same top class but misses that relation. Temperature can soften output scores before normalization, making small non-top probabilities easier for the student to learn; it does not create information absent from the teacher.

Distillation is useful when an ensemble or large model is costly to serve and a smaller student can approximate its behavior. It can also transfer a teacher's errors, calibration defects, biases, and blind spots. Evaluate the student against held-out ground-truth labels as well as teacher agreement, and compare end-to-end latency, memory, throughput, and failure slices with the teacher and an equally sized model trained without distillation.

## Student choice and deployment boundary

The student need not be smaller than the teacher. Architecture, parameter count and starting checkpoint are design choices separate from the transfer objective; same-sized distillation can change behavior without compressing the architecture. A smaller architecture creates a potential capacity saving, while successful training determines what useful behavior survives. Starting from a pretrained checkpoint is common, not a defining requirement. Hold the student architecture and initialization policy fixed when isolating the effect of teacher supervision.

Teacher probabilities are one training signal, not the only one. A retained teacher-generated answer can instead supply ordinary supervised next-token labels without revealing alternative-token probabilities. These variants preserve different information. Teacher agreement, verified task success and broader capability retention must be evaluated separately. Neither a low imitation loss nor a smaller parameter count establishes deployable quality or reduced end-to-end cost.

Distillation changes student weights during training. The deployed student can then generate independently; it does not normally ask the teacher to accept every token. In contrast, [[speculative-decoding]] uses a draft and target-model verification during inference; preserving the target distribution requires its acceptance correction, not merely a second model saying yes. A distilled model can be a draft, so these techniques can be combined, but removing the teacher and retaining target verification are different deployment contracts.

## Prerequisites

- [[neural-network]]
- [[probability-distribution]]
- [[loss-function]]

## Sources

- [Hinton, Vinyals, and Dean, “Distilling the Knowledge in a Neural Network”](https://arxiv.org/abs/1503.02531): motivates compressing ensemble behavior into a deployable model and introduces specialist ensembles.

- [Kim and Rush, Sequence-Level Knowledge Distillation](https://arxiv.org/abs/1606.07947): teacher-generated sequence supervision, including application to the original model.
- [Leviathan et al., Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192): inference-time target verification, in contrast to training transfer.
