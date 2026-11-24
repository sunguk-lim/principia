---
id: retrieved-policy-authority
title: "Retrieved Policy Authority"
summary: "Retrieved policy authority binds an application decision to an explicitly approved policy scope and version rather than treating model recollection, similarity rank or the newest-looking document as governing authority."
type: concept
tags: [ml/agents]
prereqs: [rag-freshness-contract, prompt-injection]
sources: [https://model-spec.openai.com/2026-10-29.html#chain_of_command, https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html, https://docs.langchain.com/oss/python/concepts/memory]
status: explained
created: 2026-11-25
updated: 2026-11-25
---

# Retrieved Policy Authority

## Meaning

A model can recall an old rule while retrieved text describes a different one. **Retrieved policy authority** is the application's explicit contract for deciding which approved rule applies to this caller, resource, action and time. It separates evidence about a policy from permission to govern behavior. Neither a confident recollection nor a highly similar passage establishes that permission.

## Mechanism

Keep an approved policy registry or equivalent trusted configuration outside generated text. Associate each applicable rule with its issuer, scope, effective interval and revision. Define how exceptions and overlapping rules compose. The application selects the eligible policy set and places bounded, provenance-bearing evidence into the model's input; an arbitrary document must not declare itself the new highest-priority policy.

A [[rag-freshness-contract]] distinguishes observing a new revision, making it searchable and allowing it to be used. Before relying on a rule, verify its authority and current eligibility, not just the index timestamp. A newer draft can be less authoritative than an older approved release. Current authorization and applicable policy version are related but different questions: permission to read a document does not make its content governing law.

[[prompt-injection]] explains the second boundary. Retrieved text is ordinarily evidence, not a replacement for the application's trusted instructions. If the application delegates a particular policy decision to an approved source, keep that delegation narrow and explicit. Delimiters and provenance help communicate this boundary; they do not guarantee model compliance. The inherited [[tool-call-execution-contract]] requires trusted code to validate sensitive effects even if the model produces a persuasive explanation.

## One example

In an invented expense system, the model's old training examples use a limit of 100 units. The registry says approved revision 8 lowers the applicable limit to 75 units. A retrieved draft revision 9 proposes 120 units but is not effective. For a request of 90 units, the application evaluates revision 8: 90 exceeds 75 by 15. The old learned rule and the future draft cannot authorize the transaction.

The model can explain the discrepancy with the approved revision. If the registry is unavailable, it should not silently choose whichever number is easiest to recall. The application follows a declared wait, deny or escalation rule for that action. A denial is not a successful transaction, and a readable draft is not an approved exception.

## Boundaries and validation

This is an application architecture, not a claim that one provider's message hierarchy automatically implements an organization's business policy. The Model Spec documents intended message authority and explicitly distinguishes external content; it also states that intended behavior is not perfect compliance. OWASP grounds authorization outside client-controlled decisions. Neither supplies the application's version registry or conflict-resolution procedure.

Test obsolete learned rules, inconsistent approved documents, future drafts, missing registry state, forged issuer labels, policy changes during long execution and correct exceptions. Score the resulting permitted or denied effects, not merely whether the answer quoted the current document. Include allowed cases so a system that refuses everything cannot pass. Preserve the policy revision and observed decision evidence without disclosing protected source content.

## Check your understanding

Does the highest-ranked, newest retrieved document automatically override a learned rule? No. Applicable authority, effective scope and current approval must be established separately.

## Sources

- <https://model-spec.openai.com/2026-10-29.html#chain_of_command>
- <https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html>
- <https://docs.langchain.com/oss/python/concepts/memory>
