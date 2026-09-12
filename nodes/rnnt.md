---
id: rnnt
title: RNN Transducer
summary: An RNN Transducer is a streaming sequence model that combines acoustic frames and prior emitted tokens to assign probabilities to speech transcripts while allowing either a token emission or a time advance at each decoding state.
type: concept
tags: [ml/speech]
prereqs: [neural-network, probability-distribution, softmax]
sources: [https://arxiv.org/abs/1211.3711]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# RNN Transducer

## Summary

An **RNN Transducer (RNN-T)** turns a stream of acoustic frames into tokens without requiring a pre-aligned transcript. At each state it can either emit the next token or emit a blank symbol and advance to the next frame.

## Grounded explanation

An RNN-T has three [[neural-network]] parts. An encoder maps each acoustic frame to a representation of the audio observed so far. A prediction network maps the already emitted token prefix to a representation of linguistic history. A joint network combines the two representations and applies [[softmax]] to produce a [[probability-distribution]] over vocabulary tokens plus a special blank symbol.

A decoding state is a pair `(t, u)`: audio-frame index `t` and transcript-prefix length `u`. If the model selects a vocabulary token, it appends that token and moves to `(t, u + 1)`. If it selects blank, it appends nothing and moves to `(t + 1, u)`. The blank therefore means “consume this frame without emitting a transcript token,” rather than a character in the transcript.

This separation lets an RNN-T stream: it does not need the last audio frame before it can begin predicting. It also permits several tokens to align to one frame, or many frames to pass with no token. Training sums the probabilities of valid paths through this frame/token lattice for the observed transcript, so an external frame-level alignment is unnecessary.

The same state-machine property creates a latency cost. Every blank advances only one frame, and every emitted token requires another state transition before a later blank can advance time. For speech containing silence or long held sounds, many sequential decisions may be blank decisions. The architecture is useful because its streaming behavior and token history are explicit; improving its throughput requires changing how far a transition can advance, not merely making the vocabulary larger.

## Prerequisites

- [[neural-network]]
- [[probability-distribution]]
- [[softmax]]

## Sources

- Graves, “Sequence Transduction with Recurrent Neural Networks” (2012), [arXiv:1211.3711](https://arxiv.org/abs/1211.3711): transducer lattice, blank transitions, and alignment-free sequence training.
