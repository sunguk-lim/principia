---
id: token-and-duration-transducer
title: Token-and-Duration Transducer
summary: A Token-and-Duration Transducer extends an RNN Transducer with a duration prediction that lets one decoding transition advance across multiple acoustic frames, reducing sequential blank processing.
type: concept
tags: [ml/speech]
prereqs: [rnnt, probability-distribution]
sources: [https://arxiv.org/abs/2304.06795]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Token-and-Duration Transducer

## Summary

A **Token-and-Duration Transducer (TDT)** is an [[rnnt]] whose decoder predicts both a transcript token (or blank) and a duration, allowing one transition to consume several acoustic frames instead of exactly one.

## Grounded explanation

An ordinary [[rnnt]] state is `(t, u)`: frame `t` and emitted-prefix length `u`. A blank transition always moves one frame, from `(t, u)` to `(t + 1, u)`. Thus a run of silence can require many serial blank predictions even though no transcript token changes.

A TDT retains the transducer structure but adds a duration head. Alongside the token [[probability-distribution]], it produces a distribution over permitted frame advances. A transition now chooses a token or blank and a duration `d`. A blank advances from `(t, u)` to `(t + d, u)`; a nonblank token advances to `(t + d, u + 1)`. A nonblank may use duration zero when another token must align to the same frame, while a blank must advance by at least one frame so decoding cannot stall.

The duration prediction changes the number of decoding steps, not the streaming contract. When the model can confidently assign a longer duration to a quiet or stable acoustic span, it skips intermediate blank states. When timing is uncertain, it can choose a short duration. Training extends the transducer lattice with edges for the allowed durations, so the model still marginalizes over valid token/frame alignments rather than relying on one supplied alignment.

The token and duration heads are separate because a single joint output would need one class for every token-duration pair. Separate distributions keep the token vocabulary and duration set independently sized while the transition rule combines their choices. The claimed benefit should be evaluated as a trade-off: fewer sequential decoder transitions and lower latency are useful only if transcript quality remains within the application’s tolerance.

## Prerequisites

- [[rnnt]]
- [[probability-distribution]]

## Sources

- Ghazaleh et al., “Token-and-Duration Transducer: A Transducer for Fast Speech Recognition” (2023), [arXiv:2304.06795](https://arxiv.org/abs/2304.06795): duration-augmented transducer formulation and multi-frame transitions.
