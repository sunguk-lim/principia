---
id: gpudirect
title: GPUDirect (P2P/RDMA)
summary: "GPUDirect is an umbrella name for a family of NVIDIA technologies whose single defining idea is this: let a GPU's memory exchange data with another device directly, without first…"
type: concept
tags: [gpu]
prereqs: [nvlink, dma]
sources:
  - "linux-internals-complete.html §14 — Three mechanisms, increasingly direct (CPU-staged copy vs GPUDirect P2P vs NVLink); Cross-node — GPUs in different machines (GPUDirect RDMA); What the CPU still does; What's a NIC, and why InfiniBand specifically; glossary entries GPUDirect / RDMA / InfiniBand"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# GPUDirect (P2P/RDMA)

## Summary

**GPUDirect** is an umbrella name for a family of NVIDIA technologies whose single
defining idea is this: let a GPU's memory exchange data with another device **directly**,
without first copying the bytes into the host computer's main memory and back out again.
The default way to move a block from one GPU to another is a detour — the bytes travel out
of the source GPU, up into the CPU's general-purpose memory (host RAM), and then back down
into the destination — two extra copies with the CPU on the critical path of every
transfer. GPUDirect removes that detour. Two members matter. **GPUDirect P2P**
("peer-to-peer") lets one GPU read or write *another GPU's* memory directly — over
[[nvlink]] when the chips are wired with it, so on-node exchanges run at full [[nvlink]]
bandwidth instead of bouncing through the CPU. **GPUDirect RDMA** lets a *network card* read
and write GPU memory directly, so a transfer between GPUs in *different machines* goes
GPU → card → network → card → GPU without ever touching the host RAM of either box. The why
is the same throughput pressure that motivated [[nvlink]]: distributed training exchanges
enormous blocks of numbers on every step, and every byte that detours through host memory
is a byte the CPU must shepherd while the GPU's arithmetic lanes sit idle. GPUDirect deletes
the detour so the exchange runs at the speed of the wire, not the speed of the host.

## Grounded explanation

### The default path, and the detour it forces

Start from what a GPU is and where its data lives. A GPU is a separate chip with its own
fast on-board memory (call it the GPU's memory; the source's name for it is HBM,
"high-bandwidth memory"). The chip itself is a peripheral plugged into the host computer
over a general-purpose expansion bus — the same kind of bus that connects disks and network
cards to the CPU. (Its common name is PCIe; the details belong elsewhere. What matters here
is its role: it links the GPU to the *host*, not GPU to GPU.) The [[nvlink]] node already
told this part of the story — that the ordinary host bus is the slow path, and that
[[nvlink]] is a separate, much wider wire laid *directly between GPUs* to escape it.

Now ask: how does a block of numbers leave one GPU and arrive in another by default? In the
plainest arrangement, the bytes make a round trip through the host. They are copied **out**
of the source GPU's memory, across the bus, **into** the CPU's main memory (host RAM); then
they are copied back **out** of host RAM, across the bus again, **into** the destination
GPU's memory. The source calls this the **CPU-staged copy**: "staged" because the data is
temporarily parked ("staged") in host RAM as an intermediate stop. It is the fallback that
works on any system, but it pays a triple cost — *two* full copies of the data instead of
one move, and the CPU sitting on the critical path of every transfer to drive both halves.
On the source's own numbers this path runs at roughly 32 gigabytes per second.

The detour is pure overhead. The destination GPU does not need the data to *visit* host RAM;
it just needs the data. The visit exists only because the default machinery routes
everything through the host. **GPUDirect is the family of mechanisms that deletes the visit.**

### The defining idea: direct, host-bypassing transfer

The single contribution that names this whole family is **directness** — the bytes move
*straight* from one device's memory to another's, with the host's memory and the CPU's
byte-moving labor cut out of the data path. The word for a device moving memory on its own,
without the CPU copying each byte, is **[[dma]]** (Direct Memory Access): a piece of hardware
is told once "move this region to that address," and its own circuitry does the transfer while
the CPU goes off and does other work. GPUDirect is [[dma]] extended so that the *target* of
the move can be another device's memory — another GPU's, or a network card's — rather than
only host RAM.

A crucial point about what GPUDirect does and does not remove. It removes the CPU from the
**data path** (the moving of the actual bytes), not from **setup**. The CPU still does
one-time configuration work: arranging the address mappings that let one device name
another's memory, registering which memory regions are allowed to be reached directly, and
launching and synchronizing the work. The pattern is exactly the one [[nvlink]] introduced —
the CPU's job shrinks from "move the bytes" to "tell the hardware to move the bytes." Once
that setup is in place, the bytes flow device-to-device with the CPU uninvolved.

### Member 1 — GPUDirect P2P: one GPU reaches into another's memory

**GPUDirect P2P** ("peer-to-peer," meaning the two GPUs deal with each other as equals
rather than both going through a higher authority) is the on-node member. After a one-time
setup call, the source GPU's memory is *mapped into the address space of the other GPU* —
that is, the second GPU is handed addresses that name locations physically living in the
first GPU's memory. From then on, the source GPU's DMA engine can write its bytes **directly**
into the destination GPU's memory; the source's phrasing is blunt — "the host never sees the
bytes."

The transport underneath P2P can be either wire. If the two GPUs are connected by [[nvlink]],
P2P runs over [[nvlink]] and inherits its full bandwidth (around 900 GB/s on the source's
data-center example) — this is the fast, common case in a training server. If there is no
[[nvlink]] between them, P2P can still avoid the host detour by handing the bytes directly
across the general-purpose host bus from one GPU to the other (the source measures this at
roughly 64 GB/s — still about double the staged copy's 32, because it cuts out one of the two
copies). Either way, the defining win is the same: the data does **not** park in host RAM.
The direct-over-[[nvlink]] case is the one that matters for keeping many GPUs fed, because it
combines *both* advantages — no host detour *and* [[nvlink]]'s order-of-magnitude bandwidth.

This is the same hardware behavior [[nvlink]] described from the routing side: a single GPU
instruction that reads an address can land on local memory, on a peer GPU's memory over
[[nvlink]], or on host RAM, with the hardware deciding per-address where the bytes live.
GPUDirect P2P is what makes the "peer GPU's memory over [[nvlink]]" outcome a *direct* one —
the read or write completes at the peer without a stop in the host.

### Member 2 — GPUDirect RDMA: the network card reaches into GPU memory

GPUDirect P2P solves the *within-one-machine* case. But the largest jobs span many separate
machines (the source's example: a thousand GPUs across roughly a hundred and twenty-five
servers), and [[nvlink]] does not reach between boxes — crossing machines needs a network.
The piece of hardware that connects a computer to a network is a **NIC** (Network Interface
Card) — itself a card on the host bus with a port for a network cable. GPU clusters use a
particular kind of high-speed networking fabric called **InfiniBand**, whose card is built
for **RDMA** — *Remote Direct Memory Access*, a networking capability where a NIC reads or
writes *another machine's* memory directly, without involving that machine's CPU. ("Remote"
= the memory is in a different computer; the rest is the same direct-DMA idea as above,
carried over a network.)

**GPUDirect RDMA** is the marriage of those two: it lets the InfiniBand NIC's DMA reach
directly into *GPU* memory rather than only host RAM. The CPU registers the GPU's memory
regions with the NIC once (setup), and from then on the transfer path is, in the source's own
diagram:

> source GPU's memory → NIC → InfiniBand fabric → NIC → destination GPU's memory

Both CPUs — the sender's and the receiver's — are bypassed for the actual bytes; neither
machine's host RAM is touched. The NIC reads straight from the local GPU's memory onto the
wire, and the remote NIC writes straight into the remote GPU's memory. This network path is
slower than [[nvlink]] (the source quotes InfiniBand around 50 GB/s versus [[nvlink]]'s ~900),
but it is far faster than the alternative of staging through two hosts, and fast enough that
training across many machines stays feasible. The proximity helps: in a typical training
server each GPU has its own NIC sitting right next to it on the host bus, so the
GPU-to-NIC-to-wire hop is short.

### Why this is essential, not a nicety

The justification is the recurring-exchange logic from [[nvlink]], sharpened. Splitting a
large model across many GPUs buys parallel compute but incurs a bill paid *every step*:
gradients (the correction signals each GPU computes, which must be summed across all GPUs and
handed back), activations (intermediate values passed from the GPU holding one part of the
model to the GPU holding the next), and sharded tensors (pieces of one big array spread across
GPUs, gathered when the whole is needed) all have to travel between GPUs constantly. While a
GPU waits for data it does not yet have, its thousands of arithmetic lanes do nothing — and
idle lanes are precisely the throughput the GPU was bought to provide, thrown away.

The CPU-staged detour makes that bill worse in two compounding ways: it *doubles* the bytes
moved (two copies per transfer instead of one move) and it puts the CPU on the critical path
of every single exchange, thousands of times per run. GPUDirect attacks exactly this. By
deleting the host detour it halves the copies and frees the CPU from the byte-moving loop;
by routing the on-node hops over [[nvlink]] it also gets the order-of-magnitude bandwidth.
Together that is the difference between the exchange dominating each training step and the
exchange shrinking to a small fraction of it.

### Worked instance: GPU 0 sends its gradient to GPU 1

Take the smallest non-degenerate case the source supports: two GPUs that must exchange one
gradient. After a training step GPU 0 has computed a gradient — a block of numbers, say **2
gigabytes** — that needs to reach GPU 1 (in a real all-to-all gradient sum every GPU sends to
every other; one directed send is the unit that exchange is built from). Trace the same 2 GB
down each path.

**Without GPUDirect — the CPU-staged copy.** The 2 GB is copied out of GPU 0's memory across
the host bus *into host RAM* (copy #1), then copied out of host RAM across the bus again *into
GPU 1's memory* (copy #2). Two full traversals of 2 GB, with the CPU driving both halves. At
the staged path's ~32 GB/s, each traversal of 2 GB takes about `2 ÷ 32 ≈ 0.063 s = 63 ms`,
and there are two of them — so the move costs on the order of `2 × 63 ≈ 126 ms`, plus the CPU
is occupied the whole time and cannot be doing anything else useful.

**With GPUDirect P2P over [[nvlink]].** GPU 0's DMA engine writes the 2 GB *straight* into
GPU 1's memory over [[nvlink]]. One traversal, no host RAM, no CPU on the data path. At
[[nvlink]]'s ~900 GB/s that single move of 2 GB takes about `2 ÷ 900 ≈ 0.0022 s ≈ 2.2 ms`.
Compared to the ~126 ms staged path, the transfer is now roughly **50× faster** *and* the CPU
is free — and the gap comes from *both* effects at once: one copy instead of two, and the
[[nvlink]] wire instead of the host bus. (If these two GPUs had *no* [[nvlink]], P2P would
still help by going direct across the host bus at ~64 GB/s — `2 ÷ 64 ≈ 31 ms`, about 4×
better than the staged 126 ms — just without the bandwidth bonus.)

**Across machines — GPUDirect RDMA.** Now suppose GPU 1 lives in a different server. There is
no [[nvlink]] between the boxes, so the bytes must cross the network. With RDMA, GPU 0's NIC
DMAs the 2 GB straight off GPU 0's memory onto the InfiniBand wire; the remote NIC writes it
straight into GPU 1's memory — neither host RAM is touched, neither CPU moves a byte. At
InfiniBand's ~50 GB/s the move is about `2 ÷ 50 = 0.04 s = 40 ms`: slower than the on-node
[[nvlink]] case, but it carried the data to *another machine* without the quadruple cost a
naive cross-node path would pay (GPU 0 → host RAM A → wire → host RAM B → GPU 1).

### The takeaway

The default way to move data off a GPU detours it through the host computer's memory under
the CPU's supervision — two extra copies on the critical path of every transfer. GPUDirect is
the family of technologies that deletes that detour: **P2P** lets one GPU's DMA write straight
into a peer GPU's memory (over [[nvlink]] at full bandwidth when present), and **RDMA** lets a
network card DMA straight between GPU memories in different machines. The CPU keeps only the
one-time setup; the bytes flow device-to-device. Because distributed training pays a huge
inter-GPU exchange bill on every step, removing the host detour — and pairing the on-node hops
with [[nvlink]]'s bandwidth — is what keeps the arithmetic lanes fed instead of idling on the
wire.

## Prerequisites

- [[nvlink]]
- [[dma]]

## Sources

- linux-internals-complete.html §14, *Three mechanisms, increasingly direct* — the CPU-staged copy (HBM → PCIe → host RAM → PCIe → HBM, ~32 GB/s) versus GPUDirect P2P (HBM → PCIe peer-to-peer → HBM, ~64 GB/s, "the host never sees the bytes," GPU A's memory mapped into GPU B's address space and written by A's DMA engine) versus NVLink (~900 GB/s); *Cross-node — GPUs in different machines* — GPUDirect RDMA, the NIC reading/writing GPU HBM directly (GPU A → NIC → InfiniBand → NIC → GPU B), CPU one-time setup then bulk transfers without touching host RAM, InfiniBand ~50 GB/s; *What the CPU still does* — setup/coordination/dispatch, "the CPU's role shifts from moving bytes to telling hardware to move bytes"; *What's a NIC, and why InfiniBand specifically* — NIC and InfiniBand HCA definitions, per-GPU NIC proximity; glossary entries *GPUDirect* (umbrella; P2P via PCIe peer-to-peer DMA, RDMA via NIC into HBM, both bypassing CPU memory and the syscall path), *RDMA* (NIC reads/writes another machine's memory without its CPU), *InfiniBand* (~50 GB/s fabric, standard substrate for cross-node GPUDirect RDMA), *DMA* (device moves memory without the CPU copying each byte).
