---
id: context-parallelism
title: Context Parallelism
summary: Context parallelism splits one single training sample along its sequence (token) dimension across $D$ devices, so a sequence too long to fit on any one device can still be…
type: concept
tags: [ml/llm/training]
prereqs: [ring-attention, all-reduce, gather, online-softmax]
sources: ["NVIDIA Megatron-LM context parallelism documentation"]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Context Parallelism

## Summary

**Context parallelism** splits **one single training sample along its sequence (token)
dimension** across $D$ devices, so a sequence too long to fit on any one device can still
be processed. Each device permanently holds a **contiguous block** of the sample's tokens —
their activations and their keys/values — so per-device memory for those tensors drops
**~linearly** with $D$. This is the exact contrast to data-parallelism, which replicates
the **whole model** on each device and splits the **batch** (a *different sample* per device,
gradients [[all-reduce]]'d): data parallelism helps when you have many samples but the model
fits, and does **nothing** for a single sample that is itself too long. The catch is that
attention is **global** — a token in one device's block must attend to keys/values living on
*other* devices' blocks — and that cross-device attention is exactly [[ring-attention]]: the
key/value blocks circulate around a ring and flash-attention's online softmax folds them
in exactly, so the full sequence is never materialized anywhere. Context parallelism composes
with data-parallelism: you can split the **batch** across some devices and the **sequence**
across others at the same time.

## Grounded explanation

**The problem context parallelism solves — and why data-parallelism cannot.** Suppose you
want to train on sequences of $n = 1{,}000{,}000$ tokens. The model itself fits comfortably on
one device, but the *activations* for one sequence — every layer's intermediate tensors, of
size proportional to $n$ — plus the attention keys and values (the $K, V$ for all $n$ tokens)
do **not** fit on one device. data-parallelism is the wrong tool here. As that node defines
it, data parallelism puts a *full copy of the same model on every device*, gives each device a
*different slice of the batch* (a different sample), and keeps the copies identical by
[[all-reduce]]-ing the gradients. It scales the **batch**, not the sample: ten devices let you
process ten *different* sequences at once, but each device still holds an *entire* sequence by
itself. If even one sequence overflows a device, adding more data-parallel replicas does not
help — every replica still has to fit the whole thing. Data parallelism's failure mode is
precisely "a single sample is too big," and that is the gap context parallelism fills.

**The defining move: split the sequence, not the batch.** Context parallelism keeps **one**
sample and partitions it along the **token axis**. Number the devices $i = 0, 1, \dots, D-1$.
Cut the sequence of $n$ tokens into $D$ contiguous **blocks** of $n/D$ tokens each; device $i$
permanently owns block $i$ — its tokens' activations through every layer, and the keys/values
$(K_i, V_i)$ and queries $Q_i$ for those tokens. Notice the contrast in *what is replicated and
what is split*:

| | what each device holds | what is split across devices |
|---|---|---|
| data-parallelism | the **whole model**; one **whole sample** | the **batch** (different samples) |
| **context parallelism** | the whole model; **one block** of a sample's tokens | the **sequence** (token blocks of *one* sample) |

Because each device now stores only $n/D$ tokens' worth of activations and $K, V$ instead of all
$n$, the per-device memory for those tensors is **~$D\times$ smaller**. That linear drop is the
whole point: it is what lets a million-token sequence live on a cluster when it fits on no single
member of it.

**Why this is not trivial — attention is global.** Most of a transformer's per-token work
(the feed-forward layers, layer norms, the elementwise parts) is **local**: token $t$'s
activation only depends on token $t$, so device $i$ can compute it on its own block with no
communication. Attention is the exception, and it is the reason context parallelism needs a
real mechanism rather than just "slice the tensor." In attention, the output for a query token
is a softmax-weighted sum over **every** key/value in the sequence. A query in device $0$'s
block must be scored against keys that live on devices $1, 2, \dots, D-1$. If you tried to [[gather]]
all $K, V$ onto device $0$ to do this, you would re-materialize the full $n$-token $K, V$ on one
device — destroying the very memory saving you split for. So the cross-device attention has to be
done **without** any device ever holding all the keys/values at once.

**The enabling mechanism: cross-device attention IS [[ring-attention]].** This is exactly the
problem [[ring-attention]] was built for, and context parallelism uses it verbatim as its
attention layer. Recall the [[ring-attention]] schedule: queries stay home (device $i$ never moves
$Q_i$); the key/value blocks travel around a ring $0 \to 1 \to \dots \to D-1 \to 0$. At any
instant a device holds exactly **one** key/value block beyond its own queries. On each of $D$
steps it (1) folds the resident $K, V$ block's scores against its local queries into the
flash-attention running summary $(m, \ell, O)$ — $m$ the largest score so far, $\ell$ the
running softmax denominator, $O$ the running numerator (the [[online-softmax]] state) — and (2) simultaneously sends that block
on and receives the next. After $D$ steps every query has seen every key/value block, and because
flash-attention's online summary can absorb blocks **in any order** (a bigger score triggers
a rebase factor $e^{m_\text{old}-m_\text{new}}$ that is independent of the scores), the result is
**bit-exact** the same as single-device attention. So context parallelism is **exact** training,
not an approximation: it changes only *where the tokens live and when their $K, V$ are folded in*,
never the computed answer. And the [[ring-attention]] memory bound $O(n/D)$ per device is exactly
what keeps the activation/$K, V$ saving intact — no device ever materializes the full sequence.

**Worked instance.** Take a sequence of $n = 1{,}000{,}000$ tokens across $D = 4$ devices, so each
device owns a block of $n/D = 250{,}000$ tokens. Device $0$ owns tokens $0$–$249{,}999$: it holds
their activations and their $(Q_0, K_0, V_0)$. Compare the $K, V$ memory: a single device doing
this sequence alone would store keys and values for all $1{,}000{,}000$ tokens; under context
parallelism device $0$ stores $K, V$ for only $250{,}000$ — a **$4\times$** reduction — and
likewise its layer activations are $4\times$ smaller. The local parts of the forward pass (e.g.
the feed-forward sublayer on its $250{,}000$ tokens) device $0$ computes entirely on its own. The
attention sublayer is where the ring runs. To compute attention for device $0$'s query block $Q_0$,
those queries must be scored against $K, V$ for **all four** blocks, but device $0$ starts holding
only its own $K_0, V_0$. So the [[ring-attention]] schedule executes:

| Round | $K, V$ block resident at device 0 | How it got there |
|------|-----------------------------------|------------------|
| 1 | block 0 (its own) | already local; fold $Q_0$ vs $K_0,V_0$ into $(m,\ell,O)$ |
| 2 | block 1 | received from device 3; block 0 forwarded to device 1 |
| 3 | block 2 | received from device 3 (originated at device 2) |
| 4 | block 3 | received from device 3 (originated at device 3) |

Each round folds one more block's contribution into device $0$'s running summary via
flash-attention's rebase-and-add, with the send/receive overlapped behind the compute. After
$4$ rounds, $Q_0$ has been scored against keys/values for all $1{,}000{,}000$ tokens, device $0$
divides once ($O/\ell$) and emits attention for its $250{,}000$ tokens — identical to what a single
device with the whole sequence would produce. The other three devices ran the same trace in
parallel for their own query blocks. At no instant did any device hold more than $250{,}000$ tokens'
worth of $K, V$, which is exactly why the million-token sequence is trainable on four devices that
could each hold only a quarter of it.

**Composing with data-parallelism — and where it's used.** The two strategies split different
axes, so they stack. With, say, $8$ devices you can form $2$ context-parallel **groups** of $4$:
within each group of $4$, one long sample is sequence-split as above (ring attention inside the
group); across the $2$ groups you run data-parallelism — each group processes a *different*
long sample and the two groups [[all-reduce]] their gradients to stay identical, exactly as the
data-parallelism node prescribes. So you scale the **batch** (more samples, via data
parallelism) **and** the **sequence length** (longer samples, via context parallelism) at the
same time. This is the mechanism behind long-context training in systems such as NVIDIA's
Megatron-LM, whose "context parallelism" feature is precisely this sequence-dimension split with
ring attention as the cross-device attention layer.

## Prerequisites

- [[ring-attention]]
- [[all-reduce]]
- [[gather]]
- [[online-softmax]]

## Sources

- NVIDIA Megatron-LM — *context parallelism* documentation (sequence-dimension split with ring
  attention as the cross-device attention layer)
