---
id: regularization
title: Regularization
summary: Regularization deliberately biases model fitting toward simpler or more stable solutions so performance on unseen data improves even when training error rises.
type: concept
tags: [ml/deep-learning]
prereqs: [loss-function, gradient-descent]
sources: [https://www.deeplearningbook.org/contents/regularization.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Regularization

## Summary

**Regularization** changes a learning problem so that, among solutions fitting the observed examples, training prefers one expected to behave more reliably on unseen examples. It deliberately trades some fit to the training data for a useful bias such as smaller parameter values, insensitivity to perturbations, or agreement across augmented examples.

## Grounded explanation

Let $w$ denote all trainable parameters, let $L_{\mathrm{data}}(w)$ be the ordinary [[loss-function]] measured on the training examples, let $R(w)$ measure an undesirable property of a solution, and let $\lambda\ge 0$ control how strongly that property is discouraged. Penalty-based regularization minimizes

$$
L_{\mathrm{total}}(w)=L_{\mathrm{data}}(w)+\lambda R(w).
$$

The first term asks the model to explain the observations. The second distinguishes between solutions with similar training loss. For the common squared-parameter penalty, $R(w)=\sum_j w_j^2$, two equally accurate solutions no longer tie: the one using smaller parameter magnitudes has lower total loss. The coefficient $\lambda$ exposes the tradeoff. At $\lambda=0$ there is no penalty; increasing $\lambda$ accepts more training error to obtain the preferred structure.

This works through the update itself. [[gradient-descent]] follows the gradient of the total objective,

$$
w \leftarrow w-\eta\left(\nabla L_{\mathrm{data}}(w)+\lambda\nabla R(w)\right),
$$

where $\eta>0$ is the step size. When $R(w)=\sum_j w_j^2$, its gradient is $2w$, so every step combines evidence from the data with a pull toward zero. Regularization is therefore not a score applied after training; it changes which fitted solution the training procedure reaches.

### Worked example

Suppose a one-parameter model has data loss $L_{\mathrm{data}}(w)=(w-3)^2$. Without regularization, $w=3$ gives loss $0$. Add $R(w)=w^2$ with $\lambda=0.5$:

$$
L_{\mathrm{total}}(w)=(w-3)^2+0.5w^2.
$$

Differentiating gives $2(w-3)+w=3w-6$. Setting this to zero yields $w=2$. The regularized solution has data loss $(2-3)^2=1$ rather than $0$, but its penalty is $0.5(2^2)=2$, so its total is $3$. At the unregularized solution $w=3$, the total is $0+0.5(9)=4.5$. Regularization intentionally selects $w=2$: a worse exact fit, but a smaller and less extreme parameter.

Penalty terms are only one implementation. Stopping optimization before it fully adapts to training peculiarities, randomly perturbing training inputs or activations, and expanding the training set with label-preserving transformations all impose biases too. The unifying idea is the tradeoff, not a particular formula: constrain effective flexibility so success is judged by behavior beyond the examples already seen.

## Prerequisites

- [[loss-function]]
- [[gradient-descent]]

## Sources

- Goodfellow, Bengio, and Courville, *Deep Learning*, Chapter 7, “Regularization for Deep Learning” — regularization as modifying a learning algorithm to reduce generalization error, including parameter penalties and other mechanisms.
