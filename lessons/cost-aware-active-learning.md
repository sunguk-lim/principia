# Cost-Aware Active Learning

## Meaning

Cost-aware active learning includes the expense of acquiring each label in the selection decision. Equal label counts do not mean equal budgets when annotations differ in difficulty or require different expertise. The goal is measured quality within a declared resource constraint, not simply the cheapest labels.

## Mechanism

Assign each candidate an estimated benefit and a positive cost. A basic model selects a subset whose summed cost fits the remaining budget and whose estimated total benefit is large. Benefit is uncertain: the true label and the effect of retraining are not yet known. Costs can include annotation, adjudication and selection compute; shared retraining work must also appear in the overall bill.

Sorting benefit divided by cost is an understandable heuristic, but it is not a general optimum for indivisible requests. It can strand budget, and it ignores redundancy between selected examples. ALiPy's primary implementation includes explicit costs and budgeted subset selection; its specific hierarchical multilabel strategy is only one setting.

## One example

The budget is 10 units. A has estimated value 9 and cost 6. B and C each have value 7 and cost 5. A's value/cost ratio is 1.5; the others have 1.4. Ratio-greedy takes A, leaving 4 units and total estimated value 9.

Taking B and C fits the budget exactly and yields estimated value 14 under the toy additive assumption. This counterexample shows why a ratio ranking need not find the best feasible subset. Actual model improvements need not add as these invented values do.

## Check your understanding

Can fewer labels cost more? Yes. Compare actual annotation and adjudication time, compute and quality. Test budget overshoot, changing annotator speed, rare expensive slices and redundant examples. Keep the final evaluation representative rather than evaluating only the deliberately cheap acquired set. Cost prediction and benefit prediction are both fallible.
