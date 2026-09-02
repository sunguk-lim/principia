---
id: physics-informed-neural-network
title: Physics-Informed Neural Network
summary: A physics-informed neural network trains a neural function approximation by penalizing violations of a differential equation and its boundary or initial constraints alongside any observed-data error.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, differential-equation, gradient-descent, loss-function]
sources: [https://doi.org/10.1016/j.jcp.2018.10.045]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Physics-Informed Neural Network

## Summary

A **physics-informed neural network** (PINN) represents an unknown physical field with a neural function and trains it not only against observations but also against the governing differential equation. Equation residuals at sampled coordinates act as supervision where measured target values are unavailable.

## Grounded explanation

Let $u_\theta(x,t)$ be the output of a [[neural-network]] with trainable parameters $\theta$, spatial coordinate $x$, and time $t$. Suppose the desired field must satisfy the [[differential-equation]]

$$
\frac{\partial u}{\partial t}+\mathcal{N}[u]=0,
$$

where $\mathcal{N}$ is a specified spatial operation. Substitute the network into the equation to define the residual

$$
r_\theta(x,t)=\frac{\partial u_\theta}{\partial t}(x,t)+\mathcal{N}[u_\theta](x,t).
$$

The derivatives are computed from the network's operations, so $r_\theta$ remains a function of $\theta$. A typical [[loss-function]] combines observed or boundary values with residual samples:

$$
L(\theta)=\frac{1}{N_u}\sum_{i=1}^{N_u}|u_\theta(x_i,t_i)-y_i|^2
+\lambda\frac{1}{N_r}\sum_{j=1}^{N_r}|r_\theta(\tilde x_j,\tilde t_j)|^2.
$$

Here $(x_i,t_i,y_i)$ are $N_u$ known values, $(\tilde x_j,\tilde t_j)$ are $N_r$ residual coordinates, and $\lambda$ balances the two requirements. [[gradient-descent]] changes $\theta$ to reduce this joint objective. The decisive idea is that a coordinate needs no measured label to contribute a residual: the equation itself supplies the target value zero.

### Worked example

Consider the decay equation

$$
\frac{du}{dt}+u=0,\qquad u(0)=2.
$$

Use the one-parameter trial network $u_a(t)=2+at$, which already satisfies the initial value. Its residual is

$$
r_a(t)=\frac{du_a}{dt}+u_a(t)=a+(2+at).
$$

Sample residual points $t=0$ and $t=1$. The physics loss is

$$
L(a)=\tfrac12[r_a(0)^2+r_a(1)^2]
=\tfrac12[(a+2)^2+(2a+2)^2].
$$

Differentiating gives $dL/da=(a+2)+2(2a+2)=5a+6$, so the best parameter in this restricted family is $a=-6/5$. The resulting $u_a(t)=2-1.2t$ is not the exact curved solution, but it is the line whose equation violations at the sampled points are jointly smallest. A richer network and more residual coordinates can represent and enforce the curve more closely.

PINNs can also infer unknown equation parameters by including them in $\theta$, but the governing operator and constraints must still be specified. A small residual at sampled coordinates is evidence only within the sampled domain and chosen objective; it does not guarantee accuracy between those points, and badly balanced loss terms can make one constraint dominate the others.

## Prerequisites

- [[neural-network]]
- [[differential-equation]]
- [[gradient-descent]]
- [[loss-function]]

## Sources

- Raissi, Perdikaris, and Karniadakis, “Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations,” *Journal of Computational Physics* 378 (2019) — neural representations constrained by differential-equation residuals.
