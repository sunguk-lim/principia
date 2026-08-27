# Figure spec — `arithmetic-intensity`

## Visual teaching contract

- **Audience:** A programmer who knows arithmetic and numeric formats but has not used performance models.
- **Single job:** Make the denominator physical: bytes count only when they cross one explicitly chosen boundary.
- **Visual thesis:** The FP32 vector triad performs two FLOPs while two inputs and one output cross the HBM boundary, so `2 ÷ 12 ≈ 0.17 FLOP/byte`; reuse raises work without repeating traffic.
- **Traced object:** Three four-byte FP32 values: two blue reads and one amber result write.
- **Signature moment:** All three transfers visibly cross the same amber boundary before appearing in the ratio.

**Comprehension test:** The reader should be able to name the boundary, derive 12 bytes and 2 FLOPs, compute the ratio, and explain why reuse raises intensity.

**Rendered constraints:** Static 720×640 canvas; every shown number is derivable on-canvas; no hardware speed claim is made.
