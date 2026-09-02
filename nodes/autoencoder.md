---
id: autoencoder
title: Autoencoder
summary: An autoencoder learns an encoder that compresses an input into a code and a decoder that reconstructs the input from that code.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, loss-function]
sources: [https://www.deeplearningbook.org/contents/autoencoders.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Autoencoder

## Summary

An **autoencoder** is a [[neural-network]] trained to reconstruct its input through a constrained intermediate code: an encoder maps input to code, and a decoder maps code back to a reconstruction.

## Grounded explanation

Let encoder $e_\phi$ produce $z=e_\phi(x)$ and decoder $d_\theta$ produce $\hat x=d_\theta(z)$. Training minimizes a reconstruction [[loss-function]] such as

$$\mathcal L(x,\hat x)=\sum_i(x_i-\hat x_i)^2.$$

If the code or architecture is constrained, the network cannot merely copy every input coordinate and must retain structure useful for reconstruction.

### Worked example

For input $x=(1,0)$, suppose a one-number encoder gives $z=0.8$ and the decoder returns $\hat x=(0.9,0.2)$. Squared reconstruction loss is $(1-0.9)^2+(0-0.2)^2=0.05$. Gradient-based training changes both encoder and decoder so examples receive codes that reconstruct with smaller loss.

A deterministic autoencoder maps each input to one code. It does not by itself define a probability distribution over codes or a principled way to sample new data; those are additional properties of a variational autoencoder.

## Prerequisites

- [[neural-network]]
- [[loss-function]]

## Sources

- Goodfellow, Bengio, and Courville, *Deep Learning*, “Autoencoders.”
