# Chain-of-Thought

## Meaning

Chain-of-thought prompting supplies examples of intermediate steps or asks a model to write steps before answering. Those tokens remain available to later generation. The method can improve results, but a written rationale is not a guaranteed account of the model's internal computation.

## Mechanism

Later tokens can condition on earlier tokens through attention. Writing an intermediate result therefore creates external textual state that the model may reuse. It also spends additional generation work. These properties do not prove that the model follows the text faithfully or that extra computation alone explains an observed improvement.

The original prompting study reports gains on particular arithmetic, commonsense and symbolic tasks. Compare that empirical finding with a stronger, unsupported claim that one forward pass can perform only one arithmetic operation. A language model is not necessarily executing the narrated steps as a literal interpreter.

## One example

A customer has 7 notebooks and buys 3 packs containing 4 each. A possible decomposition records 3×4=12 and then 7+12=19. The final answer can use the written 12. This illustrates a possible dependency; it does not reveal the actual causal computation from the transcript alone.

If the text instead says the packs contain 15, the model may follow the mistake, correct it or ignore it. Interventions on intermediate text help distinguish these behaviors. A plausible final explanation without an intervention cannot establish which mechanism operated.

## Check your understanding

Does a correct answer with a coherent rationale prove faithful reasoning? **No.** Evaluate final correctness, step correctness, resources and faithfulness separately. Use matched direct-answer baselines and controlled changes to the intermediate text. Results depend on model, task and prompting conditions, and a rationale must not become an authorization or correctness oracle.
