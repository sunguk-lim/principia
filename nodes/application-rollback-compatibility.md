---
id: application-rollback-compatibility
title: "Application Rollback Compatibility"
summary: "Application rollback compatibility checks whether an earlier executable revision can safely operate on current configuration, schema, permissions and persistent data."
type: concept
tags: [software/reliability]
prereqs: [continuous-integration, transaction]
sources: [https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment]
status: explained
created: 2026-11-21
updated: 2026-11-21
---

# Application Rollback Compatibility

## Meaning

Application rollback restores an earlier executable revision to recover from a faulty release. Its safety depends on the current state that the old code will encounter. Version history makes an earlier artifact identifiable; it does not prove that the artifact can run against today's database, policy or configuration.

## Mechanism

Keep an explicit compatibility contract for executable artifact, configuration, schema and persistent data. Exercise the older artifact against a representative current state in [[continuous-integration]] before relying on it as a recovery target. A staged change can preserve an old field while introducing a replacement, move consumers and only later remove the old field. This preserves a rollback window; deleting the old field immediately can close it.

A committed write is not undone by restarting an older process. [[transaction]] provides all-or-nothing behavior within its stated database boundary; reversing completed business effects requires a separate corrective operation or a separately authorized restore strategy. A restore can also discard valid later writes, so it is not a generic substitute for rolling back code.

## One example

Release A reads a column named amount. Release B introduces amount_minor and writes new records using it. If a migration removes amount before A has stopped being a recovery target, redeploying A fails even though its image remains available. Keeping both representations temporarily helps only if their meaning and synchronization are correct. A test should create data with B, then run the actual A artifact against the resulting schema and verify both reads and permitted writes.

A permission change creates a similar boundary: reverting configuration must not revive a revoked account merely to make an old binary work. Secrets rotated after A's release should remain current and external to the old artifact.

## Boundaries and check

Kubernetes documents that a Deployment rollback restores the Pod template, not every surrounding object or persistent effect. The broader compatibility analysis here is a system-design consequence, not a claim that Kubernetes automatically tests migrations, reverses transactions or restores secrets.

Validate recovery artifact identity, schema and data assumptions, current credentials, authorization and observable service behavior. Mixed old/new instances can coexist during recovery, so test the transition as well as the final old version. When no safe backward path exists, a narrowly scoped forward fix can be preferable.

**Check:** Does retaining yesterday's image guarantee rollback? No; the current environment and persistent state must remain compatible with it.

## Sources

- <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment>
