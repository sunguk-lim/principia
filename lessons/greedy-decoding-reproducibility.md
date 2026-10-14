# Greedy decoding reproducibility

Temperature zero usually means “choose the top-scoring next token,” not “guarantee the same complete response forever.” It removes random sampling. The scores themselves can still change when inputs, model versions, floating-point kernels, device type, batch shape, or server scheduling change.

Imagine two candidate tokens with almost equal scores. A tiny numeric difference switches the first chosen token. The next step now sees a different prefix, so later text may diverge substantially. A random seed cannot restore a model revision or guarantee that every kernel executes in the same order. PyTorch's reproducibility guidance makes this distinction: it separates controlling random-number generators from selecting deterministic algorithms and does not promise identical results across platforms or releases.

To test reproducibility, pin the exact prompt bytes, model weights, tokenizer, decoding parameters, runtime, hardware, numerical precision, and batching conditions. Repeat the same request. Compare token IDs and record the first divergence, not just whether the final paragraphs look similar. If possible, inspect the score gap at that point. Run a fixed single-request test and a production-concurrency test separately.

Exact replay is a stronger requirement than stable meaning. If byte identity matters, use a supported deterministic path and regression-test it after upgrades. Otherwise define an acceptable variability target and evaluate answer quality independently.

**Check:** If a seed is fixed but the tokenizer changes, should identical tokens be expected? Why not?
