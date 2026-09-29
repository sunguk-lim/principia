# Training-Data Extraction Risk

## Meaning

[[training-data-extraction-risk]] is the possibility that a model emits specific information from its training set that should not be disclosed. It differs from ordinary model error: the output can be factually accurate yet privacy-violating. It also differs from a retrieval leak, where an external document is improperly placed in the prompt.

## Mechanism

Training a [[neural-network]] adjusts parameters using many examples. Some distinctive strings can become recoverable under suitable prompts. The existence of extraction attacks means a clean refusal to one standard question does not prove safety. It does **not** mean every training example is stored verbatim or retrievable. Attack success depends on the data, model, prompt, decoding, and query budget.

Trace the full production path. Was the string in pretraining or fine-tuning data, a retrieved document, a tool response, or the conversation? Without that trace, adding another refusal rule may target the wrong cause. Preventive data minimization lowers exposure before training. Retrieval authorization and output detection protect different boundaries but can fail independently.

## One example

A synthetic canary such as a unique fictional account phrase is inserted into a controlled training set. Evaluators try multiple prompts and sampling settings, record exact and near matches, and compare a model trained without the canary. This estimates one kind of extraction risk under a stated attack budget. It is not a certificate that no real secret can leak.

## Check your understanding

**Question:** Does a model saying “I cannot share that” prove the data was removed from its weights? **Answer:** No. It proves a behavior for that prompt. Extraction tests, data lineage, and comparison with a retrained reference are needed to assess the broader risk.
