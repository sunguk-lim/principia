---
id: linear-programming
title: Linear Programming
summary: Linear programming chooses decision variables that minimize or maximize a linear objective while satisfying linear equality, inequality, and bound constraints.
type: concept
tags: [math/optimization]
prereqs: [linear-transformation, matrix-multiplication]
sources: [https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Linear Programming

## Summary

**Linear programming** optimizes a linear objective over a region described by linear constraints. It is appropriate only when the decision variables, objective, and constraints are all modeled linearly.

## Grounded explanation

Let $x$ be a vector of decisions. A standard minimization form is

$$
\min_x c^T x
\quad\text{subject to}\quad
A_{ub}x \leq b_{ub},\quad A_{eq}x=b_{eq},\quad l\leq x\leq u.
$$

The vector $c$ assigns a marginal cost to each decision. The products $A_{ub}x$ and $A_{eq}x$ use [[matrix-multiplication]] to express capacity limits, resource balances, or other coupled constraints. A row of an equality constraint is a [[linear-transformation]] of the decision vector that must take one exact value; an inequality row sets an upper limit.

**Worked instance.** Suppose $x_1$ and $x_2$ are quantities of two products. Each uses 2 and 1 hours of a 10-hour resource, so $2x_1+x_2\leq10$, and neither quantity may be negative. If their unit costs are 3 and 1, minimizing $3x_1+x_2$ subject to a required output $x_1+x_2=4$ selects $x_1=0, x_2=4$. The result is valid only because the stated costs and resource use are linear; a quantity discount, fixed setup cost, or product choice would change the mathematical program.

A solver can report an optimum, infeasibility, unboundedness, an iteration limit, or numerical difficulty. Treat the status as part of the result. Before relying on a solution, check the residuals of equality constraints, slack in inequalities, variable bounds, units, and whether the linear model represents the real operating constraints. Test small cases whose optimum is known and perturb important coefficients to find decisions that are fragile to estimation error.

## Prerequisites

- [[linear-transformation]]
- [[matrix-multiplication]]

## Sources

- [SciPy `linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html): defines the linear objective, equality and inequality constraints, bounds, solver methods, statuses, residuals, and slack values.
