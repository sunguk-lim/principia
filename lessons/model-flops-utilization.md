# Model FLOPs Utilization

## Meaning

Model FLOPs utilization (MFU) is a training-system throughput ratio. Its numerator counts useful model work at the achieved token rate, not every instruction executed by the accelerator. It is distinct from device busy time and from hardware FLOPs utilization (HFU), which can include extra arithmetic performed by the implementation.

## Mechanism

Let F_model be declared model forward-plus-backward floating-point operations per token, r the observed training tokens per second over a specified interval, and P_peak the summed theoretical arithmetic peak of all participating devices at the stated precision and operation convention. Define

$$\mathrm{MFU}=\frac{r F_{model}}{P_{peak}}=\frac{r}{P_{peak}/F_{model}}.$$

[[transformer-flop-estimation]] supplies model arithmetic accounting; [[measurement]] supplies the elapsed-time boundary and throughput. Multiply-add conventions, attention terms, padding, token counts, architecture and precision must agree. PaLM's definition excludes rematerialization from required model work. [[activation-checkpointing]] may execute additional forward operations to recover activations; these can raise hardware operation counts without increasing F_model. The reference is a definition and reported experiment, not a guarantee about other training runs.

## Worked example

Suppose F_model=2×10¹² FLOPs/token, r=100 tokens/s and system peak P_peak=10¹⁵ FLOPs/s. The ideal rate is 500 tokens/s and MFU is 100/500=0.20, or 20%. If rematerialization adds 10¹² operations per token, actual arithmetic at the same throughput is 3×10¹⁴ FLOPs/s. An arithmetic-based HFU estimate is 30% while MFU remains 20%. Those are illustrative accounting values, not accelerator measurements.

If an optimization removes that redundant arithmetic and raises r to 120, MFU becomes 24%, even though the system performs fewer operations per token. Higher hardware activity alone was not the goal. Compare useful tokens/s and time to a fixed quality target; MFU does not measure accuracy, energy efficiency or absolute cost. Changing the model to one requiring more operations can raise the ratio while reducing useful throughput. Include initialization, data stalls or checkpoint writes consistently in the measurement interval, and distinguish steady-state MFU from whole-job efficiency.

## Check your understanding

**Question:** Does recomputing more activations necessarily improve MFU? **Answer:** No. Only improved useful throughput under the same declared model-work convention improves this ratio.
