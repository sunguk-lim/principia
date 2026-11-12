# Authenticated Change Provenance

## Meaning

Change provenance records who performed a change, what changed, when it was observed and how it relates to evidence and approval. Authentication makes the actor attribution stronger than an arbitrary author string, but it does not prove the actor's change was wise, authorized or true.

## Mechanism

At the trusted write boundary, obtain the principal through [[agent-workload-identity]]. Record the requesting user when relevant, operation and attempt IDs, source revision, resulting revision or content digest, evidence references and authorization decision. A [[trace-span]] connects the attempted operation to its effects and failures. Distinguish a human approver from the runtime that executed the approved action.

Store the observed result, not merely a model's declaration of success. An attempted write, a denied write and a committed change are different events. If an acknowledgment is lost, retain the unknown state and reconcile it. A digest can bind the audit record to particular content, but an unprotected log that an attacker can rewrite is not made tamper-resistant by including a hash field.

## One example

An invented worker W proposes revision P8 based on P5. Reviewer R authorizes the exact digest of P8, and service S publishes P9 combining the validated change with current main. The record should retain W as proposer, R as approver, S as executing principal, the base and final revisions, and the publication receipt. A user-entered --as R flag from W must not replace R's authenticated approval. If P8 is edited after approval, the approval no longer describes the new payload.

## Boundaries and check

Set retention, access and redaction rules: provenance can itself expose private data. Trusted timestamps, append controls and protected storage are separate engineering requirements; complete history is not automatically immutable history. Test forged actor labels, shared credentials, missing receipts, changed payloads and cross-project access. W3C provenance supplies a model of entities, activities and agents; the implementation must still establish which assertions are trustworthy.


## Check your understanding

Does an actor label authenticate the actor? No; the trusted boundary must establish identity and bind it to the observed change.
