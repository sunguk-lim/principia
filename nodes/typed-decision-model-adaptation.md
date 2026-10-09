---
id: typed-decision-model-adaptation
title: Typed Decision-Model Adaptation
summary: Typed decision-model adaptation fine-tunes a small model for a bounded answer schema, then evaluates validity, calibration, abstention, and downstream policy against rules and an unadapted baseline.
type: concept
tags: [ml/agents]
prereqs: [lora, decision-score-action-gate, structured-output, model-calibration]
sources: [https://arxiv.org/abs/2106.09685, https://scikit-learn.org/stable/modules/calibration.html]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Typed Decision-Model Adaptation

## Summary

A small language model can be adapted to answer a restricted decision question—such as route, reject, or abstain—but a higher label accuracy or a valid JSON object is not permission to execute an action.

## Grounded explanation

Specify the input state, allowed labels, and [[structured-output]] schema before training. A [[lora]] adapter can adjust a frozen base model with fewer trainable weights; it does not guarantee low runtime memory or better decisions. Separate training, validation, and held-out evaluation by entity, time, or task to prevent near-duplicate leakage. Preserve the base checkpoint and compare it with the adapter, a deterministic rule, and an ordinary classifier under the same examples.

Measure per-class confusion, schema-invalid outputs, abstentions, latency, memory, and [[model-calibration]] of any scores. For a high-cost action, choose a threshold from error costs and check it on held-out data; re-test after model, label, or traffic changes. The [[decision-score-action-gate]] remains application-owned: it performs authorization, amount and eligibility checks, and action reconciliation outside the model. A “yes” prediction should be treated as evidence for the gate, not an instruction.

For example, a support triage model may classify refund requests. A LoRA-trained model could improve in-domain classification while worsening rare fraud or ambiguous cases; one aggregate accuracy would hide that. Test distribution shift and adversarially phrased inputs, then evaluate the actual routed outcomes. Claims that a named small checkpoint rose from 37% to 65% in minutes on 4 GB are source-specific and are not established by this concept.

## Sources

- [Hu et al., LoRA](https://arxiv.org/abs/2106.09685): low-rank adaptation mechanism.
- [scikit-learn calibration guide](https://scikit-learn.org/stable/modules/calibration.html): evaluating predicted scores against observed frequencies.
