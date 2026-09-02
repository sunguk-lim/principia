---
id: differential-equation
title: Differential Equation
summary: A differential equation constrains an unknown function through the values of that function and one or more of its derivatives.
type: concept
tags: [math/calculus]
prereqs: [derivative]
sources: [https://tutorial.math.lamar.edu/classes/de/definitions.aspx]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Differential Equation

## Summary

A **differential equation** is an equation whose unknown is a function and whose rule relates that function to its [[derivative]] or derivatives.

## Grounded explanation

For an unknown function $x(t)$, the equation

$$\frac{dx}{dt}=-2x$$

says that the instantaneous rate of change is always minus twice the current value. A solution is a whole function satisfying that relation, not one number. Initial or boundary conditions select one solution from a family.

### Worked example

Try $x(t)=3e^{-2t}$. Its [[derivative]] is $-6e^{-2t}$, while $-2x(t)=-6e^{-2t}$, so it satisfies the equation. It also satisfies $x(0)=3$. At $t=0.5$, the value is $3e^{-1}$ and its rate is $-6e^{-1}$.

Order is the highest derivative present. An ordinary differential equation has one independent variable; a partial differential equation has several and uses partial derivatives. Numerical methods approximate a solution at discrete points when no convenient closed form exists.

## Prerequisites

- [[derivative]]

## Sources

- Paul's Online Math Notes, “Definitions — Differential Equations.”
