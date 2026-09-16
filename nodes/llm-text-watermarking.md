---
id: llm-text-watermarking
title: LLM Text Watermarking
summary: LLM text watermarking biases token sampling toward a secret, context-dependent token subset so a statistical detector can identify the resulting excess without storing a visible marker.
type: concept
tags: [ml/llm/evaluation]
prereqs: [softmax, hypothesis-testing]
sources: [https://arxiv.org/abs/2301.10226]
status: explained
created: 2026-09-17
updated: 2026-09-17
---

# LLM Text Watermarking

## Summary

**LLM text watermarking** embeds a statistical signal during generation. A secret key and the recent token context choose a pseudorandom **green list** of allowed vocabulary items at each step; the generator slightly increases those items' scores before sampling. The text remains ordinary text, but a detector with the key can count an unexpectedly large number of green-list tokens.

## Grounded explanation

At one generation step, an LLM assigns a score, or logit, to every possible next token. [[softmax]] converts those scores into a probability distribution. A soft watermark leaves the vocabulary available but adds a positive bias $\delta$ to each green-list token's logit before softmax. This increases the green tokens' total sampling probability without forcing any particular word.

The green list must change with context. A secret key and a deterministic function of preceding tokens seed a pseudorandom partition of the vocabulary. The generator and detector can therefore reconstruct the same list at each position, while someone without the key cannot reliably predict which edits preserve the signal.

Let $T$ be the number of tested token positions, let $G$ be the number whose observed token belongs to that position's green list, and let $\gamma$ be the fraction of vocabulary placed on each green list. Under an unwatermarked null model that treats membership like a chance event, the expected count is $\gamma T$. A common standardized detector is

$$z=\frac{G-\gamma T}{\sqrt{T\gamma(1-\gamma)}}.$$

The detector uses [[hypothesis-testing]]: choose a threshold before inspection, then flag text only when its statistic falls far enough into the null distribution's upper tail. The threshold controls a modeled false-positive rate; it does not prove authorship, and the null approximation must be validated on representative human and model text.

### Worked example

Suppose $\gamma=0.5$ and $T=100$. The null expects $50$ green tokens, with denominator $\sqrt{100\cdot0.5\cdot0.5}=5$. If the detector observes $G=65$, then

$$z=\frac{65-50}{5}=3.$$

That is a strong excess under the simple null model. It is still evidence from one detector, not proof that a specific model wrote the text.

Increasing $\delta$ generally makes detection easier but can distort token choices or reduce text quality. Short text supplies little evidence. Paraphrasing, translation, token deletion, and adversarial editing can weaken the signal; aggressive robustness measures can raise quality costs or false positives. Evaluation must therefore report text length, model and decoding settings, quality effects, false-positive and false-negative rates, robustness to realistic edits, language/domain shift, key management, and results on data not used to tune the threshold.

## Prerequisites

- [[softmax]]
- [[hypothesis-testing]]

## Sources

- [Kirchenbauer et al., “A Watermark for Large Language Models,” ICML 2023](https://arxiv.org/abs/2301.10226): green-list logit biasing, statistical detection, sensitivity, robustness, and security analysis.
