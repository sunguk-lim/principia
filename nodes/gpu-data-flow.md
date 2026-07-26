---
id: gpu-data-flow
title: GPU Data Flow
summary: GPU data flow is the round trip a piece of work makes between the CPU and the GPU.
type: concept
tags: [gpu]
prereqs: [cuda-kernel, dma]
sources:
  - "etc/linux-internals-complete.html §14 'Data flow' — 'two computers, not master and servant', the host↔device round trip (cudaMalloc / H2D copy / launch / D2H copy), the U-shape figure, and 'Async by default — what this means for your code'"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# GPU Data Flow

## Summary

GPU data flow is the round trip a piece of work makes between the CPU and the GPU. The
right mental model is that these are **two separate computers**, not a boss and a helper:
the CPU (the *host*) and the GPU (the *device*) each have their own processor and their own
memory, joined only by a bus — a set of wires that carries data between them. The CPU
cannot reach into the GPU's memory by hand and the GPU cannot reach into the CPU's, so any
job that runs on the GPU follows a fixed U-shaped path: the CPU **reserves** memory on the
GPU, **copies** the input data across the bus into that GPU memory (host→device, "H2D"),
**launches** a [[cuda-kernel]] to compute on it, the GPU runs the kernel, the results are
**copied back** across the bus (device→host, "D2H"), and only then can the CPU read them.
The single most important and most error-prone fact is that this flow is **asynchronous by
default**: launching the kernel does not wait for it to finish. The CPU only files the
request and immediately moves on; it blocks and waits for the GPU solely when it explicitly
*synchronizes* — which a copy-back implicitly does, because the CPU needs the result. The
two big bulk copies are carried not by the CPU but by [[dma]], so the CPU is free to do
other work while the bytes are in flight.

## Grounded explanation

**What the concept is — two computers with a bus between them.** Picture the CPU and the
GPU not as one machine but as two. The CPU is the general-purpose processor your program
normally runs on, with its own main memory (host RAM). The GPU is a second, separate
processor on a card, with its own separate memory built into that card. The only connection
between them is a *bus* — a physical link of wires (in practice PCIe, the standard expansion
bus inside a computer) over which bytes travel one parcel at a time. The consequence that
makes everything else follow: neither processor can directly touch the other's memory. The
CPU holds an address that names a region of GPU memory, but it cannot *dereference* it —
cannot read or write those bytes directly — because they live across the bus on the other
computer. So you cannot simply "call a function on the GPU" the way you call one in your own
program. Instead the CPU and GPU communicate by leaving data in agreed memory regions and
poking small signal registers — like **mailing letters to a contractor down the street and
getting updates mailed back**, rather than reaching over and doing the work yourself. (The
small "you have new work" signal the CPU writes is informally called *ringing a doorbell*;
the queue the GPU reads its work from is a *ring buffer* it continuously polls. These are
plumbing — the concept is the round trip they implement.)

**The U-shape — the round trip, step by step.** Because the data must physically leave the
host, get computed on the device, and physically come back, every GPU job traces the same
path. Drawn as a letter U, it goes *down* from the host into the GPU and back *up*:

1. **Allocate** on the device. The CPU asks the GPU driver to reserve a block of GPU memory
   (the call is `cudaMalloc`). The GPU sets aside the space and hands back an address naming
   it. That address lives in the CPU's variables, but again it points across the bus, so the
   CPU cannot read it directly — it is only a handle to pass to later steps.
2. **Copy host→device (H2D).** The input data currently sits in host RAM. The CPU asks for
   it to be copied into the GPU memory just allocated (the call is `cudaMemcpy` with a
   host-to-device direction). Crucially, the CPU does **not** carry the bytes itself: it
   programs a copy engine on the card to do it, which is exactly [[dma]] — a dedicated
   piece of hardware that moves a bulk block of bytes directly between the two memories
   across the bus while the CPU is uninvolved. After this step the input exists in *two*
   places: still in host RAM, and now also in GPU memory.
3. **Launch** the [[cuda-kernel]]. The CPU issues the launch — the `kernel<<<grid, block>>>`
   line that says how many GPU threads to spawn running which kernel function. This does
   *not* run the kernel on the spot. It writes a launch command into the GPU's work queue
   and signals the GPU, then **returns immediately**. This is the asynchronous step,
   discussed below.
4. **The GPU runs the kernel.** Picking the command up from its queue, the GPU spawns the
   threads and computes, each thread handling its own element exactly as the [[cuda-kernel]]
   concept describes. The CPU, meanwhile, is already off doing whatever line of code came
   after the launch. The results land in GPU memory.
5. **Copy device→host (D2H).** The CPU asks for the results to be copied back from GPU
   memory into host RAM — again `cudaMemcpy`, now device-to-host, and again the bytes are
   carried by [[dma]], not by the CPU, this time in the reverse direction across the bus.
6. **Read.** Now the results are in host RAM, the CPU reads them with an ordinary memory
   access — no bus, no GPU involved, just a normal read of its own memory.

The U is literal: the data flows *down* (host RAM → bus → GPU memory → into the GPU's
compute units) and then *up* (GPU memory → bus → host RAM). One round trip per job.

**The key insight — asynchronous by default, and why that matters.** Steps 3 and 4 are the
heart of the concept. When the CPU launches the kernel, it is filing a request, not waiting
for an answer. The launch call returns to your program *before the GPU has computed
anything*. The same is true of the copies: the CPU programs them and they proceed on their
own. All of these requests — copies and launches — are placed onto a **stream**, which is
simply an ordered queue of work for the GPU: items on one stream run on the GPU in the order
submitted, one after another, but they run *there*, on the GPU, while the CPU runs ahead on
its own instructions. The CPU therefore does not block at the launch. It blocks only when it
*synchronizes* — explicitly says "wait here until the GPU has caught up." Reading a result
forces this: a device→host copy of the output cannot complete until the kernel that produced
the output has finished, so step 5 (and the step-6 read that depends on it) is the natural
place the CPU finally waits.

Why is async the default rather than a special optimization? Because the two processors and
the bus are three resources that can all work at once, and making the CPU sit idle waiting
for the GPU would waste two of them. With async-by-default, the CPU can queue the next job,
prepare more input, or run unrelated code; the copy engines ([[dma]]) can stream bytes
across the bus; and the GPU can compute — all overlapping in time. That overlap is what
hides the cost of the bus transfer, which is otherwise pure overhead, and keeps both
computers busy. The danger is the flip side of the same fact: if you forget that the launch
returned early, you will reason about your program as if the GPU work were already done when
it is not. This is a classic timing bug, shown in the worked instance below.

**Worked instance — `torch.add(a, b)` on 1,000,000 elements.** Suppose `a` and `b` are two
arrays of one million floating-point numbers sitting in host RAM, and we want their
element-wise sum `c[i] = a[i] + b[i]`. Trace the round trip with concrete bytes; take the
very first elements `a[0] = 3.0` and `b[0] = 4.0`.

- **Allocate.** Each array is one million 4-byte floats = 4,000,000 bytes. The CPU calls
  `cudaMalloc` three times, reserving three 4,000,000-byte regions of GPU memory — one each
  for `a`, `b`, and the output `c`. The CPU now holds three across-the-bus addresses it
  cannot dereference.
- **H2D copy.** The CPU programs the card's [[dma]] engine to copy `a` and `b` — 8,000,000
  bytes total — from host RAM into the GPU regions. The four bytes encoding `3.0` now exist
  both in host RAM and in GPU memory; likewise `4.0`. The CPU did not touch any of these
  bytes; the copy engine moved them across the bus.
- **Launch.** The CPU issues the [[cuda-kernel]] launch. With a block size of 256 threads,
  covering 1,000,000 elements needs `ceil(1,000,000 / 256) = 3907` blocks, so the launch is
  `add_kernel<<<3907, 256>>>(a, b, c, 1000000)`, spawning `3907 × 256 = 1,000,192` threads
  (the 192 extra threads past the millionth element do nothing, guarded by the kernel's
  `if (i < n)` check). This launch call **returns instantly.** At this exact moment the GPU
  has added *nothing*.
- **GPU computes.** The GPU pulls the launch from its stream and runs it. Thread 0 loads
  `a[0] = 3.0` and `b[0] = 4.0`, adds them to get `7.0`, and writes `7.0` into `c[0]` in GPU
  memory; the other ~1,000,000 threads do likewise for their own indices, in parallel. The
  result `c` now exists in GPU memory only — host RAM's copy of `c` is still uninitialized.
- **D2H copy.** The CPU asks for `c` to be copied back; the [[dma]] engine streams the
  4,000,000 result bytes from GPU memory across the bus into host RAM. This copy cannot
  finish until the kernel that wrote `c` has finished, so requesting it makes the CPU wait
  for the GPU here.
- **Read.** The CPU reads `c[0]` from host RAM and gets `7.0` — an ordinary memory read.

Now the timing bug the async default invites. Suppose you wanted to measure how long the add
takes, and you wrote: record the clock, do the launch, record the clock again, subtract. You
would measure something like **~0 milliseconds** — and conclude, wrongly, that a million
additions are free. The reason is exactly step 3's behavior: the launch returned immediately,
*before* the GPU ran a single addition, so your two clock readings straddle only the time to
*file the request*, not the time to *do the work*. To measure the real cost you must
synchronize — wait for the GPU to actually finish — before the second clock reading. This
single mistake is the most common GPU timing error, and it is a direct consequence of the
defining property of GPU data flow: the launch is a letter mailed to the contractor, not the
work itself.

## Prerequisites

- [[cuda-kernel]]
- [[dma]]

## Sources

- `etc/linux-internals-complete.html`, §14 "Data flow" — the framing "The CPU and GPU are
  two computers, not master and servant" (communicating by writing memory regions and
  ringing doorbell registers, "mailing letters to a contractor"); the eight-phase host↔device
  round trip (`cudaMalloc` allocate, `cudaMemcpy` host→device, kernel launch returning
  immediately, GPU pickup from the ring buffer, compute, completion record, `cudaMemcpy`
  device→host, CPU read); the U-shaped "round trip" figure; and "Async by default — what this
  means for your code" (the launch returns before the GPU does any work; the CPU and GPU run
  in parallel; you wait only at the copy-back / synchronize). The worked numbers
  (`torch.add` on 1,000,000 floats, 4,000,000 bytes per array, block size 256, 3907 blocks,
  `3.0 + 4.0 = 7.0`) are the source's own running example.
