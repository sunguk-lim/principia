---
id: ring-attention
title: Ring Attention
summary: Ring Attention computes the exact same attention output as flash-attention, but for a sequence so long that its keys and values cannot fit on a single device.
type: concept
tags: [ml/llm/architecture]
prereqs: [flash-attention, all-gather, softmax]
sources: ["Ring Attention with Blockwise Transformers for Near-Infinite Context (Liu, Zaharia, Abbeel, 2023), arXiv:2310.01889"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Ring Attention

## Summary

Ring Attention computes the **exact same** attention output as [[flash-attention]], but for a
sequence so long that its keys and values cannot fit on a single device. It splits the sequence
across $D$ devices, so each device permanently holds only the **queries** for its own block plus,
at any one moment, **one** block of keys/values — memory $O(n/D)$ instead of $O(n)$. The devices
are wired in a **ring**; on each of $D$ steps a device folds its current key/value block into its
[[flash-attention]] running summary while **simultaneously** passing that block to its neighbour
and receiving the next one. After $D$ passes every query has seen every key/value block, and
because [[flash-attention]]'s online summary $(m, \ell, O)$ — which streams the [[softmax]] computation incrementally — can absorb blocks **in any order**, the
result is **bit-exact**. The ring eventually delivers every device's keys/values to every other
device — the same end state as an [[all-gather]] — but as pipelined point-to-point passes that
**overlap with computation**, so the communication latency is hidden behind the math.

## Grounded explanation

**The problem Ring Attention solves.** [[flash-attention]] already makes attention cheap on *one*
device: it streams the keys and values past the queries in tiles, keeps a tiny running summary, and
never builds the full $n \times n$ score matrix, so its memory is $O(n)$ rather than $O(n^2)$. But
$O(n)$ is still linear in the sequence length $n$. When $n$ is large enough — hundreds of thousands
of tokens — even storing the keys and values *once* exceeds a single device's memory. We need to
split the sequence across **$D$** devices. The contribution of Ring Attention is a way to do that
split while keeping the answer *identical* to single-device attention, and while paying almost no
visible communication cost.

**Notation (defined before use).** Let $n$ be the sequence length and $D$ the number of devices.
The sequence is cut into $D$ contiguous **blocks** of $n/D$ tokens each. Device $i$ (for
$i = 0, 1, \dots, D-1$) permanently owns block $i$: it holds that block's **query** vectors $Q_i$,
and the **key/value** vectors $(K_i, V_i)$ for the same tokens. From [[flash-attention]], a
**score** is $q \cdot k / \sqrt{d}$ for a query vector $q$ and key vector $k$; attention output for a
query is the softmax-weighted average of value vectors. The **running summary** that
[[flash-attention]] carries for a query block is the triple $(m, \ell, O)$: $m$ is the largest score
seen so far, $\ell = \sum e^{S - m}$ is the running [[softmax]] denominator, and $O = \sum e^{S - m} V$ is the
running softmax-weighted numerator; the answer at any point is $O / \ell$.

**The central object: queries stay home, key/value blocks circulate.** Device $i$ never moves its
queries $Q_i$. Instead the key/value blocks travel. Picture the devices on a circle, $0 \to 1 \to
\dots \to D-1 \to 0$. At any instant device $i$ holds exactly **one** key/value block in addition to
its own queries. On each step it does two things at once:

1. **Compute.** Run one [[flash-attention]] inner step: take the key/value block currently resident,
   compute its scores against the local queries $Q_i$, and **fold** the result into the running
   summary $(m, \ell, O)$ for $Q_i$ — exactly the rescale-and-add update [[flash-attention]] uses
   when it streams a new tile.
2. **Communicate.** **Send** that key/value block to the next device on the ring and **receive** the
   block coming from the previous device. This is a point-to-point pass, not a global operation.

After $D$ such steps, the block that started at device $j$ has visited every device, so every
device's queries have been scored against every block. Each device then divides $O / \ell$ once and
emits the attention output for its own block.

**Why the answer is exact — the key insight.** This is the load-bearing point, and it is inherited
directly from [[flash-attention]]. The online summary $(m, \ell, O)$ does **not** depend on the
*order* in which blocks arrive. When a block brings a score larger than the current $m$, the carried
$\ell$ and $O$ were measured against the old, smaller reference; [[flash-attention]] corrects them by
multiplying both by $e^{\,m_\text{old} - m_\text{new}}$, a factor that is **independent of the
score**, and then adds the new block's contribution. Because that rebase factor is the same for the
whole carry regardless of which block triggered it, folding blocks in the ring order
$i, i{+}1, i{+}2, \dots$ gives the *identical* $(m, \ell, O)$ as folding them in any other order —
and identical to scoring all $n$ keys at once. No $n \times n$ matrix is ever formed, no device ever
holds all the keys/values, and yet the final $O / \ell$ is **bit-for-bit** the single-device result.
Ring Attention is therefore *exact* attention, not an approximation: it only changes **where** each
key/value block lives and **when** it is folded in.

**Relation to [[all-gather]] — and why the communication is hidden.** Look at the net data movement.
Over the $D$ steps, block $j$ is sent from device $j$ all the way around the ring, so **every**
key/value block eventually reaches **every** device — exactly the end state of an [[all-gather]],
where each process's chunk ends up on all processes. Indeed [[all-gather]] is "gather then
broadcast," and as that node notes, real implementations realise it as a **ring** of
point-to-point passes rather than a literal collect-then-distribute. Ring Attention uses that same
ring pattern. The crucial difference is *what happens between passes*: an [[all-gather]] would
collect all the blocks first and then let you compute; Ring Attention **interleaves** them. While a
device is busy computing the scores for the block it currently holds (the expensive part), the
network is simultaneously shipping the next block in and the current block out. If the time to
compute one block's attention is at least the time to transfer one block — which holds for realistic
model sizes, since attention's arithmetic grows with the block size while a transfer is just moving
the block's bytes — then the communication finishes *before* the compute does, and the device never
waits. The latency that an [[all-gather]] would expose as a separate phase is **overlapped away**.
That overlap, not the data pattern itself, is the win: Ring Attention gets the all-to-all delivery
of an [[all-gather]] essentially for free.

**Worked instance.** Take $D = 4$ devices and a sequence cut into 4 blocks. Follow device $0$,
which owns queries $Q_0$. To make the carry updates concrete, suppose the largest score $Q_0$ gets
against each block is: block 0 → score $2$, block 1 → score $1$, block 2 → score $5$, block 3 →
score $3$ (these are illustrative numbers; only their *relative* sizes drive the rescales). Device
$0$ starts holding its own key/value block 0.

| Round | Block resident at device 0 | Action on the carry $(m,\ell,O)$ | New running max $m$ |
|------|----------------------------|-----------------------------------|----------------------|
| 1 | block 0 (score 2) | initialise: $m=2$, $\ell,O$ from block 0 | 2 |
| 2 | block 1 (score 1) | $1 < 2$, **no rebase**; just add block 1's terms (each weighted $e^{1-2}$) | 2 |
| 3 | block 2 (score 5) | $5 > 2$, **rebase**: multiply carried $\ell,O$ by $e^{\,2-5}=e^{-3}$, then add block 2 | 5 |
| 4 | block 3 (score 3) | $3 < 5$, **no rebase**; add block 3's terms (each weighted $e^{3-5}$) | 5 |

While round 1 computes on block 0, device 0 is already sending block 0 to device 1 and receiving
block 1 from device 3; while round 2 computes on block 1, block 1 is forwarded on and block 2
arrives; and so on. Round 3 is the interesting case: the running max jumps from 2 to 5, so the
[[flash-attention]] rebase multiplies the *entire* accumulated $(\ell, O)$ by $e^{-3}$ before
block 2 is added — the one multiplication that keeps the streamed result exact. After 4 rounds
device 0 has folded all four blocks into $(m, \ell, O)$ with $m = 5$; it divides once, $O / \ell$,
and outputs $Q_0$'s attention — identical to what a single device with all of $K, V$ in memory would
have produced. Each of the four devices ran this same trace in parallel for its own query block, and
no device ever stored more than $n/4$ keys/values at a time.

**Coordinated view.** *Structure*: queries pinned to devices, key/value blocks circulating a ring.
*Algorithm*: $D$ rounds of one [[flash-attention]] fold each, carrying $(m, \ell, O)$ and rebasing
when a bigger score appears. *Substrate*: $D$ devices in a ring, each round's point-to-point
send/receive overlapped with that round's compute so the [[all-gather]]-shaped data delivery costs
no visible time. The same traced element — device 0's carry across rounds 1–4 — ties all three
together.

## Prerequisites

- [[flash-attention]]
- [[all-gather]]
- [[softmax]]

## Sources

- Liu, Zaharia, Abbeel — *Ring Attention with Blockwise Transformers for Near-Infinite Context*
  (2023), arXiv:2310.01889
