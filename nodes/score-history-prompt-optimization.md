---
id: score-history-prompt-optimization
title: "Score-History Prompt Optimization"
summary: "Score-history prompt optimization conditions a language-model proposal on previous candidate configurations and measured outcomes rather than using a derivative of the task score."
type: concept
tags: [ml/agents]
prereqs: [persistent-agent-improvement, adaptive-validation-overfitting]
sources: [https://arxiv.org/abs/2309.03409]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Score-History Prompt Optimization

## Meaning

A language model can act as a black-box proposal mechanism: show it a task objective, previous candidate instructions and their measured scores, then ask for another candidate. The score is obtained by running the real task, not by asking the proposer to guess how well its own rewrite works. OPRO is a primary example of this approach.

## Mechanism

Retain an evaluation record for each candidate: exact configuration, task set, metric, decoding settings and budget. Place a bounded selection of candidate–score pairs in the optimizer's context. Generate a proposal, evaluate it under the same contract, append the outcome, and repeat until the search budget ends. This is one search strategy inside [[persistent-agent-improvement]]; improvement still requires independent promotion evidence.

The history may help the model infer useful regularities, but it is not a mathematical gradient, an acquisition function with calibrated uncertainty, or a convergence guarantee. A stronger proposer can still exploit a faulty metric. Distinguish a scalar history from diagnostic traces: the former says which evaluated candidates scored well, whereas the latter may explain a failure. Use [[adaptive-validation-overfitting]] to keep a final estimate outside this repeated feedback loop.

## One example

For an invented extraction task, candidate A says “return the amount” and scores 6/10 on a tuning set. B specifies the currency and scores 8/10. The optimizer proposes C, which adds an explicit missing-value rule; running C yields 9/10. That is evidence for C on these ten cases, not proof that the added rule caused the gain or that C will generalize. Compare A, B and C on untouched documents and include a matched-budget random or manually designed search. Record rejected candidates too; otherwise the apparent nine successes omit the cost of finding C.

## Check your understanding

Does sorting candidates by score establish a reliable improvement direction? No. Noise, wording interactions, changing task difficulty and context selection can all mislead the proposal. Repeat uncertain comparisons, preserve task-level outcomes, and report held-out quality versus total evaluation cost. Keep the executable configuration associated with each score; a paraphrased prompt can be a different candidate.

## Prerequisites

- [[persistent-agent-improvement]]
- [[adaptive-validation-overfitting]]

## Sources

- <https://arxiv.org/abs/2309.03409>
