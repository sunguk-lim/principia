# Causal Attention Validation

## Meaning

Causal attention validation asks whether an executed model can obtain information from tokens it should not yet see. A low loss alone cannot answer this. The relevant contract is [[causal-language-model-training]]: the output for a next-token prediction depends only on the available prefix.

## Mechanism

Apply [[metamorphic-testing]] by preserving a prefix and changing its suffix. Disable stochastic behavior, keep state and positions fixed, and compare the earlier output scores within a documented numerical tolerance. Functional PyTorch attention needs its dropout argument explicitly set to zero for this comparison; setting an enclosing module to evaluation mode is not a substitute for passing the correct argument.

Check mask conventions separately. MultiheadAttention boolean True blocks access, while functional scaled-dot-product attention boolean True allows access. A floating mask adds score biases instead. The installed API, dimensions and broadcasting rule determine what actually runs.

## One example

For `[red, fox, runs, fast]` and `[red, fox, sleeps, now]`, compare outputs at the first two positions. They should agree because both inputs have the same first two tokens. The third-position outputs need not agree. For two queries and four keys, the allowed pattern is `[[1,0,0,0],[1,1,0,0]]`; a boolean block mask uses its complement. A deliberately unmasked reference should fail this test, confirming that the example is sensitive enough to reveal leakage.

## Check your understanding

Does unchanged sampled text prove unchanged prefix predictions? No. Different score distributions can choose the same token. Compare logits, then repeat for padding, packed documents and cache use. Passing these cases also does not prove the labels were shifted correctly or that the model generates useful answers.
