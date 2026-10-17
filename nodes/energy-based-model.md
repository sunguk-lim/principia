---
id: energy-based-model
title: Energy-Based Model
summary: An energy-based model assigns a scalar compatibility cost to input-output configurations and predicts by finding a low-energy output without requiring a normalized probability distribution.
type: concept
tags: [ml/deep-learning]
prereqs: [loss-function, softmax]
sources: [https://www.cs.nyu.edu/~yann/research/ebm/]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# Energy-Based Model

## Summary

An energy-based model assigns a scalar compatibility cost to input-output configurations and predicts by finding a low-energy output without requiring a normalized probability distribution.

## Grounded explanation

An energy is a score whose direction is fixed: lower means more compatible. Let $x$ be the observed input, $y$ a candidate output, and $E(x,y)$ the scalar energy assigned by a parameterized model. Prediction chooses an output that minimizes $E(x,y)$ over the allowed candidates. A finite label set permits enumeration; a structured or continuous output may require a separate search procedure. Low energy is a preference under that model, not a measured probability of correctness.

This separates two questions: which output is preferred, and how probabilities are assigned. If there are finitely many candidates, one optional probabilistic interpretation is

$$p(y\mid x)=\frac{\exp(-E(x,y))}{\sum_{y'}\exp(-E(x,y'))}.$$

This is [[softmax]] applied to negative energies. The denominator sums over every allowed candidate. Comparing energies to choose the minimum does not need that sum. Defining probabilities does. For a continuous output, the corresponding integral must be finite before it defines a normalized density; an arbitrary energy function need not satisfy that condition.

Consider three candidate energies $[1,3,4]$. Minimum-energy prediction chooses the first. Adding the same constant, such as $10$, to every energy leaves that choice unchanged. It also leaves the optional normalized distribution unchanged because the common exponential factor cancels. Thus absolute energy is not an intrinsic certainty measure. Adding a new candidate changes the normalization and can change the preferred output if its energy is lower.

Training needs a [[loss-function]] that makes desired outputs preferable to competing outputs. Simply lowering the energies of correct examples can collapse a flexible model to constant low energy everywhere. A training objective must also handle alternatives, for example through relative margins or a normalized likelihood objective. These approaches have different computational costs; avoiding a normalization during prediction does not make all training objectives free of it.

Validate ranking against labeled alternatives, search failures separately from scoring failures, and robustness to candidate-set changes. If probabilities or abstention thresholds are required, evaluate those additional contracts empirically. An energy formulation is not evidence of calibration, reliable unknown detection, or better task quality.

## Prerequisites

- [[loss-function]]
- [[softmax]]

## Sources

- <https://www.cs.nyu.edu/~yann/research/ebm/>
