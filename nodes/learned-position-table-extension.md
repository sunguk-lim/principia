---
id: learned-position-table-extension
title: Learned Position-Table Extension
summary: Learned position-table extension creates valid coordinates beyond a pretrained lookup range while separately adapting and testing long-distance behavior.
type: concept
tags: [ml/llm/architecture]
prereqs: [positional-encoding, fine-tuning]
sources: [https://docs.pytorch.org/docs/2.14/generated/torch.nn.Embedding.html, https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Learned Position-Table Extension

## Meaning

A learned absolute position table stores one trainable vector for each supported position. Extending it changes the position representation and its supported indices; it does not automatically teach the rest of the model to use a longer sequence. This is an adaptation of [[positional-encoding]], not merely an allocation change.

## Mechanism

Let P be an L-by-d table: L supported positions, numbered 0 through L-1, each with d coordinates. A token at position t receives its content vector plus row P[t]. If t is outside the table, ordinary indexed lookup has no valid row. Implementations can reject, truncate, wrap, or explicitly resize; there is no universal rule that random noise silently appears at the first unsupported token.

After resizing to L_new rows, choose an initialization policy. Copying old rows preserves their values but makes repeated coordinates ambiguous until adaptation. Random initialization leaves new rows untrained. Interpolating old rows provides a smooth warm start but changes some previously used coordinates. These are choices, not interchangeable guarantees. [[fine-tuning]] or continued training must expose meaningful long dependencies, not only padded examples or unrelated packed documents. Measure non-padding position exposure and document-boundary masks as well as the nominal training length.

## Worked example

Use three one-dimensional rows P=[2,6,3] and extend to five positions. Map target position j to old coordinate u=j(3-1)/(5-1)=j/2. Between adjacent rows, use their distance-weighted average. Target j=1 maps to u=0.5, giving 0.5×2+0.5×6=4; j=3 maps to 1.5, giving 0.5×6+0.5×3=4.5. The new table is [2,4,6,4.5,3]. All five indices are defined, but index 1 no longer has its old value 6. This explicit policy cannot claim unchanged short-context behavior.

Compare retained-plus-new rows, copied rows, and interpolation under matched training budget and length mixtures. Check short-task regressions, evidence at different depths, distractors, multi-hop use, memory and latency. Rotating queries/keys with scaled coordinates is a different operation from interpolating this learned table. A relative representation being mathematically defined at large positions does not prove useful extrapolation.

A valid position table also leaves attention behavior untested. For a toy fixed-score head, let the relevant key have score 2 and each distractor score 0. With one distractor its normalized weight is e²/(e²+1)≈0.881; with seven distractors it is e²/(e²+7)≈0.514, where e≈2.718 is the exponential base. This follows the attention normalization already supplied by the positional-encoding prerequisites. More keys can change competition even when every position vector is defined. It is not a law that useful weight must fall by this amount: learned scores, masks and content change the result. Probe distant evidence and distractor count separately instead of naming one inevitable failure.

## Check your understanding

Does a valid fifth row prove reliable five-token reasoning? No. Index validity, training exposure and long-distance task behavior are separate properties.

## Prerequisites

- [[positional-encoding]]
- [[fine-tuning]]

## Sources

- <https://docs.pytorch.org/docs/2.14/generated/torch.nn.Embedding.html>
- <https://arxiv.org/abs/1706.03762>
