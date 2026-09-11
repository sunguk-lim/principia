---
id: federated-learning
title: Federated Learning
summary: Federated learning trains one shared model by repeatedly aggregating updates computed on data that remains distributed across participating clients.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, gradient-descent]
sources:
  - https://proceedings.mlr.press/v54/mcmahan17a.html
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Federated Learning

## Summary

**Federated learning** trains a shared [[neural-network]] without first collecting every training example in one place. A coordinator sends a current model to selected clients; each client improves that copy using its local data; the coordinator combines the returned changes into the next shared model.

## Grounded explanation

The central constraint is data location. In ordinary centralized training, examples are moved to a training service, which applies [[gradient-descent]] to one combined dataset. Federated learning instead keeps the examples at clients such as devices or organizations. Only model updates cross the coordination boundary. This can reduce the need to centralize raw data, but it does not by itself guarantee privacy: updates, client participation, logs, and the final model can still reveal information unless the system adds suitable protections.

A training round begins with coordinator parameters $w_t$. It selects a set of available clients and sends each selected client the same $w_t$. Client $k$ runs local gradient descent on its own data for one or more steps and returns an updated parameter vector $w_{t+1}^{(k)}$. If $n_k$ is the number of examples represented by that client's update, the coordinator forms the weighted average

$$
w_{t+1}=\sum_{k=1}^{K}rac{n_k}{N}w_{t+1}^{(k)},\qquad N=\sum_{k=1}^{K}n_k,
$$

where $K$ is the number of updates received in the round. This procedure, commonly called Federated Averaging, lets clients with more represented examples contribute proportionally more to the next shared model.

For a small example, suppose two clients begin a round with the same one-parameter model. After local training, client A, representing $n_A=3$ examples, returns $w_A=2$, while client B, representing $n_B=1$ example, returns $w_B=6$. The coordinator computes

$$
w_{next}=rac{3}{4}\cdot2+rac{1}{4}\cdot6=3.
$$

A simple unweighted mean would have been $4$ and would give the single-example client the same influence as the three-example client. The weighted average is therefore part of the training objective, not merely a networking detail.

Local work reduces communication rounds, but it also creates a tension absent from a single combined dataset. Clients can have different label frequencies, feature distributions, hardware, and availability. With many local steps, their models can move in incompatible directions before averaging; with very few, communication becomes expensive. Practical systems must choose client sampling, local-step count, update deadlines, aggregation weights, privacy protections, and evaluation slices for their actual population rather than assuming that a global validation score represents every client.

Evaluate a federated system against a centralized or local-only baseline with the same model budget. Measure overall and per-client-group quality, convergence rounds and bytes transferred, tolerance of unavailable clients, fairness across heterogeneous clients, and privacy or security properties under the stated threat model. Keeping raw examples local is an architectural boundary; it is not evidence that the resulting learning process is automatically private, unbiased, or robust.

## Prerequisites

- [[neural-network]]
- [[gradient-descent]]

## Sources

- [McMahan et al., “Communication-Efficient Learning of Deep Networks from Decentralized Data”](https://proceedings.mlr.press/v54/mcmahan17a.html): introduces Federated Averaging and evaluates local-update averaging under decentralized, non-IID data.
