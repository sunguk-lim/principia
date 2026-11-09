---
id: model-parameter-editing
title: "Model Parameter Editing"
summary: "Model parameter editing deliberately changes a model’s stored tensors to alter behavior, with the intervention distinguished from prompt changes and from any particular training algorithm."
type: concept
tags: [ml/deep-learning]
prereqs: [position-wise-feed-forward-network, residual-connection, measurement, tensor]
sources: [https://arxiv.org/abs/2202.05262, https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Model Parameter Editing

## Meaning

A parameter edit changes stored numerical tensors, so future requests encounter a different model even when the prompt is unchanged. The edit may be derived analytically, learned by another system or proposed through code. “Direct” does not mean every method is gradient-free: model-editing algorithms can use optimization while applying a localized final update.

## Mechanism

Identify the base model, targeted [[tensor]] objects and exact update rule. A [[position-wise-feed-forward-network]] transforms token features; its output projection can be changed so selected features write different directions into a [[residual-connection]]. That is a concrete intervention in a computation, not proof that one tensor stores an isolated fact or that knowledge was inserted. Later nonlinear computation and generation can amplify, suppress or redirect a local change.

ROME is a primary example applying a rank-one weight update to selected feed-forward weights to change factual associations. Its evidence is specific to its models, edits and evaluations; it does not establish that arbitrary weight surgery reliably improves reasoning. Use [[measurement]] of tensor differences, activation changes and actual output behavior rather than inferring the latter from patch size.

## One example

Use an invented two-feature output projection with columns (1, 0) and (0, 1). For hidden activations (2, 3), its output is (2, 3). Add (1, -1) to the second column. The new output is (2, 3)+3(1, -1)=(5, 0). On a different input with hidden activations (2, 0), the same patch changes nothing at this sublayer. The parameters are persistently modified, but the immediate effect depends on the input's feature activation. These numbers describe one linear map, not language-model benchmark results.

## Check your understanding

Does a small patch imply a narrow behavioral effect? No. A shared feature may be used across many tasks, and subsequent tokens see changed context. Compare target efficacy, paraphrase behavior, unrelated-task preservation and output stability against the unchanged model and controls. Keep a restorable baseline and evaluate the loaded edited artifact rather than only inspecting the edit script.

## Prerequisites

- [[position-wise-feed-forward-network]]
- [[residual-connection]]
- [[measurement]]
- [[tensor]]

## Sources

- <https://arxiv.org/abs/2202.05262>
- <https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html>
