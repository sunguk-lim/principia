# Latent Reasoning

## Meaning

Latent reasoning performs intermediate inference work in hidden representations before emitting a prediction. It contrasts with the explicit intermediate tokens of [[chain-of-thought]]. A [[looped-transformer]] is one architecture for this, but latent reasoning is the computation-and-state choice rather than the name of every parameter-sharing architecture.

## Mechanism

Fix the model's learned weights. A token-space trajectory writes intermediate tokens, which later forward passes can read as part of the context. A latent trajectory instead updates an internal state for several steps and applies an output head afterward. The internal state can change without any visible reasoning token or weight update. Additional latent steps still execute operations; they do not turn a small parameter checkpoint into free additional depth.

The two routes have different state, observability, and cache costs. Token histories are inspectable but may be long, and their prose need not faithfully reveal the computation. Hidden states avoid requiring every intermediate result to be verbalized, but are harder to audit directly. Neither route guarantees logical correctness. A stable hidden state can encode the wrong answer, and a fluent chain can repeat a false premise.

## One example

Consider a two-layer shared core. Policy A allows four latent iterations before one answer token, costing eight core-layer applications plus fixed input/output work. Policy B uses one iteration for each of six intermediate tokens and then an answer token, costing fourteen core-layer applications plus repeated fixed work and growing token context. This is only an accounting illustration: it does not say the two policies compute the same function or reach equal quality. Tensor shapes, cache policies, and hardware utilization determine actual runtime.

A model trained for token-only computation cannot be assumed to accept arbitrary hidden-state feedback safely. Training objective, state initialization, depth distribution, and truncation determine what inference changes are meaningful. Extrapolate iteration count only after testing it; more work may produce plateaus, cycles, degraded quality, or numerical growth. Warm-starting one token from another token's latent state is another explicit architecture or inference change, not identical to restarting each token.

Use [[measurement]] to compare task correctness at matched total FLOPs, latency, memory, context, and tool/verifier cost. Report latent updates and generated tokens separately. Include difficulty slices, wrong-but-stable outputs, training-range versus extrapolated depth, and hard compute caps. Primary recurrent-depth experiments demonstrate a particular trained model; they do not prove that every task benefits or that hidden computation replaces external evidence.

## Check your understanding

Is generated-token count a universal measure of inference compute? No. A latent model can spend more internal updates while generating the same number of tokens.

