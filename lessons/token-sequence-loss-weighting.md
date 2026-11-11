# Token-versus-Sequence Loss Weighting

## Meaning

Loss aggregation decides what counts as one equally weighted observation. Equal response weight and equal token weight are different choices whenever lengths vary. This distinction applies even before selecting an optimizer or reward baseline.

## Mechanism

Let N be the number of responses, T_i the number of valid tokens in response i, and l_it a token's contribution to a [[loss-function]]. A response-averaged loss is (1/N) sum_i [(1/T_i) sum_t l_it]. A token-averaged loss is [sum_i sum_t l_it]/[sum_i T_i]. [[arithmetic]] shows that a token in response i has weight 1/(N T_i) in the first and 1/(sum_i T_i) in the second.

The first gives every response the same total weight. The second gives longer responses more total weight because they contain more valid tokens. Neither definition declares which response deserves more learning. A method can additionally choose a fixed normalization constant, reward scaling or masks; those are different operations.

## One example

Response A has two valid tokens, each with loss 3. Response B has six, each with loss 1. Equal response weighting yields (3+1)/2=2. Token weighting yields (2×3+6×1)/8=1.5. Every token in A has weight 1/4 under the first rule and 1/8 under the second; B's tokens have weight 1/12 versus 1/8. A change in the reported mean can therefore reflect a changed measure rather than improved token predictions.

## Distributed and padded boundaries

Count only valid response tokens, not padding or prompt positions excluded by the objective. Across workers or microbatches, aggregate the numerator and the intended global denominator. Averaging separately normalized local means gives equal worker weight rather than global token weight when counts differ. Gradient accumulation must preserve the same convention; a changing denominator also interacts with update scale.

Check a hand-computed unequal-length batch, an all-masked response, worker imbalance and the gradient contribution of long versus short answers. Report length distribution, correctness and task weighting alongside the scalar loss. Does token averaging intrinsically encourage verbosity? Not by definition; the resulting incentive depends on per-token advantages, sampling, rewards and the rest of the training objective.
