---
id: momentum
title: Momentum
summary: Momentum augments gradient descent with a decaying velocity of earlier update directions, smoothing noisy zig-zags while accelerating consistent descent.
type: concept
tags: [ml/deep-learning]
prereqs: [gradient-descent]
sources:
  - 'Polyak, "Some Methods of Speeding Up the Convergence of Iteration Methods" (1964), https://doi.org/10.1016/0041-5553(64)90137-5'
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Momentum

## Summary

**Momentum** changes [[gradient-descent]] so that an update remembers a decaying
fraction of earlier updates. When successive gradients point in a consistent direction,
the remembered velocity accumulates and moves faster; when gradients alternate across a
narrow valley, their opposing contributions partly cancel. It therefore trades one new
hyperparameter for less oscillation and faster progress along persistent descent
directions.

## Grounded explanation

Plain [[gradient-descent]] uses only the gradient at the current parameters:

$$\theta_{t+1} = \theta_t - \eta g_t,$$

where $g_t = \nabla \mathcal{L}(\theta_t)$ and $\eta$ is the learning rate. This is
locally sensible, but a loss surface can be steep in one direction and shallow in
another. A step that repeatedly crosses the steep direction makes the iterates zig-zag,
even while the shallow direction consistently points toward a lower loss.

Momentum keeps a velocity $v_t$ that is a decaying sum of recent negative gradients:

$$v_{t+1} = \beta v_t - \eta g_t,$$

$$\theta_{t+1} = \theta_t + v_{t+1}.$$

The coefficient $\beta$, commonly chosen between zero and one, controls how long an
old update remains influential. Expanding the recurrence shows the mechanism:

$$v_{t+1} = -\eta(g_t + \beta g_{t-1} + \beta^2 g_{t-2} + \cdots).$$

Thus, gradients that keep the same sign reinforce one another. Alternating gradients
have opposite signs, so their weighted contributions cancel instead of repeatedly
pushing the parameters from one side of a valley to the other.

Consider a point whose gradient is consistently $+1$ in a shallow horizontal direction
but alternates $+10, -10, +10, -10$ vertically. Plain gradient descent takes the same
horizontal step every iteration and large vertical steps that reverse each time.
Momentum still adds the repeated horizontal signal to its velocity, so horizontal motion
builds up. The vertical signals instead cancel in the velocity over adjacent iterations,
reducing the saw-tooth path. This is not a guarantee of convergence: it is a change in
the update dynamics that can help when the observed gradient direction is persistent.

The benefit has a corresponding risk. A large $\beta$ gives old directions a long
memory. That can carry an iterate through small noisy variations, but it can also carry
it past a minimum or make it slow to react when the loss geometry changes. The learning
rate and momentum coefficient must therefore be chosen together; increasing either can
make the update unstable. Setting $\beta=0$ removes the velocity and recovers ordinary
[[gradient-descent]].

## Prerequisites

- [[gradient-descent]]

## Sources

- Polyak, "Some Methods of Speeding Up the Convergence of Iteration Methods" (1964),
  https://doi.org/10.1016/0041-5553(64)90137-5.
