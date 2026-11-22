# Skill Procedure Consolidation

## Meaning

Skill procedure consolidation reduces ambiguous duplicate recipes by giving compatible procedures a common task contract. It does not mean placing every version of a procedure into one long prompt. The shared contract states what inputs are required, when the procedure applies and what observable outcome counts as completion. Separate resources retain implementation differences.

## Mechanism

Read each candidate procedure before grouping it. Compare goals, preconditions, permissions, completion checks and recovery paths. Similar wording is a review clue, not evidence of equivalent behavior. Extract only the obligations that genuinely agree. Select the relevant environment-specific resource from trusted runtime information, and treat an unsupported environment as an explicit failure or replanning case. Do not silently broaden the caller's authority.

Progressive disclosure lets an agent read the common procedure and then the necessary resource without loading every variant. Retain the original versions until tests establish that consolidation preserved behavior. A smaller library that loses an important exception is not a successful consolidation.

## One example

Two report-export recipes accept an authorized report identifier and destination. Service A returns the finished file immediately. Service B returns a job identifier and requires polling until completion or a deadline. Their shared contract can require a readable file for the requested report. Their execution resources must remain different: a job being accepted is not a file being completed.

Test A success, A denied access, B success, B timeout and unsupported service C. Compare wrong-variant activation, final task success and context cost with the original procedures. Use tasks not used to design the merged recipe, and keep a rollback path.

## Check your understanding

Two procedures have nearly identical descriptions. Is that sufficient to consolidate them?

No. Their goals, preconditions, permissions, observable effects and recovery behavior must support a common contract. Similarity alone can hide exactly the exception that determines whether execution succeeds.
