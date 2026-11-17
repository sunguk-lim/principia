# Numerical Comparison Contract

## Meaning

A numerical comparison contract makes “close enough” an explicit requirement rather than a visual judgment. It names the operation and reference, fixes relevant arithmetic settings, and chooses an error budget before evaluating a result. Equal formulas do not imply equal floating-point bit patterns, while equal bit patterns do not prove the formula is right.

## Mechanism

For finite components, compare `abs(actual-reference)` with `atol + rtol*abs(reference)`. Absolute tolerance matters near zero; relative tolerance scales with reference magnitude. Choose both for the application and arithmetic, not just the storage dtype. Intermediate accumulation may use a different precision. Machine epsilon describes spacing near one and is not a bound on an arbitrary long computation.

A small wider-precision implementation can serve as a reference, but it still needs correct masks and indexing. Check each candidate against it, and include finite-output and gradient checks where relevant. Two implementations agreeing with each other can share a mistake. Record masks, shapes, backend and versions so a failure can be reproduced.

## One example

Suppose the declared limits are `atol=1e-6` and `rtol=1e-4`. For reference 100 the allowed error is 0.010001, so 100.005 passes. For reference zero the allowed error is only 0.000001, so 0.000002 fails. A smaller absolute difference is therefore not automatically more acceptable: scale and the stated contract matter.

## Understanding check

Does a difference smaller than machine epsilon establish correctness? No. It says little without magnitude, operation and reference semantics. Use error locations to guide investigation, but remember that rounding can have structure and defects can be tiny. Evaluate downstream outcomes separately from kernel closeness and bitwise reproducibility.
