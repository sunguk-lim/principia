# Multi-Turn Token Accounting

## Meaning

A conversation is not billed as a single ever-growing object. Each model call has its own input and output accounting; resending history can charge for that history again, even when cached reads have a discount. Track the actual calls rather than multiplying only the final context length by a single price.

## Mechanism

For turn t, let r_t be cache-read tokens, w_t cache-creation tokens, u_t uncached input tokens and o_t output tokens. Let their applicable per-token prices be p_r, p_w, p_u and p_o. With disjoint usage categories, [[arithmetic]] gives total cost Σ_t(r_t p_r+w_t p_w+u_t p_u+o_t p_o), plus other applicable fees. Some providers report input inclusively; normalize those fields before summing to avoid double counting. [[prefix-caching]] only discounts eligible matching material: expiration, prefix edits and model changes can move tokens between categories. Outputs from one turn can become billed input on later turns. Cache reuse saves prefill but does not remove the attention work of generating from a long retained history.

## One example

Use hypothetical prices per million tokens: read $0.20, write $2, uncached $1, output $4. Turn one writes a 1,000-token prefix, reads none, adds 100 uncached tokens and generates 50. Turn two reads the 1,000-token prefix, has 150 uncached input tokens including resent output, and generates another 50. Total cost is (1,000×2+250×1+100×4+1,000×0.20)/1,000,000=$0.00285. These are illustrative rates, not a provider quotation. A miss on turn two changes the accounting; do not assume every retained history token was a hit. Reconcile per-call usage with invoices and include retries, failed attempts when billed, tool-response growth, quality and task completion. Input discounts alone do not establish cheap agent operation.

## Check your understanding

May repeated history tokens be counted as free because they were charged on the first turn? No. Use the provider’s reported cache and input categories for each call; reuse changes the applicable rate, not automatically the token count.
