# Active-Learning Stopping Rules

## Meaning

A stopping rule determines when an active-learning loop ends. It is separate from the acquisition function that chooses the next examples. Stopping because the money ran out does not establish that the model is good enough.

## Mechanism

Declare a limit on query count, elapsed time, accumulated annotation cost or pool coverage. Check feasibility before launching the next batch and reconcile actual cost afterward. An empty eligible pool also ends acquisition. ALiPy implements such resource-oriented limits; a comment about performance plateaus is not an implemented or statistically validated plateau detector.

A progress-based rule needs a different design. Specify the evaluation split, metric, meaningful gain and patience before examining the curve. Account for noisy measurements and repeated validation use. Keep a final test separate. Unchanging predictions can be consistently wrong, and an average plateau can hide progress or failure on an important subgroup.

## One example

A total budget is 100 units. Three completed rounds cost 25, 30 and 20, so only 25 remain. A proposed 30-unit batch cannot be launched unchanged under a strict budget. Checking only after completion could stop at 105, already beyond the limit.

Now consider observed validation accuracies .80, .81 and .81. A predeclared rule requiring .02 improvement for two successive rounds would stop on these point estimates. This demonstrates the procedure, not reliable evidence of convergence: sample size, uncertainty and rare-case coverage can change the interpretation.

## Check your understanding

If acquisition stops, must the model be ready to deploy? No. Record the actual reason—resource limit, empty pool or a qualified progress condition—and report whether quality requirements were met. Test boundary values, delayed labels, changing batch costs and resumed checkpoints. A plateau may call for a better acquisition policy or clearer labels instead of a claim that learning is complete.
