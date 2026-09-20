# Sandboxed Code Execution

## Meaning

Sandboxed code execution runs an untrusted program inside a boundary enforced by a trusted supervisor. The program receives only explicit inputs and bounded communication channels, so even hostile code cannot inherit all of the host's files, network, credentials, resources, or lifetime.

## Mechanism

A [[namespace]] limits what the program can see, a [[cgroup]] limits how much CPU, memory, I/O, and process count it can consume, [[seccomp]] limits which system calls it can request, and [[capabilities]] remove privileged powers it does not need. An external supervisor applies those controls, enforces a wall-clock deadline and output limit, brokers any approved external operation without injecting reusable credentials, and destroys the environment afterward.

The layers solve different problems. Filesystem isolation does not stop an infinite loop; a CPU cap does not stop data exfiltration; and a syscall filter does not decide which approved service a request may reach. The safety envelope is their composition.

## One example

A price-comparison task receives four read-only JSON files, 128 MB of memory, one CPU, a five-second deadline, no network, and a 64 KB output cap. Correct code reads and sorts the files. An infinite loop is terminated externally, while an attempt to read a host credential fails because the file is outside the mount namespace and no credential was placed inside.

## Check your understanding

**Question:** Why is an instruction such as “do not use the network” not a sandbox?

**Answer:** The untrusted program can ignore that instruction. A sandbox requires an external mechanism that makes forbidden effects unavailable even when the code is malicious.
