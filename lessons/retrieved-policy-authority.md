# Retrieved Policy Authority

## Meaning

Retrieved policy authority decides which approved rule governs a specific caller, resource, action and time. A confident model recollection, a relevant passage and the latest-looking document are three kinds of evidence, not interchangeable certificates of authority.

## Mechanism

The application maintains trusted policy identity, scope, effective interval and revision outside generated text. It defines how overlapping rules and exceptions compose, then selects the applicable approved evidence. A document cannot make itself authoritative merely by claiming to be the new policy.

A [[rag-freshness-contract]] distinguishes noticing a revision, publishing searchable evidence and permitting that evidence to be used. Reading rights also differ from governing authority: a user may be allowed to inspect a draft that is not yet effective.

[[prompt-injection]] explains why retrieved text must not automatically become operational instruction. Explicit application delegation can grant a narrow role to approved sources, but formatting alone does not guarantee obedience. Sensitive effects still require trusted execution checks. If the policy state is unavailable or conflicting, follow a declared wait, denial or escalation rule rather than silently relying on learned behavior.

## One example

In an invented expense system, old model examples use a limit of 100 units. Approved revision 8 now uses 75, while a readable draft revision 9 proposes 120. A 90-unit request exceeds the applicable limit by 15. Neither the remembered rule nor the future draft authorizes it.

A useful explanation identifies revision 8 and the discrepancy. The application independently checks the actual action. A model saying “approved” cannot override that check, and quoting the current document is not evidence that the correct transaction occurred.

## Check your understanding

Does a new timestamp settle a policy conflict? No. Establish approved authority, effective scope and current eligibility. Test both permitted and denied effects, stale rules, forged issuer labels, future drafts, missing policy state and changes during long execution. Refusing every request is not a passing policy implementation.
