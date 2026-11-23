# Reinforcement Learning from Human Feedback

## Meaning

Reinforcement learning from human feedback (RLHF) uses human judgments to guide a policy update. In the common language-model pipeline, people compare responses, a learned model predicts those preferences, and policy optimization increases the predicted reward. Human feedback is the origin of a training signal; it is not a guarantee that every resulting answer is helpful, true or safe.

## Mechanism

Begin from a pretrained model, often applying [[fine-tuning]] to demonstrations of desired behavior. Collect prompt-conditioned comparisons using a documented rater rubric and candidate-generation process. A [[pairwise-preference-model]] fits a reward score from those choices. Keep training comparisons separate from final evaluation prompts and judgments.

Generate responses from the current policy, score them with the reward model and update the policy. [[proximal-policy-optimization]] is one historically important optimizer, not the definition of all possible RLHF. A reference-policy penalty can limit drift; its exact form, value estimation and rollout configuration are implementation choices to pin. This sampling-and-update loop differs from fitting a fixed offline comparison loss alone.

The two learning problems have different failures. A reward model may misrepresent preferences, and the policy may discover ways to score well without satisfying them. [[reward-hacking]] explains why optimizing a fallible proxy can amplify its errors. Training success against that proxy must therefore be evaluated against independent outcomes and fresh judgments.

## One example

An invented support-task rubric prefers answers that are accurate and concise. Raters compare a concise correct answer A with a long incorrect answer B and choose A. A reward model might unfortunately learn shortness as a shortcut if comparisons never include short wrong answers. The policy optimizer then produces very short unsupported answers with high reward.

Add independently labeled short-wrong and long-correct cases, check the reward model's decisions, and measure the optimized policy with new raters and executable task checks where possible. A rising reward curve alone cannot reveal that the policy learned the wrong attribute. This example concerns a possible failure, not a result attributed to the InstructGPT experiments.

## Check your understanding

Does human-origin feedback make the optimized reward an objective measure of truth? No. The rubric, labels, learned proxy and deployment outcome remain distinct.
