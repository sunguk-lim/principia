---
id: row-level-security
title: Row-Level Security
summary: Row-level security applies database-owned predicates to row visibility and writes under a caller role, in addition to ordinary table privileges.
type: concept
tags: [databases/security]
prereqs: [relational-model, sql]
sources: [https://www.postgresql.org/docs/current/ddl-rowsecurity.html]
status: explained
created: 2026-10-24
updated: 2026-10-24
---

# Row-Level Security

## Meaning

Row-level security (RLS) restricts which records a database role can read or modify inside an otherwise accessible table. It moves a row predicate into database enforcement instead of relying on every application query to remember the correct filter. The [[relational-model]] supplies rows and tables; [[sql]] supplies the operations and policies.

## Mechanism

In PostgreSQL, ordinary privileges first determine whether a role may perform an operation on a table. After RLS is enabled, applicable policies determine which rows normal operations can see or change. An enabled table without an applicable policy uses default deny for those normal row operations. Enabling RLS is different from merely defining a policy while leaving enforcement disabled.

A `USING` expression checks existing rows for visibility or modification; `WITH CHECK` checks the proposed new row produced by an insert or update. Separate checks prevent a caller from reading only its own records but rewriting their ownership to cross a boundary. Policies may depend on command and role. Multiple permissive policies combine with OR; restrictive policies impose additional AND conditions. An unexpectedly broad permissive policy can therefore widen access.

## Worked example

A table `notes(owner, body)` contains rows owned by roles `alice` and `bob`. Grant a non-owner application role the required table privileges, enable RLS, and define a policy whose `USING` and `WITH CHECK` expressions both require `owner = current_user`. With Alice's authenticated role active, a query without an owner clause can see Alice's row but not Bob's. Changing Alice's row owner to Bob fails the proposed-row check. An application-provided string saying “Alice” must not establish the database identity.

This example assumes distinct authenticated roles. A pooled service using one shared database role needs a separately secured mapping from verified application identity to policy state, and must reset it between requests. A client-writable tenant setting is not automatically trustworthy. Test actual pooled sessions and administrative paths, not only a policy in isolation.

PostgreSQL superusers and `BYPASSRLS` roles bypass RLS. Table owners normally bypass it unless forced under RLS; forcing does not remove superuser or bypass-role exemptions. Whole-table operations such as TRUNCATE are outside row-policy filtering, and integrity checks can reveal information through errors. Policies consulting other tables also require careful concurrency analysis. RLS is neither column masking nor a complete authorization system for object storage, logs, cached results, or model prompts.

Test reads, inserts, updates, deletes, role inheritance, ownership, pooled identity reuse, revoked access, permissive-policy composition, and error paths. Authorization belongs before data leaves the database; downstream ranking or response filtering cannot undo a disclosed row.

## Check your understanding

Does granting SELECT make RLS irrelevant? No. Normal row visibility still requires applicable policy permission, while privileged bypass paths must be audited separately.

## Prerequisites

- [[relational-model]]
- [[sql]]

## Sources

- <https://www.postgresql.org/docs/current/ddl-rowsecurity.html>
