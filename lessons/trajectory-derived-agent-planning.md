# Trajectory-derived agent planning

A completed trace is not the same thing as a plan that was available at the start. If an agent tried three suppliers and only the third worked, a summary written afterward can say “choose the third supplier.” A planner trained on that summary would be rewarded for knowing a fact it could not have known at the original decision time. This is temporal leakage in plan supervision.

Build a training example at each decision boundary. Its input is the task and observations available so far; its label is an intended next step or revised plan written without seeing later observations. Keep the planner's output separate from the executor's low-level action examples. When new evidence changes the route, record the replan rather than pretending the successful final path was the original intention.

For example, a trace might show `check inventory → option A unavailable → check B → B compatible`. The initial plan can say “check available compatible options.” After A fails, a new example can say “check B.” Neither early label may assert that B is compatible before the check. Include failures and recoveries, not only successful final trajectories.

Validate on held-out tasks. Ask whether labels mention unavailable facts, whether proposed steps are feasible, whether the executor can complete them, and whether replanning responds to changed evidence. Compare against direct action and hindsight-labeled baselines at matched budgets. A plan that sounds polished is not evidence of executable foresight.

**Check:** If a label mentions an observation discovered five actions later, which boundary was violated?
