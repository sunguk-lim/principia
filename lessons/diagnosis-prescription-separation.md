# Diagnosis–Prescription Separation

## Meaning

A diagnosis describes what the evidence supports and which defects matter under a stated rubric. A prescription proposes what to do next. Keeping them separate lets an assistant adapt help without silently weakening the assessment when the user cannot afford the ideal repair.

## Mechanism

Use [[decision-context-assistance]] to maintain two records: findings with evidence, severity and uncertainty; and recommended actions with time, resource and authority requirements. The action planner consumes the findings but must not overwrite them. A serious defect can result in narrowing a claim, withholding release or escalating rather than pretending the defect vanished.

The boundary is conditional, not absolute. A deadline ordinarily changes feasibility, while a change from a disposable prototype to medical deployment can change the risk rubric itself. Freeze evidence and rubric when testing diagnosis invariance. [[metamorphic-testing]] then checks a relation across paired contexts: stable findings, appropriately changed recommendations. Do not require unchanged severity when the transformation changes actual harm or criteria.

## One example

An invented report uses one dataset for both tuning and final scoring. Under a fixed scientific-validity rubric, its evidence problem is the same with one day or one month remaining. With one day, prescribe removing the unsupported generalization claim and labeling the result exploratory. With one month, prescribe a fresh held-out evaluation. The assessment remains explicit in both outputs; the short schedule does not turn the report into validated evidence.

## Boundaries and check

Separate output fields alone do not enforce independence if one model reads a pleasing conclusion and rationalizes it. Test adversarial user pressure, blinded assessment, repeated runs and cases where context legitimately changes risk. Audit source evidence as well as label consistency: a consistently wrong diagnosis is still wrong. This is an application design pattern grounded in human-AI guidance and behavioral testing, not a universal statistical guarantee.


## Check your understanding

Should diagnosis always ignore context? No: only operational changes that leave evidence and the rubric fixed justify an invariance expectation.
