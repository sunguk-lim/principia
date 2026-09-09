---
id: path-environment-variable
title: PATH Environment Variable
summary: PATH is an ordered list of directories that command lookup searches when a process is asked to execute a command name without an explicit path.
type: concept
tags: [os/process]
prereqs: [process, interpreter]
sources: [https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# PATH Environment Variable

## Summary

`PATH` is an environment variable containing an ordered search path for executable commands. It affects command discovery; it does not install Python or another program.

## Grounded explanation

On POSIX systems, an environment is inherited by a new [[process]] as name–value strings. When a shell-like [[interpreter]] receives a command name without a slash, it searches the directories listed in `PATH` according to its command-resolution rules. The first acceptable match determines which executable runs.

Adding a directory to `PATH` changes discoverability:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Prepending gives that directory precedence; appending preserves precedence of existing directories. This distinction matters when several Python installations expose commands with the same name.

An interactive change affects the current process and descendants. Persistence requires editing the startup configuration actually read by the user’s shell or operating environment. Before changing it, inspect the current value, command resolution, active shell, and installation location. Merge with the existing value rather than replacing it.

Search order is a security boundary. A writable or untrusted directory placed early can shadow trusted commands. Empty entries and the current directory have platform-specific risk and should not be introduced accidentally. Prefer explicit absolute paths in privileged automation and avoid adding broad directories solely to fix one command.

Verify with the platform’s command-resolution tool, then run the executable’s version command and inspect its resolved path. A successful import may still use a different interpreter or environment, so verify both executable identity and package environment.

## Prerequisites

- [[process]]
- [[interpreter]]

## Sources

- [POSIX.1-2024, “Environment Variables”](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html): defines process environments and the standard `PATH` variable used by utilities.
