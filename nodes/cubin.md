---
id: cubin
title: Cubin and Fatbinary
summary: A cubin (CUDA binary) is the compiled GPU machine code for one specific GPU architecture, packaged in an ELF object file; it runs only on chips of that exact generation.
type: concept
tags: [gpu]
prereqs: [ptx, compute-capability, sass]
sources: [linux-internals-complete.html]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Cubin and Fatbinary

## Summary

A *cubin* (CUDA binary) is the compiled GPU machine code for **one** specific GPU
architecture, packaged in an ELF object file; it runs only on chips of that exact
generation. A *fatbinary* is a container that bundles **several** cubins — one per
targeted architecture — together with the architecture-independent [[ptx]] as a
fallback, and is embedded as a special section inside an ordinary host program or
library. At load time the CUDA runtime selects the cubin that matches the GPU
actually present; if none matches, it falls back to compiling the embedded [[ptx]] on
the spot. This pairing is what lets a single shipped file (for instance a PyTorch
wheel) run unchanged across many GPU generations, including ones that did not exist
when the file was built.

## Grounded explanation

Start from a tension that [[ptx]] already half-resolves. [[ptx]] is the portable
virtual instruction set: a stable, text-form intermediate that the GPU driver can
translate ("JIT", just-in-time, compile) into the real machine code of whatever GPU
is present. That portability has a cost — translating [[ptx]] to machine code takes
time, and it happens on the user's machine on first use. The actual instructions a
GPU executes are **not** portable: each GPU generation has its own native
instruction set (NVIDIA's name for it is [[sass]]), and instructions assembled for one
generation are meaningless on another. A generation is identified by a *[[compute-capability]]*,
a version number NVIDIA assigns to each chip design (written like
`sm_70`, `sm_80`, `sm_90`, where larger numbers are newer). Machine code built for
`sm_80` will not run on `sm_90` hardware and vice versa.

A **cubin is exactly that non-portable machine code, frozen and packaged.** The
build toolchain takes [[ptx]] and runs it through an assembler (NVIDIA's tool is
`ptxas`) aimed at one chosen architecture; the result is the native [[sass]] for that one
architecture, wrapped in an ELF object file. ELF is the standard Unix container
format for compiled code — it carries the raw instruction bytes alongside a symbol
table so that the loader can later look up a routine by name. So a cubin is to a GPU
what a normal compiled `.o`/executable is to a CPU: ready-to-run machine code for one
target, with no translation step left. Its defining property is precisely this
**per-architecture specificity**: one cubin, one compute capability, no portability.

That property creates a shipping problem. You want to distribute **one** artifact,
but native code only ever fits one generation. Two bad extremes bracket the answer.
At one extreme you ship only [[ptx]] and let the driver JIT it everywhere — fully
portable, but every machine pays the translation tax on first run, and a faulty or
slow JIT affects all users. At the other extreme you ship one cubin per generation as
separate downloads — fast everywhere, but the user must somehow pick the right file,
and any GPU generation you did not build for simply cannot run.

The **fatbinary is the structure that takes the good half of each extreme.** It is a
container blob that holds a *set* of cubins — say one for each of the common
architectures you care about — **plus** the original [[ptx]]. Concretely it is stored
as a named section inside the final host binary (the section is called
`.nv_fatbin`), so the GPU code rides along inside the very same `.so` library or
executable that holds the ordinary CPU code calling it; there is still just one file
on disk. The CPU side's job is only to hand the runtime a pointer into this blob and
ask it to launch a named routine.

The payoff is in **how selection works at load time**, and this is the key insight.
When the program first needs a GPU routine, the runtime reads the compute capability
of the GPU physically present, then scans the fatbinary's catalogue of cubins for an
exact match. **If a matching cubin exists, it is used directly** — the SASS is already
native to this chip, so there is nothing to compile and startup is immediate. **If no
cubin matches** — the GPU is newer or simply a generation you did not build for — the
runtime falls back to the embedded [[ptx]] and JIT-compiles it into fresh SASS for
this exact chip, then caches that result on disk so later runs of the program skip
the compile. Precompiled cubins thus serve as a fast path for the generations you
anticipated, while the [[ptx]] is an insurance policy that keeps even unforeseen
future hardware working. This is the whole reason a single wheel survives across GPU
generations: the cubins cover today's chips with no compile cost, and the [[ptx]]
covers tomorrow's.

This also explains a visible side effect: CUDA libraries can be enormous. Every
routine is shipped once per targeted architecture **plus** once as [[ptx]]; if you
target six generations, each routine exists in seven forms inside the `.nv_fatbin`
section, which is why a single vendor math library's GPU-code section can run to
hundreds of megabytes. Size is the price of carrying many ready-to-run cubins instead
of forcing a JIT everywhere.

**A concrete walkthrough.** Suppose a library is built targeting three architectures,
so its fatbinary contains a cubin for `sm_70`, a cubin for `sm_80`, a cubin for
`sm_90`, and the [[ptx]] fallback — four payloads for the routine, all inside the one
`.nv_fatbin` section of the shipped `.so`.

- Loaded on an A100, whose compute capability is `sm_80`: the runtime reads `sm_80`,
  finds the `sm_80` cubin in the catalogue, and launches its SASS directly. No
  compilation happens; the other two cubins and the [[ptx]] sit unused. This is the
  fast, common path — the case the precompiled cubins exist for.
- Loaded on a brand-new chip whose compute capability is `sm_100`: the runtime reads
  `sm_100` and scans the catalogue — `sm_70`, `sm_80`, `sm_90`, none equal to
  `sm_100`. With no matching cubin, it falls back to the embedded [[ptx]],
  JIT-compiles it into `sm_100` SASS, runs that, and caches the freshly built code on
  disk so the next run of the program loads it without recompiling.

Both cases ran the **same shipped file** with no rebuild; the difference is only
whether a matching cubin was found (use it) or not (JIT the [[ptx]]). That is the
contribution of the cubin-and-fatbinary pairing: precompiled native code for speed
where you can predict the target, portable [[ptx]] for reach where you cannot, both
carried inside one ordinary binary.

## Prerequisites

- [[ptx]]
- [[compute-capability]]
- [[sass]]

## Sources

- `etc/linux-internals-complete.html` — §17, CUDA compilation pipeline: cubin (per-arch
  SASS in an ELF file produced by `ptxas`), fatbinary as the container of many cubins
  plus PTX embedded in the `.nv_fatbin` section, compute-capability matching at load
  time with PTX-JIT fallback, and the cubin-lifecycle / "why CUDA binaries are huge"
  discussion.
