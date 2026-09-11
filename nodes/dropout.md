---
id: dropout
title: Dropout
summary: Dropout is a training-time regularizer that independently masks selected activations and scales the survivors so their expected value matches inference-time activations.
type: concept
tags: [ml/deep-learning]
prereqs: [bernoulli-distribution, neural-network, regularization, tensor]
sources: [https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# Dropout

## Summary

**Dropout** is a [[regularization]] method for a [[neural-network]] that, during training, independently replaces some activation values with zero and scales every retained value to preserve the expected activation scale used at inference.

## Grounded explanation

A layer can otherwise make later layers depend too closely on particular paths through a network. During each training forward pass, dropout makes the path variable: for every element of an activation [[tensor]], it either retains the value with probability $q=1-p$ or replaces it with zero, where $p$ is the configured dropout probability sampled by [[bernoulli-distribution]]. The random choice is fresh on each forward pass.

PyTorch uses *inverted dropout*. If an activation has value $x$ and survives, the layer emits $x/q$; if it is dropped, it emits $0$. The expected training-time output is therefore $q(x/q)+(1-q)0=x$. At inference dropout is disabled, so the unmodified value $x$ has the same expected scale. This is why implementations scale during training rather than applying a compensating factor at inference.

### Worked instance

Let $x=6$ and choose $p=0.25$, hence $q=0.75$. A training pass emits either $0$ with probability $0.25$ or $6/0.75=8$ with probability $0.75$. Its expected output is $0.25(0)+0.75(8)=6$. In inference mode it always emits $6$. The expected scale agrees, although individual training passes differ.

Dropout is not a guarantee of better generalization and it is not an inference-time uncertainty procedure. Its rate, placement, model architecture, data volume, and other regularizers require validation on held-out data.

## Prerequisites

- [[bernoulli-distribution]]
- [[neural-network]]
- [[regularization]]
- [[tensor]]

## Sources

- [PyTorch `torch.nn.Dropout` documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html): states that elements are independently zeroed during training, sampled from a Bernoulli distribution, and that outputs are scaled by $1/(1-p)$ during training while evaluation is an identity function.
