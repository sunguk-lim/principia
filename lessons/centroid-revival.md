# Centroid Revival

## Meaning

A center that attracts no useful assignments cannot represent a new region merely by recomputing an empty mean. Centroid revival supplies a policy for reusing that capacity. It is an optimization intervention, not evidence that every implementation leaves empty centers permanently dead.

## Mechanism

In [[k-means-clustering]], define occupancy using current counts or a specified running usage measure. Select centers below a threshold, choose eligible donors or high-residual data points, initialize replacements, and update all associated statistics consistently. Splitting a donor creates nearby alternatives that may subsequently separate. Reseeding from an observed high-error point is a different policy with different outlier sensitivity.

The inspected Faiss e-means implementation checks running mass periodically, samples donors without replacement with probability weighted by their masses, perturbs donor and child coordinates in opposite directions and divides the donor's mass. It does not simply choose the single most crowded cluster. The implementation can disable revival at low dimension, which reinforces that the policy is not universally beneficial. Pin the implementation revision when reproducing it.

## One example

Suppose three centers have running masses 80, 20 and 0. A rule flags the third as underoccupied. Splitting the first could create centers near 9.99 and 10.01 in place of its old position 10, with mass 40 each, while retaining the center of mass 20. These invented offsets show the policy, not Faiss's exact coordinate formula. The next assignments determine whether the split finds structure; it does not immediately divide all points into equal halves.

## Boundaries and check your understanding

Duplicated points, exact ties, zero-valued coordinates, nonfinite data and more centers than distinct observations can prevent useful separation. A coordinate perturbation can round away at the chosen precision. Repeated revival can chase noise or damage a stable solution. Check finite centers, mass bookkeeping, split frequency, occupied-center count, final distortion and downstream quality against disabled-revival and reseeding baselines.

**Check:** Does halving donor mass prove half its observations belong to the child? No. Mass is maintained optimizer state; actual membership follows subsequent assignments.
