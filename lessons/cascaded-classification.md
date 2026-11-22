# Cascaded Classification

## Meaning

A classification cascade sends only selected inputs to later decision stages. It can reject easy negatives cheaply before using an expensive model or human reviewer. The defining idea is conditional routing, not voting by models that all see every case.

## Mechanism

The first stage determines which population the second stage receives. For a positive example to be detected, it must pass the first stage and then be accepted by the second. Final recall is the fraction of positives forwarded multiplied by the fraction accepted among those forwarded positives. This multiplication uses conditional measurements; it does not assume independent stages.

A reviewer cannot recover positives rejected before review. Similarly, its error rate on an ordinary test set need not match its error rate on the harder survivors. Evaluate both stages together and retain stage-specific counts. Measure the review load as well as accuracy: a reviewer without sufficient capacity can create an unbounded wait rather than a completed decision.

## One example

An invented batch contains 100 positives and 9,900 negatives. Stage one forwards 90 positives and 990 negatives. The reviewer accepts 81 positives and 99 negatives. Final recall is 81/100=81%, and precision is 81/(81+99)=45%. Although only 1% of the negatives survive both stages, the final alert list is still mostly false positives because negatives were common.

At a first-stage cost of one unit per input and review cost of ten units per forwarded case, total work is 10,000+1,080×10=20,800 units. Reviewing all inputs would cost 100,000 units in this simplified model. The saving comes with nineteen missed positives and must be judged against the application's error costs.

## Check your understanding

Can perfect review guarantee perfect recall after a first stage that forwards only 90% of positives?

No. The discarded 10% never reaches review. Audit early rejections and test changing populations; a fixed threshold or architecture alone cannot guarantee a permanent precision or recall floor.
