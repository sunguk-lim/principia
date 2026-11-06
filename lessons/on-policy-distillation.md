# On-Policy Distillation

## Meaning

A student trained only on externally supplied continuations may encounter unfamiliar prefixes once its own mistakes become context. On-policy distillation samples continuations from the current student and queries the teacher on those same prefixes. It changes where [[knowledge-distillation]] supplies feedback, not whether the teacher is trustworthy.

## Mechanism

For each input, roll out the student's current token policy. At each resulting prefix, evaluate teacher and student distributions over the next token and optimize a declared discrepancy. [[causal-language-model-training]] explains why prefix provenance matters: changing an earlier token changes the later conditional prediction problem. Refresh sampled trajectories as the student changes, or explicitly describe a mixture of current and previously recorded trajectories.

The Generalized Knowledge Distillation paper uses student-generated sequences with teacher token-level probabilities and does not backpropagate through the sampling distribution in its imitation update. That is a concrete training choice, not permission to silently substitute a policy-gradient estimator or assume every algorithm called on-policy uses identical gradients. The prefix distribution and the loss between teacher/student distributions are independent design axes.

## One example

In an invented navigation task the teacher's reference begins “left, bridge,” but the student emits “right.” Training exclusively on the reference only teaches what follows “left.” Student rollout visits “right”; teacher feedback there can teach a recovery continuation such as “return,” if that continuation is representable and appropriate. The student is not retroactively given a correct first action. If the teacher is itself confused after “right,” the new data can reinforce an error instead.

## Check your understanding

Does a repeated replay of a month-old student dataset remain current on-policy data? Not generally: the policy generating it may no longer match the trained student. Compare fixed teacher data, student rollouts and mixtures under matched feedback and training budgets. Measure independent full-trajectory success, recovery after early mistakes, coverage and resource cost. Token agreement is not an external correctness oracle, and a model may need trusted task checks as well as teacher feedback. Serving the trained student still need not retain the teacher.
