# Value-model-based Augmented PPO

## Meaning

Value-model-based Augmented Proximal Policy Optimization (VAPO) is an integrated actor–critic training recipe for long reasoning outputs. It retains a learned value model and changes how that critic is initialized and used. It is not simply PPO with a different numerical clipping width.

## Mechanism

[[proximal-policy-optimization]] supplies the policy surrogate. VAPO first fits the value model to returns from a fixed policy rather than assuming that a reward-model initialization predicts intermediate-state values. It then separates the critic-target and policy-advantage calculations in [[generalized-advantage-estimation]]: a return-oriented critic target can use lambda=1 while policy advantages use another lambda.

For response length l and positive scale alpha, the proposed policy trace setting is lambda_policy=1-1/(alpha l), where alpha l must be at least one to keep lambda within [0,1]. The motivation is that the infinite geometric weight sum 1/(1-lambda) becomes alpha l. This calibrates a trace horizon to response length; it does not make a finite response's actual weight sum exactly alpha l or make the critic accurate.

The recipe also uses [[token-sequence-loss-weighting]], [[asymmetric-policy-clipping]], groups of sampled answers and a supervised term on successful outputs. That last component follows the imitation idea in [[success-filtered-self-training]], but supplements rather than replaces the policy update. Each changes a different part of the learning procedure.

## One example

Take alpha=.5. A length-10 response gets lambda=.8, while length 100 gets .98. A residual five positions away has relative weight .8^5=.32768 in the first case versus .98^5≈.90392 in the second, ignoring discounting. A fixed .95 would weight a residual 100 positions away by .95^100≈.00592. These conditional calculations show the intended horizon change, not measured task gains. Larger distant-reward influence can also carry more noise.

## Boundaries and check

Read value calibration, response-length slices, actor and critic targets, accepted imitation samples and all loss coefficients together. Ablate components with matched prompts, rollout tokens and compute rather than attributing a combined recipe to one trick. The primary paper's benchmark results are author-reported experiments, not universal superiority. Does value pretraining remove future critic drift? No: the policy and visited prefixes change during learning, requiring continued validation.
