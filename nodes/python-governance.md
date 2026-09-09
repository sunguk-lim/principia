---
id: python-governance
title: Python Language Governance
summary: Python's formal governance assigns broad but constrained project authority to an elected five-person steering council and specifies elections, conflicts, delegation, and accountability mechanisms.
type: concept
tags: [languages/python]
prereqs: [interpreter]
sources: [https://peps.python.org/pep-0013/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Language Governance

## Summary

Python's formal governance is defined by PEP 13. A five-person steering council maintains the language and CPython project's direction while seeking consensus and delegating routine decisions.

## Grounded explanation

The council's mandate includes language and [[interpreter]] quality and stability, sustainable contribution, the core-team relationship with the Python Software Foundation, PEP decision processes, and final appeal when other mechanisms fail.

Its authority includes accepting or rejecting PEPs, maintaining conduct processes, managing project assets with the PSF, and delegation. The authority is constrained: PEP 13 itself has a specified amendment process, core-team membership cannot be changed arbitrarily, conflicts require abstention, and no more than two council members may share one employer.

The core team elects a new council after each feature release. PEP 13 specifies nominations, anonymous scoring, term boundaries, vacancies, and no-confidence votes. The current individuals are mutable and should be checked in the live PEP rather than embedded as a timeless concept.

Governance is not the same as implementation or standardization by fiat. Most technical proposals proceed through public PEP processes, designated decision makers, expert groups, and consensus; the council is intended to use direct power sparingly. When evaluating a claim about Python's direction, verify the relevant PEP status, decision record, release documentation, and supported-version behavior separately.

## Prerequisites

- [[interpreter]]

## Sources

- [PEP 13, “Python Language Governance”](https://peps.python.org/pep-0013/): specifies council composition, mandate, powers, elections, conflicts, terms, core-team role, and accountability mechanisms.
