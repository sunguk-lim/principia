# Optimization Solver Interface

## Meaning

A model's objective and the algorithm used to fit it are different objects. An optimization solver interface selects the fitting procedure and exposes some of its controls. It need not expose the fixed step size familiar from [[gradient-descent]], even when fitting changes the same model parameters.

## Mechanism

The [[loss-function]] defines what is minimized, possibly including [[regularization]]. The solver decides how to propose updates and stop. A fixed-step method exposes a learning rate; another method may choose steps internally or use curvature information. A library can expose solver choice, maximum iterations and convergence tolerance while hiding lower-level update decisions. No visible learning-rate parameter therefore does not imply no optimization, no step selection or no convergence sensitivity.

Separate controls by meaning. Regularization changes the objective. A stopping tolerance changes the acceptance criterion. An iteration cap limits work and can stop before convergence. Data scaling can alter numerical conditioning. Solver/penalty compatibility and defaults can change by version; record the exact estimator implementation instead of transferring hyperparameters between superficially similar APIs.

## One example

For an invented scalar objective f(w)=(w-3)^2 starting at w=0, the derivative is 2(w-3). A fixed learning rate .1 gives w=0-.1*(-6)=.6 on its first update, with loss (0.6-3)^2=5.76 rather than 9. A method that minimizes this particular quadratic exactly would choose w=3 immediately without asking the user for .1. The target objective is unchanged; its update rule and exposed controls differ. This illustration is not a description of any library's complete logistic-regression algorithm.

## Check your understanding

Does increasing max_iter guarantee better held-out prediction? No. It permits more fitting work; the estimator may already be converged, may converge poorly or may generalize worse under another objective. Use [[measurement]] to check convergence warnings, objective behavior, held-out quality, scaling sensitivity, runtime and memory. Scikit-learn's LogisticRegression documents several solvers plus tolerance and iteration controls without a user learning-rate argument. Consult current solver compatibility rather than inferring that all implementations fit identically or that a solver eliminates tuning.
