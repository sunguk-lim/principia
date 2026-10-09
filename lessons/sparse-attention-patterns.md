# Sparse Attention Patterns

## Meaning

Sparse attention computes only selected token-to-token interactions. It can reduce the number of scores compared with dense attention, but the chosen pattern determines what information can travel.

## Mechanism

A local window connects nearby positions. Strided, global, or random links can carry information farther. Multiple layers can propagate through intermediate positions, but a missing short path may harm long-range tasks. Count the edges actually computed and check whether kernels avoid dense intermediate tensors.

## One example

A document question depends on a fact at the beginning and a fact at the end. A narrow local window may not connect them soon enough; a global token or suitable sparse link may. Test the actual task rather than assuming lower theoretical complexity guarantees a good answer.

## Check your understanding

**Question:** Why can sparse attention fail to speed inference? **Answer:** Irregular indexing or dense masked computation can cost more than the saved arithmetic.
