# Distillation Divergence Objective

## Meaning

A teacher and a restricted student need not be able to represent the same distribution. Choosing what mismatch to penalize is therefore part of the distillation method, not merely a numeric implementation detail. [[knowledge-distillation]] defines the transfer task; [[kl-divergence]] supplies an asymmetric discrepancy.

## Mechanism

At one fixed prefix, let p_i be the teacher probability of vocabulary token i and q_i the student probability of that same token. Both vectors use aligned token meanings and sum to one. Forward KL is sum_i p_i log(p_i/q_i); reverse KL is sum_i q_i log(q_i/p_i). Natural [[logarithm|logarithms]] are used here, and zero-probability terms require the usual limiting convention.

Forward KL strongly penalizes omitting teacher-supported outcomes: p_i>0 with q_i=0 gives an infinite term. Reverse KL instead makes student mass outside teacher support infinitely costly. Under restricted model families these pressures can yield different coverage/concentration trade-offs. They do not prove that every forward-trained student covers every useful mode or that reverse KL always collapses. Finite optimization, regularization, vocabulary mismatch and the available data all matter.

## One example

For a fictional three-token prefix, p=(.8,.15,.05) and q=(.6,.25,.15). Forward KL is .8 log(4/3)+.15 log(.6)+.05 log(1/3), about .09859. Reverse KL is .6 log(.75)+.25 log(5/3)+.15 log(3), about .11989. The different values arise from different weighting distributions, not a symmetric distance measured two ways.

## Check your understanding

Does changing KL direction also specify who produces training prefixes? No. A loss can be evaluated on recorded teacher prefixes, current student prefixes or a mixture. Declare both axes, and whether teacher probabilities and enough vocabulary support are actually available. Compare held-out task correctness, alternative-answer coverage, stability and total feedback cost, not divergence alone. Generalized Knowledge Distillation studies alternative losses and prefix distributions; its results do not identify one universally best divergence. Matching an incorrect teacher more closely can still worsen independent task quality.
