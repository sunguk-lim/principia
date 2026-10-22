---
id: work-span-model
title: Work-Span Model
summary: The work-span model separates total computation from the longest dependency chain to bound execution time with finite processors.
type: concept
tags: [computing/performance]
prereqs: [computation-graph, arithmetic]
sources: [https://www.cs.cmu.edu/afs/cs/academic/class/15210-f15/www/tapp.html]
status: explained
created: 2026-10-23
updated: 2026-10-23
---

# Work-Span Model

## Meaning

Work counts everything an algorithm must execute. Span counts the longest chain of dependent operations. Lower work does not guarantee lower elapsed time when the smaller computation exposes less parallelism. These are properties of a specified execution graph and cost model, not percentages inferred from accelerator activity.

## Mechanism

Use a [[computation-graph]] without dependency cycles. Assume each operation takes one time unit, data are ready, and scheduling has no overhead. Define W as total operations, S as operations on the longest directed path, P as available identical processors, and T_P as elapsed execution steps. [[arithmetic]] gives two lower bounds:

$$T_P\geq\max(W/P,S).$$

At most P operations finish per step, so all W need at least W/P steps. No schedule can run a consumer before its producer, so every operation on the longest path must wait for its predecessors. W/S is the average available parallelism; increasing P far beyond it cannot yield proportional speedup. Ideal greedy scheduling gives an upper bound of W/P+S, not an assurance that a real accelerator reaches it. Different operation durations require weighted work and weighted paths.

## Worked example

Compare an eight-operation chain with a sixteen-operation balanced reduction tree: eight independent leaf operations, then four combines, two combines, one combine and a final dependent output operation. The chain has W=8, S=8; the tree has W=16, S=5. With eight processors the tree's stages take 1+1+1+1+1=5 steps, beating the chain's eight despite twice the work. With two processors the same level schedule takes 4+2+1+1+1=9 steps; now the chain wins. More work is not always faster either.

Memory movement, launches, communication, imperfect load balance and changing arithmetic precision alter real costs. State whether a matrix product is modeled as one weighted operation or many scalar operations before claiming constant attention depth. A causal training mask does not create a position-to-position execution chain, but reductions still take time. Validate the model with operation dependencies and measured timelines rather than equating asymptotic work with GPU seconds.

## Check your understanding

**Question:** Can unlimited processors make an eight-step dependent chain finish in one step? **Answer:** No; its span remains eight under the stated operation model.

## Prerequisites

- [[computation-graph]]
- [[arithmetic]]

## Sources

- <https://www.cs.cmu.edu/afs/cs/academic/class/15210-f15/www/tapp.html>
