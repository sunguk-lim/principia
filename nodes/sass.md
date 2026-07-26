---
id: sass
title: SASS (GPU Machine Code)
summary: SASS (Streaming ASSembler) is the actual machine code a GPU runs — the real, binary instructions that the streaming-multiprocessors (the GPU's arithmetic cores, abbreviated SMs)…
type: concept
tags: [gpu]
prereqs: [ptx, streaming-multiprocessor, compute-capability, fma]
sources: [linux-internals-complete]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# SASS (GPU Machine Code)

## Summary

SASS (Streaming ASSembler) is the actual machine code a GPU runs — the real, binary instructions that the [[streaming-multiprocessor]]s (the GPU's arithmetic cores, abbreviated SMs) decode and execute directly. It is the final, concrete form that the portable virtual instruction set [[ptx]] is compiled *down* to. Unlike [[ptx]], which is architecture-independent and forward-compatible, SASS is tied to one specific GPU architecture (NVIDIA labels these by [[compute-capability]], e.g. `sm_80` for the Ampere generation, `sm_90` for Hopper): the SASS for `sm_90` is a different instruction set, with different encodings, from the SASS for `sm_80`, and is not portable between them. SASS is where the abstractions of [[ptx]] become physical reality — concrete machine instructions, an actual fixed set of hardware registers, and real memory operations — so reading SASS is the only way to see what the hardware truly executes.

## Grounded explanation

**What SASS is — the defining structure.** [[ptx]] is the architecture-independent virtual instruction set a kernel is compiled to, which the driver can compile down to machine code. SASS is *that machine code*: the concrete instructions a real GPU chip understands. The word is NVIDIA's, short for "Streaming ASSembler," referring to the assembly language of the [[streaming-multiprocessor]]s — the GPU's parallel arithmetic units, which are the engines that actually run a kernel. Where [[ptx]] is a *virtual* set of operations — an idealized, portable description that no chip executes literally — SASS is the *real* set of operations: each SASS instruction corresponds to something the silicon physically decodes and carries out. In the worked GPU pipeline this is the lowest level; everything above it (the library file on disk, its sections, the per-architecture binaries packaged inside) is just packaging that routes the correct block of SASS to the correct GPU.

**Why SASS exists, and why it differs from [[ptx]].** [[ptx]] is deliberately abstract so that one compiled kernel keeps working on GPUs released years apart: it describes the computation in terms that do not commit to any one chip's instruction encodings, register count, or special-purpose hardware units. But no chip executes [[ptx]] directly — the silicon only understands its own native instructions. So [[ptx]] must, at some point, be turned into concrete instructions for the *specific* chip about to run it. That concrete form is SASS, and it is necessarily architecture-specific: each GPU generation — identified by its [[compute-capability]] — adds, removes, or re-encodes instructions and exposes different hardware (for example, newer generations expose more capable matrix-multiply units). A portable description cannot name those generation-specific instructions; only SASS, compiled for one named architecture, can. This is the precise division of labor: [[ptx]] buys *portability across time*, and SASS buys *executability on one chip* — you cannot have both in a single artifact, which is why both exist.

**The two paths from [[ptx]] to SASS.** There are exactly two ways the lowering happens, and they differ only in *when* it runs. (1) *Ahead of time:* a tool called `ptxas` — the "PTX assembler" — takes [[ptx]] plus a chosen target architecture and emits the SASS for it, packaged into a binary file (a "cubin," for *CUDA binary*) that holds the machine code for that one architecture. This happens at build time, so a finished program can ship with SASS already prepared for the architectures it expects. (2) *At load time:* if a program reaches a GPU whose architecture has no matching prebuilt SASS, the driver performs the lowering itself — "just-in-time" (JIT) compilation — running the same kind of [[ptx]]-to-SASS translation on the spot for the chip in hand. The JIT result is cached on disk so later runs skip the compile. Either path produces the identical kind of output: SASS for one specific architecture. The first trades a longer build for an instant first launch; the second trades a slow first launch for the ability to run on a chip that did not exist when the program was built — which is exactly the forward-compatibility that keeping [[ptx]] around provides.

**What appears at the SASS level that [[ptx]] hides.** Because SASS is the real instruction stream, it exposes things [[ptx]] abstracts away. The most important are the *actual* hardware instructions — the named operations the chip provides for one architecture — and the *actual* register allocation, meaning the finite, numbered hardware registers (fast on-chip storage slots, written `R0`, `R1`, …) that the compiler has assigned to hold the kernel's values. A few concrete instruction names from a Hopper (`sm_90`) kernel make this tangible: `FFMA` is a 32-bit floating-point [[fma]] (fused multiply-add: compute `a*b+c` as one rounding step); `HMMA` is a tensor-core matrix-multiply-accumulate instruction (a single instruction that multiplies two small matrix tiles and accumulates the result, the workhorse of deep-learning matmuls); `LDG` and `STG` are global load and global store (read from and write to the GPU's main memory). None of these specific instruction names is part of [[ptx]] — [[ptx]] phrases the same intent in its own portable vocabulary, and the choice of which real instruction to emit, and into which registers, is made only when the SASS is produced.

**Why this is the level you inspect for performance.** Since SASS is what physically runs, it is where real performance behavior becomes visible — which exact instructions were chosen, how many registers each thread consumes, whether an expensive operation became one fast hardware instruction or several. [[ptx]] cannot tell you this, because the decisions that determine it are made *below* [[ptx]], during the lowering. The tool `cuobjdump` with its `-sass` option disassembles a cubin and prints the SASS, so `cuobjdump -sass mykernel.cubin` is how you read the instructions the GPU actually executes — the ground truth beneath the [[ptx]] abstraction.

**Worked instance.** Take a kernel that, among other work, computes a floating-point multiply-add and a tensor-core matrix tile. In [[ptx]] the multiply-add appears as a portable `mad` (multiply-add) operation on virtual operands, and the matrix tile appears as a portable tensor operation — neither names any real hardware. Lowering for Hopper (`sm_90`), whether by `ptxas` ahead of time or by the driver's JIT at load time, turns the [[ptx]] `mad` into the concrete `sm_90` instruction `FFMA` writing into specific allocated registers, and turns the [[ptx]] tensor tile into the concrete `HMMA` instruction — for example, a 16×8×16 tile multiply taking FP16 inputs and accumulating in FP32, with its operands pinned to particular registers such as `HMMA.16816.F32 R12, R8, R10, R12`. Compile the *same* [[ptx]] for Ampere (`sm_80`) instead and you would get the `sm_80` SASS encodings of those operations — different machine code for the same computation, which is exactly why SASS is not portable while the [[ptx]] it came from is. Running `cuobjdump -sass` on the resulting `sm_90` cubin prints precisely these `FFMA` and `HMMA` lines, letting you confirm that the abstract [[ptx]] `mad` did become one `FFMA`, and read off how many registers the kernel ended up using.

## Prerequisites

- [[ptx]]
- [[streaming-multiprocessor]]
- [[compute-capability]]
- [[fma]]

## Sources

- linux-internals-complete.html §17 (Compilation pipeline / "nvcc, PTX, SASS"; "Anatomy of an installed kernel — from wheel to SASS," Level 5 raw SASS; glossary entries for SASS, ptxas, cubin)
</content>
</invoke>
