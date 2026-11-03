---
id: ademamix
title: AdEMAMix
summary: AdEMAMix combines fast and slow exponential gradient averages with squared-gradient scaling to retain both recent and older directional information.
type: concept
tags: [ml/deep-learning]
prereqs: [adam]
sources: [https://arxiv.org/html/2409.03137v2]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# AdEMAMix

## Meaning

AdEMAMix modifies [[adam]] by retaining two directional time scales rather than one. A fast average responds to recent gradients; a slower average keeps older directions influential. The question is whether that longer history improves training enough to justify extra state and scheduling choices.

## Mechanism

Let g_t be one coordinate's gradient, m_t a fast average, s_t a slow average and v_t a squared-gradient average. With decay coefficients beta_1, beta_3 and beta_2 respectively, update each by its exponential rule: m_t=beta_1*m_previous+(1-beta_1)*g_t, s_t=beta_3*s_previous+(1-beta_3)*g_t and v_t=beta_2*v_previous+(1-beta_2)*g_t^2. The slow decay beta_3 is closer to one.

In the paper's form, the direction combines a bias-corrected fast average with alpha_t times the slow average, then divides by a stabilized bias-corrected square root of v_t. Alpha_t and the slow decay can follow warmup schedules. This is not simply Adam with a larger beta_1: one average cannot simultaneously place high weight on the immediate past and retain the same long tail. State the chosen variant and correction conventions rather than assuming all buffers are corrected identically.

## One example

Isolate the directional mechanism after a history has produced m_previous=1 and s_previous=2. With a new gradient -3, fast decay 0.5 gives m=-1, while slow decay 0.9 gives s=1.5. Before any startup correction, a mixing coefficient alpha=0.5 produces -1+0.5*1.5=-0.25. The recent direction reversed strongly, but older positive history moderated it. A coefficient alpha=1 would instead make the combined direction positive; schedules and history genuinely affect the step.

## Check your understanding

Does retaining old gradients always help after a distribution change? No. Old directions can become stale. Compare tuned schedules, multiple seeds, forgetting behavior, validation quality and time-to-quality. Include the third parameter-sized state array and initialization/warmup effects. The paper's token-efficiency comparisons remain experimental results for its workloads, not promises for every model.

## Prerequisites

- [[adam]]

## Sources

- <https://arxiv.org/html/2409.03137v2>
