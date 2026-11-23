---
id: direct-preference-optimization
title: "Direct Preference Optimization"
summary: "Direct Preference Optimization fits preferred-versus-dispreferred response pairs using reference-relative policy log probabilities instead of a separately trained online reward-optimization loop."
type: concept
tags: [ml/llm/training]
prereqs: [pairwise-preference-model, causal-language-model-training, kl-divergence]
sources: [https://arxiv.org/html/2305.18290v3]
status: explained
created: 2026-11-24
updated: 2026-11-24
---

# Direct Preference Optimization

## Meaning

Direct Preference Optimization (DPO) adapts a language model using an offline dataset of prompt/response comparisons and a fixed reference policy. It is a specific loss, not a synonym for every method that uses feedback, and its theoretical reparameterization does not guarantee perfect human alignment in a finite model.

## Mechanism

For prompt x, let y_w be the preferred response and y_l the dispreferred response. Let pi_theta(y|x) be the trainable policy's full-response probability and pi_ref(y|x) the fixed reference's probability. Both must be positive on the compared responses. Define beta>0 as the objective scale, sigma(z)=1/(1+exp(-z)), and the reference-relative margin

$$m=\beta\left[\ln\frac{\pi_\theta(y_w\mid x)}{\pi_{ref}(y_w\mid x)}-\ln\frac{\pi_\theta(y_l\mid x)}{\pi_{ref}(y_l\mid x)}\right].$$

The pair loss is -ln sigma(m), averaged over the declared dataset. [[causal-language-model-training]] supplies sequence log probabilities as sums over response-token log probabilities given the prompt and preceding tokens. Mask prompt/padding tokens consistently; replacing those sums with arbitrary length averages changes the objective.

Why can a preference loss use policy probabilities? For a reward objective penalized by beta times [[kl-divergence]] to a reference, the ideal optimum has policy proportional to the reference times exp(reward/beta). Rearranging gives reward=beta times the log policy/reference ratio plus a prompt-specific constant. In a [[pairwise-preference-model]], the constant cancels between two responses. Substituting the remaining ratios produces the displayed loss. The derivation assumes the stated reward/preference model and compatible support, not arbitrary human choices.

## One example

For a toy pair, reference probabilities are 0.2 for the winner and 0.3 for the loser; trainable probabilities are 0.3 and 0.2. With beta=0.5, the margin is 0.5×ln[(0.3/0.2)/(0.2/0.3)]=0.5×ln(2.25), about 0.4055. The implied preference probability is 0.6 and the loss about 0.5108. At identical trainable/reference policies, the margin is zero and the pair loss ln(2), about 0.6931. These are pair calculations, not a guaranteed optimization trajectory.

## Validation and check

Pin the reference, tokenizer, rendering, truncation, response masks and dataset provenance. Test preference direction and a tiny hand-calculated pair before training. Compare held-out human/task preference, factual quality, safety, diversity and length behavior—not only pairwise training accuracy. Noisy labels, narrow coverage and distribution shift remain problems; a fixed offline dataset need not cover the model's new deployment outputs.

DPO avoids a separate explicit reward model and fresh on-policy sampling in the original training formulation. This is an algorithmic difference, not a universal stability, compute or quality advantage over every RLHF implementation.

**Check:** Does raising the winner's absolute probability alone fully describe DPO? No. The loss depends on the winner/loser log-ratio difference relative to the reference.

## Prerequisites

- [[pairwise-preference-model]]
- [[causal-language-model-training]]
- [[kl-divergence]]

## Sources

- <https://arxiv.org/html/2305.18290v3>
