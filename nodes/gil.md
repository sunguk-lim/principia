---
id: gil
title: Global Interpreter Lock
summary: In the default CPython build, the Global Interpreter Lock permits only one thread at a time to execute Python bytecode; optional free-threaded builds remove that global serialization and replace its safety role with finer-grained mechanisms.
type: concept
tags: [os/process]
prereqs: [thread]
sources:
  - https://docs.python.org/3/howto/free-threading-python.html
  - https://peps.python.org/pep-0703/
  - linux-internals-complete.html ("The GIL — why Python threads don't run in parallel"; "One lock, and everything else follows from it")
status: explained
created: 2026-06-23
updated: 2026-09-12
---

# Global Interpreter Lock

## Summary

The **Global Interpreter Lock (GIL)** is a process-wide lock used by the default build of CPython, the most common Python implementation. A [[thread]] must hold it while executing Python bytecode, so two [[thread]]s in the same interpreter cannot execute that bytecode simultaneously on different CPU cores. They can still overlap waiting for input/output, and compiled extensions can release the GIL while doing work that does not need Python objects.

The qualifier **default build** matters. Since CPython 3.13, Python also supports an optional **free-threaded build** in which the GIL can be disabled. Python 3.14 made that build officially supported; it did not remove the GIL from every Python installation. A program therefore has to distinguish the interpreter version from its build mode and runtime state.

## Grounded explanation

### What the lock serializes

Each [[thread]] has its own execution position and stack, but [[thread]]s in one process share Python objects and interpreter state. In a GIL-enabled CPython interpreter, a [[thread]] acquires the GIL before the interpreter advances it through Python bytecode. Another [[thread]] can exist and be runnable, yet it must wait until the current holder releases the lock before it can execute Python bytecode.

This protects broad regions of interpreter bookkeeping with one coarse coordination mechanism. CPython historically relied heavily on reference counts: shared integers attached to objects that change as references are created and destroyed. Serializing bytecode execution made many such internal updates simpler and preserved a fast common single-threaded path. Reference counting is important to the design, but it is not accurate to reduce every GIL decision to one counter operation; extension compatibility, object access, memory management, and interpreter invariants are part of the boundary.

The GIL does **not** make an application's compound operation safe. A statement that reads shared state, computes a value, and writes it back can interleave with another [[thread]]. Code needing an invariant across several operations must still use explicit synchronization. Nor should code depend on one Python operation remaining atomic across interpreter versions or build modes.

### Why threads can still help

The lock controls execution that needs the GIL, not every activity of the operating-system [[thread]]. CPython releases it around many blocking input/output operations. While one [[thread]] waits for a socket or file, another can execute Python code. A compiled numerical extension may also release the GIL around a kernel that does not touch Python objects, allowing several native computations to run in parallel.

The practical question is therefore workload-specific:

- Pure Python CPU work in a GIL-enabled interpreter is serialized at the bytecode boundary and usually does not gain multicore throughput from more [[thread]]s.
- Input/output-heavy work can improve because waits overlap.
- Native extensions can run in parallel when they deliberately release the GIL.
- Separate processes or isolated interpreters can provide parallel execution with different communication and isolation costs.
- A free-threaded CPython build can execute Python [[thread]]s in parallel, but only compatible code and extensions preserve that mode.

### Free-threaded CPython

PEP 703 introduced a CPython build configuration that can run with the GIL disabled. Official macOS and Windows installers have offered optional free-threaded binaries since Python 3.13, and Python 3.14 classifies free-threaded Python as officially supported. The ordinary GIL-enabled build remains available and remains distinct.

Removing one global lock does not remove the need for synchronization. Free-threaded CPython uses mechanisms such as internal locks for built-in containers, revised reference counting, object immortalization, and a different allocator strategy to protect interpreter state. These mechanisms change performance and memory behavior. The Python documentation also warns that concurrent mutation behavior of built-in containers is an implementation description rather than a language-level guarantee; application invariants should use explicit locks.

A free-threaded process can have the GIL enabled again at runtime. Importing a C extension that has not declared free-threading support may enable it automatically. Check the actual process with `sys._is_gil_enabled()`; do not infer the state from `3.14` in the version string alone.

### Worked instance: identify the real execution mode

Suppose a CPU-bound pure-Python function takes 8 seconds once, and four independent calls must run on a four-core machine.

1. **Default GIL-enabled build:** four [[thread]]s share one GIL. Their bytecode execution takes turns, so an ideal 2-second result is impossible; the run stays near the single-core total and may add scheduling overhead.
2. **Free-threaded build with compatible dependencies:** the four [[thread]]s may execute Python bytecode on four cores. A 2-second result is only a ceiling: shared-data contention, memory bandwidth, allocation, and load imbalance can make it slower.
3. **Free-threaded build importing an incompatible extension:** the extension can re-enable the GIL. The process then behaves like case 1 for GIL-bound Python execution despite using a free-threaded binary.

Validate the choice instead of relying on labels: check the runtime GIL state, run the representative workload at one, two, and four [[thread]]s, verify output correctness under concurrent access, and record throughput, latency, CPU utilization, memory use, and extension compatibility. That experiment separates “threads exist” from “Python bytecode actually ran in parallel.”

## Prerequisites

- [[thread]]

## Sources

- [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html): free-threaded builds began in 3.13; runtime detection; extension-triggered GIL re-enabling; built-in-container locking; known performance and memory limitations.
- [PEP 703 — Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/): the optional build design, interpreter-safety mechanisms, compatibility considerations, and rollout rationale.
- `linux-internals-complete.html` — sections “The GIL — why Python threads don't run in parallel” and “One lock, and everything else follows from it”: the GIL-enabled execution model, input/output release behavior, and process alternative.
