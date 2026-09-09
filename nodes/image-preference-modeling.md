---
id: image-preference-modeling
title: Image Preference Modeling
summary: Image preference modeling learns or evaluates which of multiple generated images people prefer for a prompt while separating subjective appeal from prompt adherence and other quality dimensions.
type: concept
tags: [ml/evaluation]
prereqs: [text-image-attribute-binding, model-calibration]
sources: [https://arxiv.org/abs/2305.01569]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Image Preference Modeling

## Summary

**Image preference modeling** uses human comparisons such as “image A or image B for this prompt?” to train a ranking score, evaluate generators, rerank samples, or provide a post-training objective.

## Grounded explanation

A comparison record contains prompt $c$, images $x_a,x_b$, and a preference label. A score $s(c,x)$ can be trained so the preferred image receives higher probability, for example

$$P(a\succ b\mid c)=\frac{e^{s(c,x_a)}}{e^{s(c,x_a)}+e^{s(c,x_b)}}.$$

Pick-a-Pic collected prompt-conditioned user comparisons and trained PickScore, a CLIP-based ranking model. Such a score approximates preferences represented in its collection protocol; it is not an objective definition of image quality or a universally “superhuman” judge.

Preference conflates dimensions unless the protocol separates them. A polished image may ignore the prompt, while an accurate image may have weak aesthetics. Measure prompt adherence—including [[text-image-attribute-binding]]—aesthetics, artifacts, diversity, safety, and pairwise choice separately when those distinctions drive decisions.

Uses have different risks. Reranking several samples changes inference cost and selection bias without changing the generator. Adapting the generator on preferred examples or optimizing against a learned score changes its parameters and can reduce diversity, amplify annotator or demographic bias, and exploit score artifacts. Retain an adherence objective and compare against curated supervised targets and reranking baselines.

Use blinded randomized comparisons, explicit ties, multiple raters, agreement statistics, held-out prompt and style slices, and confidence intervals. Audit [[model-calibration]] and ranking consistency under transformations that should not change preference. Recheck with people after optimization because improvement against the learned score does not establish improved human preference.

## Prerequisites

- [[text-image-attribute-binding]]
- [[model-calibration]]

## Sources

- [Kirstain et al., “Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation”](https://arxiv.org/abs/2305.01569): describes prompt-conditioned comparison collection, PickScore training, evaluation against human rankings, and reranking use.
