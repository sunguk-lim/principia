# Task-Aligned Loss Selection

## Meaning

An algorithm name does not uniquely determine the right objective. Choose a [[loss-function]] from the prediction target and its error meaning, then verify that the fitted predictions support the operational decision. Predicting a number, predicting a probability and choosing an action are related but different contracts.

## Mechanism

Begin with [[ml-task-specification]]: who acts on the output, what outcome matters and which errors are costly? Specify whether a numeric prediction should represent a central value or an upper safety allowance, or whether a classifier must estimate probabilities rather than only a label. The same model family may support several training objectives. Convenient optimization is not proof that the chosen objective elicits the quantity the application needs.

For a simple constant predictor on observations 1, 2 and 9, squared error is minimized at their mean, 4: its total is 9+4+25=38. At 2 the squared total is 1+0+49=50. Absolute error instead favors the middle observation, 2: its total is 1+0+7=8, versus 3+2+5=10 at 4. The two objectives deliberately select different summaries of the same data; neither is universally the right target. These arithmetic examples illustrate the target distinction, not performance of a commercial model.

A probability estimate also needs a separate action rule. Changing a decision threshold changes false-positive and false-negative counts without retraining the probability model. If missing a dangerous case costs 20 units and an unnecessary review costs 1, a classifier with more total label errors may still have lower operational cost. Calibration, threshold tuning and final acceptance need their own held-out evidence rather than reusing the training score.

## One example

On an invented acceptance set, policy A misses 2 dangerous cases and triggers 8 unnecessary reviews; its cost is 2×20+8=48. Policy B misses 1 and triggers 15 reviews; its cost is 1×20+15=35. A makes 10 label errors and B makes 16, yet B has lower cost under this declared rule. This does not imply that choosing a threshold on this same set produces an unbiased evaluation: tune earlier and reserve final acceptance data.

## Check your understanding

Can “regression uses squared error” settle the choice? No. Establish the quantity, error asymmetry and data assumptions first. Use [[measurement]] to compare the training target, held-out predictive score and final decision cost separately, including critical slices and changed conditions. Do not describe a tree's split impurity as interchangeable with every final training or deployment objective.
