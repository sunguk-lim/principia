# Masked diffusion language model

An autoregressive language model extends a prefix one token at a time. A masked diffusion language model begins with unknown positions and repeatedly predicts some of them. Its “diffusion” process can use discrete masks, not the Gaussian noise familiar from image models.

In training, hide selected token positions and ask a Transformer to predict the missing tokens from those still visible. Vary the mask pattern so the model learns to fill gaps under different amounts of context. At generation time, choose an output length or length policy, initialize its positions as masks, predict unresolved tokens, and commit or remask positions according to a schedule. Later passes can use the newly visible tokens to revise uncertain choices.

For example, start with `The [MASK] is [MASK]`. One pass proposes two words. A second pass may retain the first and reconsider the second. Several positions can be proposed in one pass, but repeated whole-sequence passes have their own cost. Parallel proposals therefore do not prove lower latency than left-to-right generation.

LLaDA is a concrete published implementation of masked forward corruption and reverse generation. Its results belong to that model and benchmark setup. Compare methods at matched quality and hardware, reporting wall-clock time, passes, memory, length errors, and order-sensitive task accuracy. Also specify which predictions become fixed and which may change.

**Check:** Why does predicting multiple positions per pass not automatically make masked diffusion faster?
