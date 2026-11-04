# Intrinsic Self-Correction

## Meaning

Intrinsic self-correction is a draft–critique–revise process in which the model supplies both an answer and the feedback used to change it, without receiving an external correctness judgment. Its defining boundary is the information available to the critic, not whether a second API request was made. A calculator result, source lookup or executable test introduces a different signal and must be evaluated as a different condition.

## Mechanism

First generate a proposed solution, optionally with [[chain-of-thought]]. Next ask for a bounded critique against explicit criteria. Finally produce a revision conditioned on that critique. Keep the model, prompt, revision budget and stopping rule recorded. Feedback may expose an overlooked constraint even when the weights stay fixed, but the critic can inherit the same false premise or be persuaded that a correct draft is wrong. The existence of another reasoning pass is not independent evidence.

The primary Self-Refine work reports improvements from iterative feedback in its tested tasks. The primary reasoning self-correction study finds failures and degradation without external feedback under its evaluated conditions. These are workload- and procedure-dependent observations, not mutually exclusive laws about every model. Neither title establishes the outcome for a new numerical-extraction workflow.

## One example

Consider an invented evaluation of 100 tasks. The first answers contain 70 correct and 30 incorrect results. Revision repairs 12 incorrect results but corrupts 8 correct ones. Final correctness is 70+12−8=74. The repair rate is 12/30=40%, while the corruption rate is 8/70, about 11.4%. Reporting only “12 errors repaired” hides the damage; reporting only 74% hides which transitions occurred. If a new prompt repairs 6 and corrupts 10, correctness falls to 66 despite using more computation.

## Check your understanding

Does fluent critique establish that a revision is better? No. Use [[measurement]] on held-out tasks, keeping original and revised outputs for blind comparison. Count correct-to-wrong and wrong-to-correct transitions, unchanged errors, abstentions, tokens and elapsed time. Compare no revision, intrinsic feedback and externally grounded checks under declared budgets. Stop after a bounded number of unproductive passes; do not treat changing an answer as evidence of progress.

