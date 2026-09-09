---
id: score-based-generative-model
title: Score-Based Generative Model
summary: A score-based generative model estimates time-dependent log-density gradients and uses reverse-time stochastic or probability-flow dynamics to transform a tractable prior into data.
type: concept
tags: [ml/deep-learning]
prereqs: [score-function, stochastic-differential-equation, differential-equation, differential, denoising-diffusion-probabilistic-model, neural-network]
sources: [https://arxiv.org/abs/2011.13456]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Score-Based Generative Model

## Summary

A **score-based generative model** learns the time-dependent [[score-function]] of progressively perturbed data, then solves reverse dynamics from a simple prior distribution to the data distribution.

## Grounded explanation

Consider a forward [[stochastic-differential-equation]]

$$dX_t=f(X_t,t)\,dt+g(t)\,dW_t$$

that gradually changes data into a tractable terminal distribution. Under regularity conditions, its reverse-time SDE depends on the score $\nabla_x\log p_t(x)$. A [[neural-network]] estimates that score from noisy training samples.

Generation begins with a random draw from the terminal prior, not a fixed data-space point. A numerical solver then follows either the reverse-time SDE or a corresponding deterministic probability-flow [[differential-equation]]. These are structured, time-dependent dynamics; direct gradient ascent on one static density is a different operation and generally seeks local modes.

Stochastic sampling is not the only valid route to diverse samples. A deterministic probability-flow solver can preserve the same marginal distributions when initialized with independent prior draws and integrated correctly. Reusing one initial draw naturally gives reproducible output; diversity must be assessed across prior samples, not repeated execution with an identical seed alone.

This framework includes connections to the discrete [[denoising-diffusion-probabilistic-model]], but discretization, prediction target, solver, and noise schedule remain design choices. More injected noise is not automatically better: stochasticity, corrector steps, and solver tolerance trade compute, numerical bias, fidelity, and diversity.

Validate analytic toy distributions, endpoint moments, mode coverage, sample fidelity and diversity, solver convergence at matched function evaluations, and sensitivity to initial draws. Separate score-estimation error from solver error with an analytic-score baseline when possible.

## Prerequisites

- [[score-function]]
- [[stochastic-differential-equation]]
- [[differential-equation]]
- [[differential]]
- [[denoising-diffusion-probabilistic-model]]
- [[neural-network]]

## Sources

- [Song et al., “Score-Based Generative Modeling through Stochastic Differential Equations”](https://arxiv.org/abs/2011.13456): derives reverse-time SDE and equivalent probability-flow dynamics driven by time-dependent scores.
