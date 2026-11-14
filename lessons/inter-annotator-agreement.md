# Inter-Annotator Agreement

## Meaning

Agreement measures how reproducibly raters apply a defined labeling task. It is not automatically accuracy. Two people can consistently apply the same wrong rule. Choosing a coefficient is only one part of the study; sampling, independence and task definition determine what the number means.

## Mechanism

Preserve item, annotator, original label and instruction version through [[dataset-lineage]]. Raters should independently label common items before discussing disagreements. Specify label types, eligible comparisons and missing-rating treatment. For two categorical raters, a [[confusion-matrix]] retains agreement and directional disagreement.

Raw agreement estimates the [[probability]] that an eligible pair matches. A chance-adjusted statistic adds a specified baseline and answers a different question. Multiple raters, incomplete assignments and ordered labels require an estimator matching that design rather than blindly applying a two-rater formula.

Adjudication is a subsequent policy decision. Preserve pre-adjudication labels instead of replacing them with consensus and then measuring an artificially perfect agreement. Report counts, prevalence, uncertainty and important difficulty or source slices.

## One example

Two raters label 20 cases. They both accept eight, both reject seven and disagree on five. Raw agreement is (8+7)/20=.75. If the five disagreements all concern new borderline instructions, the aggregate hides a policy problem. Revise the instructions and independently rate fresh cases to test improvement; discussion of the original five alone does not estimate improved reproducibility.

An independent audit could still find errors among the fifteen agreements. The observed .75 is therefore neither accuracy nor evidence that every majority label is correct. Check duplicate items, mismatched codes, rater influence and sampling bias before interpreting the score.

## Check your understanding

Does consensus after discussion establish that the original task was reliably specified? No. Consensus can settle particular cases, but reproducibility needs new independent ratings under the clarified policy. Keep study design and adjudication outcomes distinct.
