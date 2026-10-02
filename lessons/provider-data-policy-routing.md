# Provider Data-Policy Routing

## Meaning

A gateway may offer several providers for one model, but they can have different retention, training-use, cache, and logging terms. **Data-policy routing** removes endpoints that violate a declared policy before optimizing price or latency.

## Mechanism

Represent policy at endpoint granularity, not as a blanket property of the model slug. A zero-data-retention request can require a provider whose current endpoint terms permit no post-response storage, while account policy may additionally prohibit training use. An [[api-key-usage-guardrail]] can enforce defaults, and a per-request constraint can narrow them. The effective candidate set is their intersection; [[load-balancing]] chooses only among eligible endpoints. If the set is empty, fail visibly rather than silently relaxing the policy.

The path also includes gateway logs, caches, observability, server tools, and downstream processors. “No training” and “zero retention” are not synonyms, and neither says whether transient processing, abuse monitoring, billing records, or legal holds are in scope. Document those boundaries from current primary terms and a contract where stakes require it.

## Worked example

One model slug has two serving providers. One endpoint satisfies a zero-retention requirement and the other does not. A price-first failover router could switch to the second endpoint during an outage; a policy-first router excludes it and fails visibly if no eligible endpoint remains.

**Understanding check:** Why must retention policy be evaluated per endpoint before failover?
