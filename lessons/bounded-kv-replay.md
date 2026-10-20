# Bounded KV Replay

## Meaning

Bounded KV replay rebuilds a short recent attention state rather than retaining every local key and value persistently. It trades recomputation for smaller long-lived storage.

## Mechanism

The [[kv-cache]] ordinarily avoids work by retaining attention state. Replay gives back part of that saving, using recent tokens and whatever compatible boundary state the implementation retains. A bounded number of input tokens does not automatically imply exact reconstruction: the [[receptive-field]] of stacked [[transformer-attention]] layers can depend on earlier tokens outside that suffix.

An exact method must supply those dependencies or prove they are unnecessary. A truncated method deliberately changes the dependency boundary and must evaluate the resulting approximation. DeepInfer's deployment Q&A describes approximate missing-window replay that restricts attention to the replayed suffix; it also distinguishes encoder recovery from decoder prefill reconstruction. Decoder replay state is used for decode rather than stored as a reusable prefix entry. Do not universalize its model-specific window and backtracking settings.

Replay can be paid during [[prefill-vs-decode]] admission or when state is missing. Measure peak device memory as well as persistent storage, replay frequency, FLOPs, first-token latency and later token latency. Fewer stored bytes can be useful even when total work rises. Compare keeping the state, compressing it, transferring it and recomputing it under the same workload.

## One example

With two local-attention layers, each seeing the current token plus two earlier positions, the final output can depend on five raw-token positions. Replaying only the final three without a boundary state cuts a real dependency path. It can be an intentional approximation, but it is not an exact reconstruction just because one layer's window is three.

## Check your understanding

**Question:** Does a 128-token replay bound prove exact equivalence? **Answer:** No. Check retained boundary state, multilayer dependencies, truncation semantics and quality. Measure the actual cost and correctness contract separately.
