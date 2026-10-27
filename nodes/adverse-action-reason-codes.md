---
id: adverse-action-reason-codes
title: Adverse-Action Reason Codes
summary: Adverse-action reason codes map the actual principal drivers of a decision into specific reproducible explanations under a scoped notification policy rather than substituting a generic failed-score label.
type: concept
tags: [ml/evaluation]
prereqs: [local-feature-attribution, dataset-lineage]
sources: [https://www.ecfr.gov/current/title-12/chapter-X/part-1002/section-1002.9]
status: explained
created: 2026-10-28
updated: 2026-10-28
---

# Adverse-Action Reason Codes

## Meaning

Adverse-action reason-code design converts the actual principal grounds for an unfavorable decision into specific, understandable statements that can be reproduced later. It is a decision-explanation interface, not merely a ranked list of globally important features. Its legal scope must be explicit: the U.S. credit-notification provision in 12 CFR 1002.9 is not a universal rule for every fraud flag, employment decision or jurisdiction.

## Mechanism

Record the actual decision path before explaining it: model version, feature snapshot, threshold, policy rules, overrides and missing-data handling. [[dataset-lineage]] connects feature values to their source and transformation versions. Where [[local-feature-attribution]] informs candidate reasons, preserve the background population and attribution convention; contribution rankings alone do not establish that the mapped statement is a principal actual reason.

Use a controlled mapping from decision drivers to reason definitions with documented scope and tests. Distinguish a model rejection from a separate policy stop. Validate specificity, fidelity and language comprehension before emitting a code. The cited regulation's paragraph (b)(2) requires specific principal reasons and says internal-policy or failed-qualifying-score statements are insufficient. It does not prescribe one explanation algorithm or establish that a particular template is legally adequate.

## Worked example

Suppose a pipeline first checks whether income documentation is complete, then applies a risk score. Applicant A fails the documentation check, so the risk model never runs. Applicant B passes that check but the score decision is driven by high revolving utilization. Emitting “credit score too low” for both loses the actual path; attributing A's uncomputed model output invents evidence. Store separate driver-to-reason mappings and reproduce each outcome from its archived inputs. These hypothetical mappings illustrate fidelity, not legally approved notice language or a complete notification workflow.

## Validation and alternatives

Audit records by decision path, model version and important population slices. Test feature-to-reason mapping, ties, overrides and equivalent inputs. Reconstruct historical decisions after model changes and retain explanation-method versions. Review the applicable notification obligations separately; specific reasons are only one component of the cited provision, and accuracy of one explanation does not certify the entire product's compliance.

## Check your understanding

Can a faithful SHAP allocation alone establish an adequate adverse-action notice? No. It does not by itself establish principal actual reasons, correct wording, policy-path coverage, jurisdictional applicability or satisfaction of other notification requirements.

## Prerequisites

- [[local-feature-attribution]]
- [[dataset-lineage]]

## Sources

- <https://www.ecfr.gov/current/title-12/chapter-X/part-1002/section-1002.9>
