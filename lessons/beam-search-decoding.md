# Beam Search Decoding

## Meaning

Beam search is a bounded search over partial token sequences. It keeps several alternatives rather than making one irreversible greedy choice at each position. The beam width says how many unfinished candidates survive a pruning step, not how many complete possibilities have been examined.

## Mechanism

A sequence probability multiplies the conditional token probabilities along its own path. Implementations usually add log probabilities instead, avoiding tiny products. At each position, expand retained prefixes with eligible tokens, compute their cumulative scores and keep the best bounded frontier. Completed candidates and stopping conditions need explicit handling.

Finite pruning is the approximation. Once a prefix is removed, a later excellent continuation cannot rescue it. Length normalization changes the scoring objective; raw products favor shorter outputs because each additional factor is at most one. More search does not certify a factual or otherwise correct answer, even when the highest model score is found.

## One example

Consider exactly two output positions. The first distribution is A=.6, B=.4. After A, the next probabilities are x=.5 and y=.5. After B, they are x=.9 and y=.1. With a tie rule selecting x, greedy returns Ax with probability .30.

A width-two beam retains both first tokens. The completed candidates have probabilities Ax=.30, Ay=.30, Bx=.36 and By=.04. It therefore selects Bx, which began with the locally less likely first token. The four completion probabilities sum to one. The example shows why retaining an alternative can help; it does not prove that a finite beam finds the optimum in a deeper tree.

## Check your understanding

Does doubling beam width necessarily improve task quality? No. It changes which high-scoring candidates survive and adds compute and memory. Validate cumulative scores on small enumerated trees, specify length penalties and stopping, then compare actual task outcomes and latency. A likelihood score and a correctness judgment answer different questions.
