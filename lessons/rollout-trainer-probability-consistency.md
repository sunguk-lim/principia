# Rollout–Trainer Probability Consistency

## Meaning

Rollout–trainer probability consistency asks whether the trainer assigns the probabilities of the policy that actually generated its training responses. This is different from asking whether a generated answer looks repeatable.

## Mechanism

A policy update uses sampled tokens and their relationship to an earlier policy. If collection and training use different model snapshots, tokenizers, templates, logits transformations or numerical paths, the comparison can contain a hidden implementation difference. Traffic-dependent arithmetic is one possible source; deterministic serving addresses only that source.

Keep the behavior policy, the stored old-policy probabilities and the current optimized policy distinct. The current policy should change during training. A penalty against a separate reference model measures a different divergence and must not be confused with sampler/trainer agreement.

## One example

At fixed weights, the rollout distribution over two tokens is 0.6 and 0.4. The trainer instead reconstructs 0.55 and 0.45. For the first token its probability ratio is 0.55 divided by 0.6, about 0.917, even before the intended update. That numerical discrepancy can affect an update that assumes both paths represent the same old policy.

Compare log probabilities on the same tokens and actual prefixes at a frozen checkpoint. Include sampling transformations and valid-token masks. Inspect rare large differences as well as averages; a matching score on one sampled token does not establish equality over all possible tokens.

## Check your understanding

Does a flat sampler/trainer discrepancy prove the RL task is solved? **No.** It supports a computation contract on tested cases. Reward validity, exploration, held-out task quality and the expected change to the current policy remain separate checks. Likewise, reproducible text alone does not establish probability equality.
