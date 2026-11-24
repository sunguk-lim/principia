---
id: parallel-transformer-block
title: "Parallel Transformer Block"
summary: "A parallel Transformer block computes attention and feedforward updates from the same pre-block state, removing the within-block dependency between those branches without making the architecture equivalent to a serial block."
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, position-wise-feed-forward-network, residual-connection, layer-normalization]
sources: [https://arxiv.org/html/2204.02311v5, https://raw.githubusercontent.com/black-forest-labs/flux/main/src/flux/modules/layers.py]
status: explained
created: 2026-11-25
updated: 2026-11-25
---

# Parallel Transformer Block

## Meaning

A conventional serial Transformer block computes an attention update and then lets a feedforward branch read the updated state. A **parallel block** lets both branches read the same pre-block state and combines their outputs afterward. “Parallel” describes which inputs the branches depend on; it does not promise concurrent hardware execution or distribution across devices.

## Mechanism

Let $x$ be the input token-state array, $N$ a [[layer-normalization]] operation, $A$ the [[transformer-attention]] branch and $F$ the [[position-wise-feed-forward-network]] branch. Each branch returns an array with the same shape as $x$. A shared-normalization parallel block forms

$$y=x+A(N(x))+F(N(x)).$$

The additions implement a [[residual-connection]]. Neither branch needs the other's new result. By contrast, a common serial pre-normalized block first forms $u=x+A(N(x))$ and then $y=u+F(N(u))$. The serial feedforward branch reads $u$, not $x$. Changing between these forms generally changes the function and training behavior; it is not an algebraically exact optimization of arbitrary pretrained serial weights. Other architectures may use separate normalization or gating, so state the actual equations.

Independent inputs can enable larger combined input projections and a shorter dependency path. Nonlinear activation and attention still execute as separate operations, and both results must be ready before their sum is consumed. Hardware scheduling, workspace memory and matrix shapes decide whether overlap or projection combination helps. A branch-level architecture is distinct from a projection-fusion implementation: one describes which state each branch reads, the other groups compatible matrix operations.

## One example

Use deliberately simple scalar stand-ins to expose the dependency, not to model a trained attention layer. Let normalization be the identity, $x=2$, $A(t)=3t$ and $F(t)=t^2$. The parallel result is $2+6+4=12$. In the serial version, $u=2+6=8$ and the result is $8+64=72$. Both branches participate, but changing the feedforward input changes the answer. A real block uses arrays and nonlinear normalization; the counterexample merely disproves universal functional equivalence.

## Boundaries and validation

PaLM's primary report documents parallel attention/feedforward layers and possible input-projection fusion. Its measured speed and quality are specific to that model and setup, not guarantees for another implementation. Flux provides a concrete single-stream implementation with combined projections; its additional choices are not the definition of every parallel block.

Test a reference implementation against the intended equation, including normalization placement, output shape, branch scaling, bias and any stochastic masks. Compare serial and parallel architectures after appropriate training at matched parameters and compute; do not demand equal outputs from different functions. Separately compare fused and unfused implementations of the *same* parallel block for numerical agreement, peak memory and runtime over representative workloads. More theoretical concurrency may lose in practice when memory use or small kernels dominate.

## Check your understanding

Does running a serial attention-then-MLP block on two streams make it a parallel block? No. The MLP still depends on the attention-updated state.

## Sources

- <https://arxiv.org/html/2204.02311v5>
- <https://raw.githubusercontent.com/black-forest-labs/flux/main/src/flux/modules/layers.py>
