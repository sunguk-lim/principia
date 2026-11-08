---
id: versioned-inference-configuration
title: "Versioned Inference Configuration"
summary: "Versioned inference configuration preserves the effective model, prompt, parameters, tools and routing rules as a reviewable artifact distinct from mutable preset names."
type: concept
tags: [ml/model-portability]
prereqs: [model-alias-pinning, repository-agent-instructions]
sources: [https://openrouter.ai/docs/guides/features/presets]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Versioned Inference Configuration

## Meaning

An inference configuration specifies how an application invokes a model: model identity, system instructions, generation parameters, tools and provider policy. A reusable preset separates these choices from application code. Reproducibility additionally requires preserving the resolved version, because a stable preset name can point to changed contents.

## Mechanism

Extend [[model-alias-pinning]] beyond the model string. Capture the configuration revision, resolved model/provider, effective prompt and request overrides with each evaluation. A remote preset is a reference to configuration, not necessarily an immutable snapshot. OpenRouter documents named presets, version creation and request-field overrides; verify the actual precedence for the chosen API. Keep credentials and private request content out of public artifacts.

Like [[repository-agent-instructions]], a prompt can encode durable expert guidance. Versioning makes that contribution inspectable, but does not enforce the instructions. To test an agent's own judgment, compare otherwise matched configurations with and without provided design guidance, recording the changed task rather than attributing every difference to the base model. Use [[measurement]] to retain outcomes, latency and cost for each effective version.

## One example

A fictional preset named analyst uses model M, prompt P1 and temperature .2. A later edit keeps the name but changes to prompt P2. Calling both runs analyst does not reproduce the first experiment. If a request overrides temperature to .7, the effective configuration is M/P2/.7, not the stored M/P2/.2. Save that resolved contract and its evaluation revision so rollback can restore the intended behavior rather than merely the old label.

## Check your understanding

Does a configuration hash guarantee deterministic output? No. It identifies supplied content; provider revisions, sampling and execution can still vary. Test override precedence, fallback, denied providers and rollback. Record unresolved server-managed settings explicitly. Reusing a prompt without tracking its version can silently change both production behavior and the amount of expert assistance present in a benchmark.

## Prerequisites

- [[model-alias-pinning]]
- [[repository-agent-instructions]]

## Sources

- <https://openrouter.ai/docs/guides/features/presets>
