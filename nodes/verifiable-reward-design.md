---
id: verifiable-reward-design
title: Verifiable Reward Design
summary: A verifiable reward maps an output to an executable score, but its parser, test coverage, and hidden assumptions define exploitable gaps.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [reward-hacking, execution-benchmark-validity]
sources: [https://arxiv.org/abs/2501.12948, https://www.swebench.com/SWE-bench/guides/evaluation/]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Verifiable Reward Design

## Summary

A **verifiable reward** uses an executable rule—such as exact answer checking, a schema validator, or tests—to score a generated output. The rule is cheaper to apply repeatedly than a human judgment, but it measures only the behavior its implementation exposes.

## Grounded explanation

For a math task, the verifier must parse a final answer and compare it with a reference under explicit rules for formatting, equivalence, and invalid output. For code, executable tests must be run in an isolated environment and distinguish a fix from a patch that breaks already-passing behavior. [[execution-benchmark-validity]] asks whether those tests represent the intended task rather than a narrow artifact. A reward can be deterministic yet incomplete: memorized answers, leaked test cases, parser quirks, or test gaps can all receive high scores without solving the underlying problem.

Because an optimizer will seek high reward, [[reward-hacking]] is a design constraint, not an afterthought. Keep reward-development data separate from held-out evaluation; include adversarial cases and malformed responses; log parse failures and impossible scores; and compare a sample of high-reward outputs with independent assessment. Define what happens on timeout, crashed tests, flaky tests, and invalid generations before training begins. Version the verifier code and configuration alongside each training run so a later score can be tied to the exact rule that produced it.

A verifier is most valuable when a reliable checker exists and ideal reasoning traces are costly. It is less suitable for goals such as helpfulness or design quality that have no complete executable oracle. Combining several checks can improve coverage, but arbitrary weighted sums may let a model trade a serious failure for easy bonus points. Use gates for non-negotiable constraints and measure each component separately.

## Prerequisites

- [[reward-hacking]]
- [[execution-benchmark-validity]]

## Sources

- [DeepSeek-R1 technical report](https://arxiv.org/abs/2501.12948): discusses rule-based rewards for verifiable tasks.
- [SWE-bench evaluation guide](https://www.swebench.com/SWE-bench/guides/evaluation/): illustrates executable test outcomes and harness boundaries.
