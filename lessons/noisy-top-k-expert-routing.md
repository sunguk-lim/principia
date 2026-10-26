# Noisy Top-k Expert Routing

## Meaning

A [[mixture-of-experts]] router normally chooses the experts with the largest learned scores. Noisy top-k routing perturbs those scores before sparse selection, giving other experts a chance to receive training examples. It still runs only the chosen experts, not all of them.

## Mechanism

For each expert, add a standard [[normal-distribution]] draw multiplied by a positive noise scale to the clean routing score. The scale can be learned from the current token representation. Keep the k largest resulting scores and normalize their weights with softmax; other weights become zero. This separates two choices: which experts are visited and how much each selected expert contributes.

Exploration is useful because an expert that receives no examples has little opportunity to improve. But noise alone does not guarantee equal traffic. The original design also uses objectives that discourage unbalanced importance and load. Its noise is not promised to decay monotonically, and the evaluation path must state whether it uses clean or noisy scores.

## One example

Clean scores [2.0, 1.8, 0.2] select experts 1 and 2 when k=2. Give each expert noise scale 0.5. Draws [-2, -1, 3] change the scores to [1.0, 1.3, 1.7], so experts 3 and 2 now run. Their scores differ by 0.4, giving normalized weights about 0.599 and 0.401. Expert 1 gets zero. This shows how a less-favored expert can receive a training example; it does not establish its long-run selection probability.

## Check your understanding

Is noisy routing a complete load-balancing policy? No. Measure expert traffic, overflow, task quality and runtime across seeds. Test the expected sparsity and weight sums. In the referenced Tensor2Tensor implementation, noise is training-only and inference uses clean scores; preserve that distinction when validating deployment.
