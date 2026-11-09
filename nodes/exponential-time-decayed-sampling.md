---
id: exponential-time-decayed-sampling
title: "Exponential Time-Decayed Sampling"
summary: "Exponential time-decayed sampling assigns recency-dependent weights whose common aging factor preserves old-item relative priorities while new arrivals enter the sample."
type: concept
tags: [math/probability]
prereqs: [weighted-stream-sampling, exponential-function]
sources: [https://arxiv.org/html/1012.0256v2]
status: explained
created: 2026-11-10
updated: 2026-11-10
---

# Exponential Time-Decayed Sampling

## Meaning

A history-uniform sample and a recent-traffic sample target different populations. Exponential time decay gives every historical record a positive but decreasing importance as it ages. This is a chosen sampling policy, not a claim that old data are invalid or that recency eliminates model bias.

## Mechanism

Let T be the current time, $t_i$ record i's timestamp, $b_i>0$ its base importance, and $\lambda>0$ a shared decay rate in inverse time units. Define effective weight $w_i(T)=b_i\exp[-\lambda(T-t_i)]$. The [[exponential-function]] makes each additional time interval multiply every old record's weight by the same factor. Apply a declared [[weighted-stream-sampling]] law to these weights; specify whether it means sequential weight-proportional draws or prescribed final inclusion probabilities.

Factor $w_i(T)=\exp(-\lambda T)\,b_i\exp(\lambda t_i)$. The common positive factor does not change relative weighted priorities among existing items. Thus a key-based sampler can use the time-independent relative factor $b_i\exp(\lambda t_i)$; stable implementations use a time reference or log-domain keys rather than exponentiating large absolute timestamps. The algorithm still considers new arrivals, whose relative factors differ. The weighted-stream source grounds the key-based selection law; this shared-factor identity is an independent algebraic specialization, not a claim of arbitrary time-varying-weight support.

## One example

Choose a half-life of ten time units: $\lambda=\log(2)/10$, where log denotes the natural logarithm already grounded through weighted-stream sampling. Equal-base records aged twenty and ten units have weights 1/4 and 1/2. A one-slot proportional draw selects them with probabilities (1/4)/(3/4)=1/3 and (1/2)/(3/4)=2/3. Ten units later their weights are 1/8 and 1/4, still in a 1:2 ratio. A newly arriving equal-base record has weight 1, so probabilities across the three records become 1/11, 2/11 and 8/11. Aging alone preserved the old ratio; arrival changed the population.

## Check your understanding

Does the same fixed-key trick work for arbitrary future weight changes? No. Individual corrections, nonshared decay rates or hard expiry can change old-item relative ranking, possibly requiring records no longer retained in a bounded reservoir. Check the exact maintenance algorithm and event-time policy for late data. Validate inclusion frequencies, effective sample age, rare-group coverage, recovery and downstream quality against uniform and windowed baselines. Weighting a sample for a recency objective does not automatically supply an unbiased estimator of historical totals.

## Prerequisites

- [[weighted-stream-sampling]]
- [[exponential-function]]

## Sources

- <https://arxiv.org/html/1012.0256v2>
