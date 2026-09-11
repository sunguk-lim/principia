---
id: cyclical-feature-encoding
title: Cyclical Feature Encoding
summary: Cyclical feature encoding maps a repeating scalar such as hour-of-day to sine and cosine coordinates so values adjacent across the wraparound remain close.
type: concept
tags: [ml/feature-engineering]
prereqs: [arithmetic]
sources: [https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Cyclical Feature Encoding

## Summary

A repeating value such as an hour, weekday, or month has an endpoint only in
its storage format: the last value is adjacent to the first. **Cyclical feature
encoding** represents its phase with two coordinates, sine and cosine, so that
this wraparound is preserved.

## Grounded explanation

Let `x` be a value in a cycle of period `P`, with `0 <= x < P`. Convert it to
an angle and retain both coordinates:

$$\theta = 2\pi \, x / P, \qquad (s, c) = (\sin\theta, \cos\theta).$$

The two coordinates place every value on the unit circle. For an hour feature,
`P = 24`: hour 23 and hour 0 lie next to one another on that circle, whereas
the raw integers make them appear far apart. A model can then learn smoothly
from the pair instead of being asked to infer that the numeric discontinuity is
an artifact of representation.

Keep both coordinates. Sine alone has the same value at different phases, and
cosine alone does too; their ordered pair identifies a phase around the cycle.
The period must come from the meaning of the feature rather than from observed
minimum and maximum values: a weekly feature has period seven even if a sample
omits a day. This encoding is appropriate only when the endpoints are genuinely
adjacent; ordinal categories and nonrepeating counts should retain a different
representation.

The calculation is a fixed numeric transformation built from [[arithmetic]]. It
does not create information or establish a causal relationship; it makes the
known circular geometry available to a downstream model.

## Prerequisites

- [[arithmetic]]

## Sources

- [scikit-learn: Time-related feature engineering](https://scikit-learn.org/stable/auto_examples/applications/plot_cyclical_feature_engineering.html): official example of sine/cosine encodings for cyclical time features.
