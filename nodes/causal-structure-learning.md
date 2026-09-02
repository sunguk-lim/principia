---
id: causal-structure-learning
title: Causal Structure Learning
summary: Causal structure learning searches observational or interventional data for a directed acyclic graph whose arrows encode candidate direct causal relations consistent with stated assumptions.
type: concept
tags: [ml/deep-learning]
prereqs: [conditional-independence, directed-acyclic-graph]
sources: [https://www.jmlr.org/papers/v3/chickering02b.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Causal Structure Learning

## Summary

**Causal structure learning** infers a graph of candidate cause–effect directions from data rather than taking that graph as given. It uses patterns that a proposed graph predicts—especially conditional independences or a data-fit score—while relying on explicit assumptions to connect those statistical patterns to causal arrows.

## Grounded explanation

Represent measured variables as vertices in a [[directed-acyclic-graph]]. An arrow $X\to Y$ says that $X$ is a direct causal parent of $Y$ relative to the included variables. A path through intermediate vertices represents an indirect relation, so the goal is not to connect every associated pair but to find a sparse structure explaining the observed dependencies.

Two major strategies test candidate structures differently:

1. **Constraint-based learning** asks which [[conditional-independence]] statements the data support and removes or orients edges to match them.
2. **Score-based learning** assigns each candidate DAG a score balancing fit to the observations against excessive complexity, then searches for a high-scoring graph.

Both strategies face an identification limit: several DAGs can imply exactly the same conditional-independence statements. Observational data then identify an equivalence class rather than one uniquely oriented graph. Background knowledge, time order, distributional assumptions, or interventions may distinguish members of that class. Without such assumptions, an arrow is not justified merely because two variables are associated.

### Worked example

Suppose the measured variables are rain $R$, sprinkler use $S$, and wet grass $W$. Data show little association between $R$ and $S$ overall, but after conditioning on $W$ they become associated. Consider the candidate DAG

$$
R\to W\leftarrow S.
$$

It predicts that $R$ and $S$ need not be associated before $W$ is known, while conditioning on their shared effect $W$ can relate them: if the grass is wet and it did not rain, sprinkler use becomes more plausible. The chain $R\to W\to S$ predicts a different pattern: $R$ and $S$ should become conditionally independent given $W$. A constraint-based procedure can therefore reject the chain when that independence fails.

A score-based procedure instead compares candidate scores. If the three-edge graph also adds $R\to S$, it may fit the finite sample slightly better, but a complexity penalty can favor the two-edge collider above. Search matters because the number of possible DAGs grows rapidly; practical methods modify one edge at a time, evaluate the resulting constraints or score, and stop at a structure no permitted move improves.

The output is best read as “causal structure supported under the declared variable set and assumptions,” not as causality manufactured from correlations. Hidden common causes, selection of which records are observed, or incorrect independence tests can all change the learned structure.

## Prerequisites

- [[conditional-independence]]
- [[directed-acyclic-graph]]

## Sources

- Chickering, “Optimal Structure Identification With Greedy Search,” *Journal of Machine Learning Research* 3 (2002) — score-equivalent DAG structure search and equivalence classes.
