---
id: sandboxed-code-execution
title: Sandboxed Code Execution
summary: Sandboxed code execution runs an untrusted program inside an externally enforced boundary that limits what it can see, call, consume, and reach, then returns only bounded outputs.
type: concept
tags: [ml/agents]
prereqs: [namespace, cgroup, seccomp, capabilities]
sources: [https://man7.org/linux/man-pages/man7/namespaces.7.html, https://docs.kernel.org/admin-guide/cgroup-v2.html, https://man7.org/linux/man-pages/man2/seccomp.2.html, https://man7.org/linux/man-pages/man7/capabilities.7.html, https://firecracker-microvm.github.io/]
status: explained
created: 2026-09-21
updated: 2026-09-21
---

# Sandboxed Code Execution

## Summary

**Sandboxed code execution** runs a program that is not trusted to obey policy inside a boundary controlled by a trusted supervisor. The supervisor supplies explicit inputs, limits what the program can see and do, caps its resource use, and returns only bounded outputs. This preserves code's useful loops, variables, and data transformations without granting the generated program the host process's ambient files, network, credentials, or lifetime.

The key is external enforcement. A prompt that says “do not access the network,” a language-level import block, or a timeout implemented inside the untrusted program is not a sandbox: the same code being restricted can ignore or evade it. A real sandbox places controls in the operating system or a separate virtual-machine boundary that the guest cannot remove.

## Grounded explanation

### Why code needs a different boundary than one tool call

A schema-constrained tool call selects one operation whose arguments can be validated before dispatch. General code instead describes a sequence of operations: it can branch, loop, allocate memory, create child processes, open files, and issue network requests. That larger action space is useful when one program can replace many dependent round trips, but it also means validation cannot enumerate every future action from the source text alone.

Sandboxing changes the question from “can we prove this program is harmless?” to “what effects remain possible even if this program is hostile?” The answer is a composition of independent controls:

1. A [[namespace]] restricts **visibility**. Fresh process, mount, and network namespaces can hide host processes, expose only a chosen filesystem view, and start with no route to external networks.
2. A [[cgroup]] restricts **quantity**. CPU, memory, process count, and I/O limits prevent an infinite loop, allocation storm, or fork bomb from monopolizing the host.
3. [[seccomp]] restricts the **system-call vocabulary**. An allowlist can prevent the program from reaching kernel operations its workload does not require, even after the interpreter itself is compromised.
4. [[capabilities]] restrict privileged **powers**. Dropping unnecessary capability bits keeps a nominally privileged identity from mounting filesystems, changing ownership, opening raw sockets, or performing unrelated administrative actions.

These controls are orthogonal. A private filesystem view does not stop CPU exhaustion; a memory cap does not stop network access; a syscall filter does not decide which remote service may receive data; and a container that shares the host kernel is not automatically safe merely because it is called a container. The supervisor must choose and verify every boundary required by the threat model.

### The trusted supervisor and the capability channel

The supervisor remains outside the sandbox and owns the lifecycle. It creates an immutable runtime image, mounts a small read-only input area plus disposable scratch space, applies the four restrictions, starts the program, enforces a wall-clock deadline, captures bounded standard output and error, and destroys the environment afterward. Because the deadline is enforced from outside, an infinite loop cannot cancel its own termination.

Network access is denied by default. If the task needs an external service, the program receives a narrow brokered operation rather than a general network and a reusable secret. The broker checks the destination, operation, arguments, and response size, authenticates outside the sandbox, and records the request. Thus the sandbox holds a limited capability—“read this object” or “query this approved endpoint”—instead of the credential from which many capabilities could be derived.

Dependencies follow the same rule. The runtime image contains pinned, reviewed packages; untrusted code cannot install arbitrary packages at run time. This separates the program's logic from the authority to change its execution base and avoids turning package installation into an unbounded network and supply-chain channel.

For mutually distrustful tenants or a threat model that includes host-kernel exploits, a separate guest-kernel boundary can be appropriate. A microVM places a virtual-machine barrier between guest code and the host while still requiring resource limits, network policy, credential brokerage, lifecycle control, and output bounds. Stronger isolation changes the boundary; it does not eliminate the need to define capabilities.

### Worked instance: bounded price comparison

Suppose an agent must compare four local price files. Each file contains at most 2 MB of JSON, and the required output is one 20-row table. The supervisor gives the sandbox:

- a read-only `/input` directory containing exactly the four files;
- an empty 16 MB scratch directory;
- one CPU, 128 MB of memory, at most 16 processes, and a 5-second wall-clock deadline;
- no network interface or reusable credential;
- an allowlist of the system calls needed by the interpreter to read, allocate, write, and exit;
- a 64 KB combined output limit.

**Normal branch.** The generated program reads the four files, normalizes currencies using conversion values already supplied as input, sorts the rows, prints the cheapest 20, and exits. The supervisor returns the captured table and deletes the scratch directory. Code was valuable because the loop and sort happened in one execution, but its authority never exceeded the explicit files and output channel.

**Resource-failure branch.** A bug enters an infinite loop while allocating memory. The [[cgroup]] reaches 128 MB and prevents further growth; independently, the supervisor's external timer reaches 5 seconds and terminates the remaining [[process]]. The host keeps its memory and CPU, and the run returns a bounded timeout failure rather than hanging the agent indefinitely.

**Policy-failure branch.** Malicious code tries to read a host credential file and send it to an arbitrary server. The credential file is absent from the sandbox's mount [[namespace]], so the path cannot resolve. Its network [[namespace]] has no external route, and prohibited socket operations are rejected by [[seccomp]]. No secret was injected for the code to recover. The attempt is logged, the run is discarded, and the supervisor exposes no partial result.

The example shows the invariant a sandbox must preserve: every successful or failed execution remains inside a predeclared envelope of visible objects, callable operations, resource budgets, communication channels, and time.

### What to validate

Test the boundary, not just task success. Run representative workloads and deliberate failures: infinite loops, memory and process exhaustion, oversized output, path traversal, symlink tricks, forbidden system calls, attempts to enumerate host processes, network scans, dependency installation, and credential discovery. Confirm limits from outside the sandbox and verify teardown leaves no reusable state.

Then compare the sandboxed-code approach with schema tools, composite tools, or a restricted workflow language. Measure end-to-end correctness, number of round trips, latency, cost, reproducibility, failure recovery, and audit coverage. Code execution is justified when its control-flow advantage survives these controls and when the residual blast radius matches the task's consequence level—not merely because a benchmark reports fewer turns.

## Prerequisites

- [[namespace]]
- [[cgroup]]
- [[seccomp]]
- [[capabilities]]

## Sources

- Linux `namespaces(7)`: namespace isolation and the resource classes whose views can be separated.
- Linux kernel cgroup v2 documentation: hierarchical process organization and resource-control behavior.
- Linux `seccomp(2)`: syscall filtering, inheritance, strict mode, external termination requirements, and allowlist guidance.
- Linux `capabilities(7)`: decomposition of privileged operations into independently grantable capability bits.
- Firecracker documentation: a separate guest-kernel microVM boundary and an additional host-side jailer as defense in depth.
- The worked instance and validation procedure are independent constructions; no performance claim from the archived newsletter is treated as verified.
