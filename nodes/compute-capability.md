---
id: compute-capability
title: Compute Capability
summary: Compute capability is the version number of an NVIDIA GPU's architecture — a number NVIDIA assigns to each generation of its hardware design, written as a major.minor pair (8.0…
type: concept
tags: [gpu]
prereqs: [cuda-kernel, streaming-multiprocessor]
sources:
  - etc/linux-internals-complete.html — "About compute capability (SM version)", "PTX / SASS / cubin / fatbinary", "Custom CUDA extension — PTX JIT fallback"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Compute Capability

## Summary

Compute capability is the **version number of an NVIDIA GPU's architecture** — a number
NVIDIA assigns to each generation of its hardware design, written as a major.minor pair
(8.0, 9.0, 12.0) or, in the compiler's spelling, `sm_80`, `sm_90`, `sm_120`. That number is
a contract: it says exactly which hardware features and machine instructions a GPU of that
generation has — which numeric formats it can multiply, which generations of specialized
matrix-multiply units it carries, how many registers and threads a block may use, and so on.
The number matters because of one hard consequence for a [[cuda-kernel]]: when you compile a
kernel down to the actual machine code a GPU runs, that machine code is built **for one
specific compute capability and will not run on a different architecture**. So compute
capability is the thing you must *target* when you compile, and the thing you must *match*
when you deploy — get it wrong and your kernel refuses to load on the GPU in front of you.

## Grounded explanation

**What the concept is.** A GPU is not one fixed design that NVIDIA has shipped unchanged for
twenty years; it is a *line* of designs, one new architecture per generation, each with a
codename — Volta, then Ampere, then Hopper, then Blackwell. Compute capability is the formal
*version number* attached to each of these architectures. The numbering has a major part and a
minor part. Ampere (the A100 datacenter chip) is compute capability **8.0**; Hopper (the H100)
is **9.0**; the Blackwell workstation chips are **12.0**. The compiler writes the same number a
different way, gluing the two digits onto the prefix `sm_` (for [[streaming-multiprocessor]],
the GPU's repeated processing unit) — so capability 8.0 is `sm_80`, 9.0 is `sm_90`, 12.0 is
`sm_120`. "Compute capability 8.0," "CC 8.0," and "`sm_80`" are three spellings of the one
idea: *this generation of GPU*.

**What the number actually specifies.** The version is not decoration; it is an exact statement
of what the hardware can do. Two GPUs of different compute capability differ in concrete,
checkable ways: which numeric formats they can compute on (an 8-bit floating-point format that a
newer generation multiplies natively may simply not exist on an older one), which generation of
specialized matrix-multiply units they carry, and the size limits a [[cuda-kernel]] must respect —
how many threads a block may contain, how many fast on-chip registers each thread may claim. A
program written assuming a feature that the target capability does not provide is not "slower" on
the old chip; it is *uncompilable* for it, because the machine has no instruction to express the
operation. The version number is therefore the precise boundary between "the hardware can do this"
and "it cannot."

**Why the number is load-bearing for a kernel — the central consequence.** Recall what a
[[cuda-kernel]] is: a function you write once and launch across a vast grid of threads. But the
GPU does not execute the CUDA C++ source you typed. Before it can run, the kernel function must be
*compiled* into the GPU's own machine code — its native instruction set, the real binary the
silicon executes. Here is the pivotal fact: **each generation of GPU has a different machine
language.** The instructions, their encodings, and which ones exist all change from one compute
capability to the next, exactly because the hardware features change. So the compiled machine code
for a kernel is *specific to one compute capability*. The compiler even forces you to say which one
up front: you compile "for `sm_80`," and what comes out is the architecture-specific binary — the
toolchain calls this finished blob a **cubin** (a "CUDA binary") — that holds the native code for
that one architecture and no other. A cubin built for `sm_80` will not load on a GPU of a different
major architecture; the driver looks at the GPU in the machine, sees its compute capability, and
refuses a cubin that does not match.

**Why it has to be this way (the insight).** One might wish for a single universal GPU binary, the
way an ordinary program can often run on any x86 PC. But GPU instruction sets are *not* held stable
across generations — NVIDIA deliberately reworks them each architecture to expose new units and
formats. That freedom to change the hardware's machine language is what lets each generation be
faster and do new things; the price is that the compiled binary cannot be generation-agnostic.
So the toolchain must target a *concrete* capability when it compiles, and the binary it emits is
welded to that capability. Matching the binary to the device's capability thus stops being a
detail and becomes a real, unavoidable deployment concern: the question "which compute capabilities
might this code ever run on?" must be answered at *build* time, long before the GPU is known.

**The two ways to cover more than one GPU.** Because a single cubin covers a single architecture,
software that must run on several different GPUs needs a plan. There are two, and real CUDA software
uses both at once.

- *Bundle several cubins.* You compile the same [[cuda-kernel]] once *per* target capability and
  pack all the resulting cubins into one container. The toolchain's word for this container is a
  **fatbinary** — literally a fat binary holding many cubins side by side, one for each architecture
  you chose to support. At load time the driver reads the GPU's compute capability and picks the
  matching cubin out of the bundle. This is precise (the code is fully optimized for each
  generation) but it only covers capabilities you *named at build time*, and every extra target
  makes the binary larger.
- *Ship a forward-compatible intermediate.* Alongside (or instead of) the per-architecture cubins,
  the compiler can emit an *architecture-independent* intermediate form — a portable, generation-neutral
  representation of the kernel, conventionally called **PTX**. PTX is not machine code any GPU runs
  directly; it is a stable intermediate that the GPU *driver* can compile the rest of the way — into
  the actual native code (informally **SASS**, the real per-architecture instructions) for whatever
  GPU is present — the first time the kernel is launched. This last-moment compile inside the driver
  is called **JIT** ("just in time"). PTX is the escape hatch for *future* GPUs: a chip whose compute
  capability did not even exist when you compiled has no matching cubin, but the driver can JIT the
  bundled PTX into native code for it on the spot.

**Worked instance — one kernel, three GPUs.** Suppose you have written a vector-add [[cuda-kernel]]
and you compile it for a single target, telling the compiler `-arch=sm_80`. The output is one cubin,
native code for compute capability 8.0. Now consider three machines:

1. An **A100**, which *is* compute capability 8.0. The driver sees CC 8.0, finds the `sm_80` cubin,
   loads it, and the kernel runs. Exact match — no further work.
2. A **V100**, an older Volta chip at compute capability 7.0. The driver sees CC 7.0 and looks for a
   matching cubin; there is none (you only built `sm_80`), and there is no PTX to fall back on, so the
   kernel **fails to load** outright. The binary is simply not for this architecture.
3. An **H100**, compute capability 9.0 — *newer* than what you built for. Again there is no `sm_90`
   cubin. If you had also emitted PTX, the driver would JIT-compile that PTX into fresh `sm_90` native
   code on first launch and the kernel would run (after a one-time compile pause); if you shipped *only*
   the `sm_80` cubin and no PTX, it cannot run here either.

The fix is to decide your coverage at build time. Compiling the same kernel for `sm_70` **and**
`sm_80` **and** `sm_90` produces a fatbinary with three cubins — one each for the V100, A100, and
H100 — so all three machines find an exact native match. Adding PTX to the bundle covers the *next*
generation too, the one you have not heard of yet, by letting its driver JIT from the portable form.
That single decision — which compute capabilities to target, and whether to carry PTX for the rest —
is the whole practical weight of this concept: the kernel's source never changed, but *which GPUs it
can actually run on* was fixed the moment you chose the target capabilities.

## Prerequisites

- [[cuda-kernel]]
- [[streaming-multiprocessor]]

## Sources

- `etc/linux-internals-complete.html` — "About compute capability (SM version)" (the SM-version
  numbering, `sm_90`/`sm_120`, and "kernels compiled for one capability do NOT run on different
  hardware"); the PTX / SASS / cubin / fatbinary definitions ("fatbinary … bundles all your cubins
  together with the original PTX, so the driver can pick whichever cubin matches the current GPU —
  or JIT-compile the PTX if none match"); and the custom-CUDA-extension PTX JIT-fallback note
  (a wheel built for `sm_80;sm_90` run on a newer arch uses embedded PTX to JIT a fresh cubin once).
