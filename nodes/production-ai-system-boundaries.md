---
id: production-ai-system-boundaries
title: Production AI System Boundaries
summary: Production AI behavior emerges from connected data, model, serving, context, control, and evaluation boundaries; a model-only benchmark cannot validate the whole system.
type: concept
tags: [ml/ai-systems]
prereqs: [prefill-vs-decode, agent-execution-harness, progressive-model-rollout]
sources: [https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning, https://www.nist.gov/itl/ai-risk-management-framework]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Production AI System Boundaries

## Summary

Two products using the same base model can have different latency, cost, accuracy, and safety because the **system around the model** changes what it sees, what it may do, and how outcomes are checked. A layer inventory is useful only when it identifies interfaces and failure evidence, not when it implies that one universal stack has exactly eight components.

## Grounded explanation

Trace one request across boundaries: input and data authorization; tokenization and model inference; serving and scheduling; retrieval or context assembly; the [[agent-execution-harness]] that validates actions; and outcome evaluation. [[prefill-vs-decode]] illustrates why a model-level throughput number can hide distinct service bottlenecks. The harness can prevent an unauthorized write even when the model proposes one, while a retrieval error can make a fluent answer wrong despite unchanged weights.

Each boundary needs an observable contract: inputs, ownership, permitted effects, version, latency, and failure behavior. A local model-quality score does not establish end-to-end task completion; a fast token stream does not establish a correct or authorized action. Google Cloud's MLOps guidance likewise treats model code as a small part of an operated ML system, with data verification, automation, monitoring, and serving outside the model. NIST's AI RMF frames risk management over design, development, use, and evaluation rather than a checkpoint alone.

## Validation

Build an end-to-end task set with ground-truth state changes and policy constraints. Hold the base model fixed while varying one boundary—retriever, batching policy, tool gate, or rollout cohort. Measure user-visible correctness, unauthorized effects, TTFT, TPOT, throughput, cost, and recovery. Use a [[progressive-model-rollout]] to distinguish offline confidence from production outcomes before broad exposure. Attribute failures to evidence at the relevant boundary instead of calling every miss a model failure.

## Prerequisites

- [[prefill-vs-decode]]
- [[agent-execution-harness]]
- [[progressive-model-rollout]]

## Sources

- [Google Cloud, MLOps continuous delivery and automation](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning).
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).
