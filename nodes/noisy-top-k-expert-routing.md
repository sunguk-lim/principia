---
id: noisy-top-k-expert-routing
title: Noisy Top-k Expert Routing
summary: Noisy top-k expert routing perturbs learned expert scores before sparse selection, enabling stochastic expert exploration while retaining an explicit routing and load-balancing contract.
type: concept
tags: [ml/deep-learning]
prereqs: [mixture-of-experts, normal-distribution]
sources: [https://arxiv.org/html/1701.06538, https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/utils/expert_utils.py]
status: explained
created: 2026-10-27
updated: 2026-10-27
---

# Noisy Top-k Expert Routing

## Meaning

Noisy top-k routing modifies a [[mixture-of-experts]] router: perturb each expert score, keep the largest k perturbed scores, and normalize only those selected scores. It gives initially disfavored experts a chance to receive examples without evaluating every expert. Stochastic exploration is not a guarantee of balanced load or better model quality.

## Mechanism

For a token representation x and expert i, let a_i(x) be its learned clean routing score and sigma_i(x) a positive learned noise scale. Draw an independent epsilon_i from the standard [[normal-distribution]], whose mean is zero and standard deviation is one. Form h_i = a_i(x) + sigma_i(x)*epsilon_i. Select the k largest h_i, replace other entries with negative infinity, then apply the softmax inherited from the mixture. Unselected entries have zero gate weight; selected weights sum to one. The original paper learns input-dependent positive scales; a complete implementation must specify its positivity transformation and any numerical floor.

Noise changes which examples reach which experts, and therefore the training signal they can receive. With k greater than one, the softmax weights of selected experts vary with their scores. Selection boundaries are still discrete, and equal expected exploration does not ensure equal realized load. The original work uses additional load/importance objectives; do not substitute the presence of noise for those controls or assume noise must decline monotonically during learning.

## Worked example

Let three experts have clean scores [2.0, 1.8, 0.2], use k=2 and noise scales [0.5, 0.5, 0.5]. One illustrative standard-normal draw is [-1, 0, 2], producing perturbed scores [1.5, 1.8, 1.2]. Experts 2 and 1 are selected. Their score difference is 0.3, so normalized weights are approximately 0.574 and 0.426; expert 3 gets zero.

A second draw [-2, -1, 3] yields scores [1.0, 1.3, 1.7]. Now experts 3 and 2 are selected, with difference 0.4 and weights about 0.599 and 0.401. Expert 3 received training traffic it would not get under clean top-two selection. This pair of draws illustrates possibility, not a frequency or a balancing proof.

## Validation and alternatives

Declare training and inference behavior separately. Tensor2Tensor's referenced implementation adds noise only during training and uses clean scores at inference; that is an implementation contract, not a law of every sparse model. Compare clean and noisy routing across seeds for task loss, per-expert counts, empty/hot experts, capacity overflow and communication/compute cost. Check exactly k nonzero weights when expected, sums near one, ties, finite scales, extreme scores and deterministic evaluation behavior. Compare auxiliary balancing changes independently from the noise intervention. More experts at fixed k retain expert sparsity but still add router, storage and communication costs.

## Check your understanding

Does Gaussian score noise ensure every expert receives equal work? No. Scores, scales, data, finite samples and capacity policy all matter; load must be measured and controlled.

## Prerequisites

- [[mixture-of-experts]]
- [[normal-distribution]]

## Sources

- [Shazeer et al., Outrageously Large Neural Networks](https://arxiv.org/html/1701.06538), section 2.1 and appendix A: noisy sparse gates and load controls.
- [Tensor2Tensor expert utilities](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/utils/expert_utils.py), `noisy_top_k_gating`: positive learned scales, noise floor and training-only noise.
