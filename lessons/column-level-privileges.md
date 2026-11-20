# Column-Level Privileges

## Meaning

Column-level privileges restrict which table attributes a role may read or modify. A caller can be permitted to read a person's public name without being permitted to read that same row's compensation. The protected dimension is the field, not the subset of rows. [[sql]] expresses the requested columns and the grants.

## Mechanism

PostgreSQL supports column-specific SELECT, INSERT, UPDATE and REFERENCES privileges. A role needs privileges for columns it reads, including columns used in expressions or conditions, not just those printed in the final output. Column privilege is permission to use the column; masking instead transforms a displayed value under a separate policy.

Effective authority includes direct grants, applicable role membership and PUBLIC. A narrow grant does not cancel an existing broad table grant. In particular, revoking one column privilege does not remove access that a table-wide privilege still supplies. Start from the intended effective role and inventory all grant paths rather than treating the last GRANT statement as the complete policy.

## One example

A fictional table has columns employee_id, team and salary. A non-owner analyst role has schema access but no inherited table-wide rights. Grant SELECT(employee_id, team), then compare two requests: selecting employee_id and team succeeds, while selecting salary fails. A SELECT * request also asks for salary and therefore fails rather than automatically projecting only permitted columns. If SELECT on the entire table is later granted through a group, salary becomes readable despite the original narrow grant.

Test the example under the actual application role, not the table owner or an administrative session. Functions, views, exports and service accounts can introduce separate access paths whose execution identity must be reviewed.

## Check your understanding

Does a narrow column grant override a broad table grant? No; effective privileges must be evaluated across all grant paths.
