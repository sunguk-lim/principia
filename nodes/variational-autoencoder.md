---
id: variational-autoencoder
title: Variational Autoencoder
summary: A variational autoencoder is a latent-variable generative model whose probabilistic encoder approximates the posterior and whose decoder is trained through a reparameterized evidence lower bound.
type: concept
tags: [ml/deep-learning]
prereqs: [autoencoder, latent-variable-model, variational-inference, reparameterization-trick]
sources: [arxiv:1312.6114]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Variational Autoencoder

## Summary

A **variational autoencoder (VAE)** combines an encoder–decoder [[autoencoder]] shape with a probabilistic [[latent-variable-model]]: the encoder approximates the posterior over latent codes, and both networks train by maximizing a reparameterized variational lower bound.

## Grounded explanation

For observation $x$, the encoder outputs parameters of $q_\phi(z\mid x)$; the decoder defines $p_\theta(x\mid z)$; and a prior $p(z)$ defines valid latent samples. The objective is

$$\mathcal L(x)=E_{q_\phi(z\mid x)}[\log p_\theta(x\mid z)]-D_{KL}(q_\phi(z\mid x)\|p(z)).$$

The first term rewards reconstruction under the decoder. The second comes from [[variational-inference]] and keeps each encoded distribution near the prior, making the latent space sampleable. For a Gaussian encoder, the [[reparameterization-trick]] writes $z=\mu_\phi(x)+\sigma_\phi(x)\epsilon$ so gradients reach encoder parameters.

### Worked example

For one one-dimensional input, suppose the encoder gives $\mu=1.0$, $\sigma=0.5$, and noise draw $\epsilon=-0.4$. Then $z=0.8$. If the decoder's reconstruction log-likelihood is $-0.30$ and the KL term to the unit-normal prior is $0.25$, the ELBO is $-0.30-0.25=-0.55$. Training raises it by improving reconstruction while avoiding an arbitrary, disconnected code distribution.

After training, generation samples $z$ from the prior and decodes it. This distinguishes a VAE from a deterministic [[autoencoder]], which may reconstruct well but has no guarantee that arbitrary latent samples decode to plausible observations. The VAE's compromise can blur reconstructions when the likelihood is simple or the KL pressure overwhelms the decoder; report both terms and sample quality rather than one total alone.

## Prerequisites

- [[autoencoder]]
- [[latent-variable-model]]
- [[variational-inference]]
- [[reparameterization-trick]]

## Sources

- Kingma and Welling, “Auto-Encoding Variational Bayes,” arXiv:1312.6114 — probabilistic encoder, ELBO, and reparameterized training.
