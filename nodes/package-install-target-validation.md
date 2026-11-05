---
id: package-install-target-validation
title: "Package-Install Target Validation"
summary: "Package-install target validation restricts user-controlled installation selectors to the intended package and release rather than letting a package manager reinterpret them as alternate code sources or options."
type: concept
tags: [software/security]
prereqs: [tool-call-execution-contract, process]
sources: ["https://pip.pypa.io/en/stable/cli/pip_install/", "https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Package-Install Target Validation

## Meaning

An installer input is not necessarily a version number just because a field is called `version`. Package managers accept rich selectors: names, version constraints, local directories, archives and remote source locations. Target validation constrains that language to the application's actual intended operation before the installer is invoked.

## Mechanism

A [[tool-call-execution-contract]] separates proposed arguments from execution authority. Avoid a shell and pass a deliberate argument vector, but do not mistake shell avoidance for validation of the called program's own grammar. A package manager can interpret one argument as a different source without any shell metacharacter being evaluated. pip's documentation explicitly lists URL, directory, file and requirement-specifier handling.

If the feature is “upgrade this application to an approved release,” keep the application package name and trusted repository policy fixed in code. Accept a bounded release identifier under a deliberately narrow parser or approved-release lookup, then construct the requirement from those trusted components. Reject unsupported URLs, paths, options and compound requirements before launching any [[process]]. A restricted application grammar need not accept every version form supported by the package ecosystem.

Installing source distributions or dependencies can execute build code under the installer's identity. Therefore also constrain privileges, repository configuration and artifacts; selector validation alone cannot establish that an approved package is harmless or that a repository is uncompromised.

## One example

A fictional updater accepts only approved releases `2.4.1` and `2.4.2` of a fixed package. Input `2.4.2` becomes that package's pinned requirement. An archive URL or filesystem path is rejected rather than forwarded, even if it contains no shell-special characters. A value beginning with an option marker is also rejected. This is a contract example, not a universal regular expression for Python versions.

## Check your understanding

Does calling an installer with a list of arguments make arbitrary user targets safe? No. The list prevents shell parsing, not alternate meanings in installer arguments. Regression tests should substitute a harmless recorder for the installer and prove that rejected targets never reach it, while approved releases preserve the intended package and source policy.

## Prerequisites

- [[tool-call-execution-contract]]
- [[process]]

## Sources

- <https://pip.pypa.io/en/stable/cli/pip_install/>
- <https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html>
