---
id: column-level-privileges
title: "Column-Level Privileges"
summary: "Column-level privileges authorize particular table attributes and operations independently of which rows a caller may access."
type: concept
tags: [databases/security]
prereqs: [sql]
sources: [https://www.postgresql.org/docs/current/ddl-priv.html, https://www.postgresql.org/docs/current/sql-grant.html]
status: explained
created: 2026-11-21
updated: 2026-11-21
---

# Column-Level Privileges

## Meaning

Column-level privileges restrict which table attributes a role may read or modify. A caller can be permitted to read a person's public name without being permitted to read that same row's compensation. The protected dimension is the field, not the subset of rows. [[sql]] expresses the requested columns and the grants.

## Mechanism

PostgreSQL supports column-specific SELECT, INSERT, UPDATE and REFERENCES privileges. A role needs privileges for columns it reads, including columns used in expressions or conditions, not just those printed in the final output. Column privilege is permission to use the column; masking instead transforms a displayed value under a separate policy.

Effective authority includes direct grants, applicable role membership and PUBLIC. A narrow grant does not cancel an existing broad table grant. In particular, revoking one column privilege does not remove access that a table-wide privilege still supplies. Start from the intended effective role and inventory all grant paths rather than treating the last GRANT statement as the complete policy.

## One example

A fictional table has columns employee_id, team and salary. A non-owner analyst role has schema access but no inherited table-wide rights. Grant SELECT(employee_id, team), then compare two requests: selecting employee_id and team succeeds, while selecting salary fails. A SELECT * request also asks for salary and therefore fails rather than automatically projecting only permitted columns. If SELECT on the entire table is later granted through a group, salary becomes readable despite the original narrow grant.

Test the example under the actual application role, not the table owner or an administrative session. Functions, views, exports and service accounts can introduce separate access paths whose execution identity must be reviewed.

## Boundaries and check

Column permission does not restrict which authorized rows appear, establish the user's identity, or prevent inference from other accessible data. Combining it with a row policy requires both mechanisms to be correctly configured; neither is shorthand for the other. Do not treat a hidden UI column or removing a field after fetching it as server-side protection.

Validate reads and writes, expressions, SELECT *, role changes, PUBLIC grants and indirect query paths. Keep source rows and expected failures in test fixtures. An unexplained successful read is a policy defect even if the dashboard omits the field.

**Check:** Does a narrow column grant override a broad table grant? No; effective privileges must be evaluated across all grant paths.

## Sources

- <https://www.postgresql.org/docs/current/ddl-priv.html>
- <https://www.postgresql.org/docs/current/sql-grant.html>
