# Seeded-Defect Evaluator Validation

## Meaning

Seeded-defect validation deliberately introduces known errors into otherwise controlled artifacts, then measures whether an evaluator finds them. It tests the evaluator as an instrument. Counting how many items the evaluator rejects does not reveal whether it detected real defects.

## Mechanism

Define fault families and their ground truth before running the judge: a wrong denominator, unsupported conclusion, leaked test example or unauthorized state change. Review the seed to ensure it actually creates the intended fault without adding irrelevant cues. [[metamorphic-testing]] motivates pairing a valid original with a controlled defective variant, but this method also has explicit fault labels. Keep clean controls and report [[precision-recall]] by fault family and severity.

Keep seed identities hidden from the tested system, randomize presentation and use novel templates for final checks. A repeated obvious phrase can become a shortcut. Inspect detection evidence: identifying a different legitimate problem is not necessarily detection of the planted one. Preserve ambiguous cases for adjudication rather than forcing every item into a clean binary score.

## One example

An invented suite has twenty artifacts with an altered denominator and twenty valid controls. A reviewer flags twelve seeded items and four controls. Fault recall is 12/20=60%; precision among its sixteen flags is 12/16=75%; the control false-positive rate is 4/20=20%. The 40% overall rejection rate alone conveys none of these distinctions. Add a different fault family to test whether denominator success generalizes to unsupported claims.

## Boundaries and check

Synthetic faults may be easier than organic failures, and known-fault coverage does not estimate deployment prevalence. Use real incidents, expert review and independent execution checks as complementary evidence. Freeze a held-out seed set and do not let the repair or generation agent edit its labels. Treat this as bounded coverage evidence, not certification that every unplanted defect will be found.


## Check your understanding

Is planted-fault recall sufficient? No; valid controls and novel fault families are also needed.
