---
id: greedy-decoding-reproducibility
title: Greedy Decoding Reproducibility
summary: Greedy decoding removes random token sampling but does not guarantee identical text when model execution, numerical kernels, tie handling, or request conditions vary.
type: concept
tags: [ml/llm/inference]
prereqs: [decoder-only-transformer, numeric-precision-formats, measurement, probability-chain-rule]
sources: [https://docs.pytorch.org/docs/2.14/notes/randomness.html, https://huggingface.co/docs/transformers/generation_strategies]
status: explained
created: 2026-10-15
updated: 2026-10-22
---

# Greedy Decoding Reproducibility

## Summary

A temperature setting of zero is commonly implemented as greedy selection: choose the highest-scoring token rather than sample from a probability distribution. This removes one source of randomness. It does **not** by itself promise byte-identical output across runs or systems.

## Grounded explanation

A [[decoder-only-transformer]] computes a score for each candidate next token. Greedy decoding chooses the largest score, subject to a specified tie rule. If two candidates are close, a small numerical change can switch the winner; that different token changes the entire subsequent context. [[numeric-precision-formats]] and reduction order affect floating-point results, while different kernels, devices, model revisions, tokenizers, prompt templates, batching, and server-side processing can change the scores or inputs. A seed matters for stochastic sampling but cannot repair a changed model or nondeterministic kernel.

PyTorch's reproducibility documentation explicitly limits guarantees across releases, platforms, and CPU/GPU execution even with identical seeds. It distinguishes controlling random-number generators from selecting deterministic algorithms, some of which are slower or unavailable. This is a framework-level constraint, not proof that any particular hosted model varies at temperature zero.

For a reproducibility claim, pin model weights and revision, tokenizer, prompt bytes, decoding parameters, runtime and kernel versions, device type, precision, batch shape, and concurrency policy. Record returned model and service metadata where available. Run repeated identical requests and compare token IDs, not just visible strings. Use [[measurement]] to report mismatch frequency and the first diverging position; inspect the score gap at that position if logits are available. Test both a fixed single-request configuration and the intended production scheduler. If exact replay is a requirement, verify a supported deterministic execution path and regression-test it after upgrades; otherwise specify a tolerance and evaluate semantic stability separately.

## Local choice, sequence probability and correctness

By the [[probability-chain-rule]], complete-sequence probability multiplies the probabilities conditioned on its prefixes. Greedy choice optimizes the next token's score, not a complete sequence's probability or the task's true answer. Consider exactly two generation steps. First-token probabilities are P(A)=0.6 and P(B)=0.4. After A, two final tokens x and y each have probability 0.5; after B, x has probability 0.9 and y 0.1. With a tie rule choosing x, greedy returns Ax with probability 0.6×0.5=0.30. The complete sequence Bx has probability 0.4×0.9=0.36, which is larger. The other complete sequences Ay and By have probabilities 0.30 and 0.04; all four sum to one. A search procedure can explore alternatives, but highest model probability still does not establish a correct or authorized action.

Repeatability is a separate axis. A router can return the same wrong tool on every replay. Compare token and action agreement with independently labeled task success. Batch-shape sensitivity is also a hypothesis to isolate, not a universal property of every server: keep the fully rendered prompt, retrieval ordering, model and tokenizer fixed, then vary batch shape and concurrency while checking actual deterministic-kernel guarantees. Dynamic timestamps and changing tool results are input changes, not numerical nondeterminism. Store bounded versioned evidence references for replay rather than indiscriminately logging private payloads.

## Prerequisites

- [[probability-chain-rule]]

- [[decoder-only-transformer]]
- [[numeric-precision-formats]]
- [[measurement]]

## Sources

- [PyTorch reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html): seeds, nondeterministic algorithms, platform/version limits, and performance trade-offs.

- <https://huggingface.co/docs/transformers/generation_strategies>
