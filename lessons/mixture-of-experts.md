# Sparse Mixture-of-Experts

## Meaning

A sparse mixture-of-experts layer offers many independent expert transformations but executes only a few for each token. An expert can be a [[neural-network]] block. A learned router scores experts for the token, chooses a small subset and combines their outputs using gate weights derived from [[softmax]]. Selected-weight renormalization depends on the implementation.

## Mechanism

The distinction is between available parameters and selected work. A dense layer uses its whole transformation for every token. In a sparse layer, a token can use two experts out of many, while another token chooses a different pair. Increasing the expert population can add available capacity without proportionally increasing selected expert evaluations. It does not guarantee that experts specialize usefully, that training is stable or that overall latency stays fixed.

The router still has to decide. A flat learned projection computes a score for every expert. The system must store all expert weights, move tokens to the right place and manage uneven demand. At a fixed token batch, additional experts can reduce each expert's batch size and make execution less efficient. Load-balancing controls help but do not remove every skewed workload.

## Worked example

Take eight experts containing one million parameters each, selecting two per token. Total expert parameters are eight million; selected expert parameters per token are two million. Double the expert population to sixteen: total storage now represents sixteen million, while the selected parameter count stays two million. The flat router scores sixteen values rather than eight. These counts omit shared layers, router storage, optimizer state and data movement. They cannot be read as a measured speedup or total arithmetic count.

## Check your understanding

Does keeping two active experts guarantee constant latency as the population grows? No. It bounds one component under fixed expert dimensions. Measure routing, selected expert execution, communication, memory and complete step time at matched workload and quality.
