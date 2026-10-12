# LLM Policy Optimization Method Selection

## Meaning

PPO, DPO, and GRPO differ in the feedback they require and in how they use data. Selecting an optimizer begins with the available reward or preference signal, not a leaderboard rank.

## Mechanism

PPO updates from sampled trajectories and an advantage estimate, using the [[advantage-baseline]] idea. DPO learns from offline preferred/rejected pairs. GRPO samples several responses for one prompt and compares their rewards within the group; it can use [[reinforcement-learning-from-verifiable-rewards]]. All methods can fail when feedback is noisy or biased, and [[reward-hacking]] is a risk for methods that optimize an exploitable scorer.

## One example

For arithmetic tasks with an exact-answer checker but few human preference pairs, compare a supervised baseline with GRPO or PPO at matched rollout cost. For a writing task with trusted preference pairs but no executable correctness check, DPO may be more practical. Evaluate each on held-out tasks, not training reward alone.

## Check your understanding

**Question:** Does GRPO eliminate all extra compute? **Answer:** No. It removes a separate value model but still needs multiple sampled responses and reward evaluation.
