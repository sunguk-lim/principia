# Figure training dataset — (x = concept, y = refined reference figure)

> Extracted from `../etc/` (7 artifacts → **213 figures**; each sample is one FIGURE, flat
> table below — counts corrected 2026-07-18 after flattening exposed a long-standing
> undercount: the linux section was labeled "100" while actually holding 152 rows).
> Used by the template-training loop:
>
> 1. **Blind draw**: produce ŷ from (concept x, `specs/_TEMPLATE.spec.md`) — the drawer must NEVER see y first.
> 2. **Compare**: render y (never judge from code), diff ŷ vs y — what did the reference do better, and why?
> 3. **Update**: write each lesson into `specs/_TEMPLATE.spec.md` (spec structure) or
>    `protocols/VISUAL_PROTOCOLS.md` (drawing mechanics) as a GENERAL principle, never an incident.
> 4. Next example. **Break** after 2 consecutive examples yielding no new rule.
>
> **CONVERGENCE STATUS (revised 2026-07-18):** the 2026-07-17 "converged" call (#21–#22
> consecutive zeros) was premature — those probes sampled covered strata. A corrected
> certification batch on unexplored structures (#23 comparison-spine: 7, #24 curve/plot: 7,
> #25 rack-nesting: 3, #26 time-grid: 4) showed **execution quality is converged** (zero
> correctness defects; draws consistently beat references) but **genre-corner rule coverage
> is not** — each never-exercised structure still yields 2–7 rules, decaying within the
> corner. Treat every structurally novel genre/overlay combination as untrained until probed.
>
> **Tier**: A = drawn/animated diagram with spatial semantics (prime training signal) ·
> B = box/arrow/chain styled-div diagram (good) · C = styled list/comparison table (weak — use
> only for genre coverage, skip by default).
> **Pass**: fill with `#iter: lesson-count` when trained on. Curriculum: A-tier first,
> maximize genre diversity between consecutive picks.

## Samples — flat, one row per FIGURE

| id | concept (x) | source | y location | genre | node | tier | pass |
|---|---|---|---|---|---|---|---|
| mpi-broadcast | root replicates one value to all ranks | mpi | `drawBroadcast()` L142–159 | dataflow | broadcast | A |  |
| mpi-scatter | root splits data into distinct per-rank chunks | mpi | `drawScatter()` L162–179 | dataflow | scatter | A |  |
| mpi-gather | all ranks send chunks to root, which assembles | mpi | `drawGather()` L182–200 | dataflow | gather | A |  |
| mpi-reduce | values combine via SUM, result lands at root only | mpi | `drawReduce()` L203–230 | dataflow | reduce | A |  |
| mpi-all-reduce | reduce then result fans back to every rank | mpi | `drawAllreduce()` L233–261 | dataflow | all-reduce | A | #1: 4 lessons |
| mpi-all-gather | every rank ends with the full collection (4×4 mesh) | mpi | `drawAllgather()` L264–287 | dataflow | all-gather | A |  |
| mpi-all-to-all | personalized exchange = distributed transpose | mpi | `drawAlltoall()` L290–318 | dataflow/grid | all-to-all | A |  |
| mpi-reduce-scatter | element-wise reduce, then scatter result slices | mpi | `drawReduceScatter()` L321–372 | dataflow | reduce-scatter | A |  |
| mpi-scan | inclusive prefix-sum built rank-by-rank | mpi | `drawScan()` L374–437 | dataflow | scan | A | #21: 0 lessons ✅ |
| mpi-barrier | all must arrive before any proceeds (timeline lanes) | mpi | `drawBarrier()` L440–560 | timeline | barrier | A | #9: 3 lessons |
| diffop-overview-table | six operators by input→output type | diffop | "The six operators" L138–148 | comparison | differential-operators | C |  |
| diffop-gradient-shape | gradient: scalar → column of first partials | diffop | Fig 1, L162–178 | math-shape | gradient | A |  |
| diffop-laplacian-shape | Laplacian: scalar → one cell, summed 2nd partials | diffop | Fig 1, L179–187 | math-shape | laplacian | A |  |
| diffop-hessian-shape | Hessian: scalar → symmetric 3×3 grid of 2nd partials | diffop | Fig 1, L188–214 | math-shape/grid | hessian | A |  |
| diffop-divergence-shape | divergence: vector column → one summed cell | diffop | Fig 1, L217–229 | math-shape | divergence | A | #22: 0 lessons ✅ |
| diffop-curl-shape | curl: vector → column of mirror-pair differences | diffop | Fig 1, L230–248 | math-shape | curl | A |  |
| diffop-jacobian-shape | Jacobian: vector → 3×3 grid of all first partials | diffop | Fig 1, L249–279 | math-shape/grid | jacobian | A | #4: 7 lessons |
| diffop-del-atom | ∇ as a single vector-of-derivatives building block | diffop | Fig 2, L306–308 | math-shape | del-operator | A |  |
| diffop-three-products | ∇ × {scalar-mult, dot, cross} = grad/div/curl | diffop | Fig 2, L309–326 | dataflow | del-operator | A |  |
| diffop-composition-tree | composing the three yields Laplacian/Hessian/Jacobian | diffop | Fig 2, L327–342 | hierarchy | differential-operators | A |  |
| diffop-antisymmetry-identities-svg | Jacobian trace→div, antisym part→curl, compositions vanish | diffop | Fig 2, L342–347 | comparison | symmetric-antisymmetric-decomposition | A |  |
| diffop-laplacian-dot-product | Laplacian = ∇·∇, matching partials paired | diffop | Fig 3, L379–399 | math-shape | laplacian | A |  |
| diffop-laplacian-composition-chain | Laplacian = divergence after gradient (3-box chain) | diffop | Fig 3, L402–412 | dataflow | laplacian | A |  |
| diffop-antisymmetry-identity-cards | ∇×(∇f)=0 and ∇·(∇×F)=0 side by side | diffop | L418–421 | comparison | curl-of-gradient-zero, divergence-of-curl-zero | C |  |
| arch-attention-variants | MHA/GQA/MQA/MLA trade KV size via head sharing | llm_par | `AttentionVariants` L1450–1594 | hierarchy | gqa | A |  |
| arch-sliding-window-mask | SWA + sinks mask the N×N attention matrix | llm_par | `SlidingWindow` L2193–2284 | grid-tiling | sliding-window-attention | A |  |
| arch-mamba-block-graph | Mamba block signal flow with shape tags per wire | llm_par | `MambaSSM` L2382–2479 | dataflow | state-space-model | A |  |
| arch-mamba-recurrence-zoom | selective-SSM recurrence, 5-phase state update | llm_par | `MambaSSM` L2499–2576 | state-machine | state-space-model | A | #11: 7 lessons |
| arch-mamba-sequence-tape | one fixed-size state threads the whole sequence | llm_par | `MambaSSM` L2583–2602 | timeline | state-space-model | A |  |
| par-data-parallel | replicas diverge on data, AllReduce re-syncs grads | llm_par | `DataParallel` L113–148 | dataflow | data-parallelism | A | #14: 1 lesson |
| par-tensor-parallel-mlp | column- then row-split weights, one AllReduce per block | llm_par | `TensorParallel` L205–325 | grid-tiling | tensor-parallelism | A | #15: 4 lessons |
| par-pipeline-parallel-gpipe | GPipe fill-drain schedule with bubble | llm_par | `PipelineParallel` L373–427 | timeline | pipeline-parallelism | A | #3: 4 lessons |
| par-context-parallel-ring | KV blocks rotate a ring; block matrix fills per round | llm_par | `ContextParallel` L477–607 | grid+dataflow | context-parallelism | A | #13: 3 lessons |
| par-expert-parallel-moe | router + two All-to-Alls (dispatch, merge) | llm_par | `ExpertParallel` L671–759 | dataflow | expert-parallelism | A | #16: 4 lessons |
| par-fsdp-zero-clock | shard → AllGather → compute → discard → ReduceScatter | llm_par | `FSDP` L831–952 | layered/state | fsdp | A | #17: 2 lessons |
| exec-memory-movement-amortization | prefill amortizes weight loads; decode is memory-bound | llm_par | `MemoryMovement` L3336–3423 | dataflow | weight-load-amortization | A | #18: 3 lessons (0 ref-grounded) |
| exec-flash-attention-tiling | tile sweep + online softmax, no N×N materialized | llm_par | `FlashAttention` L1750–1840 | grid-tiling | flash-attention | A | #8: 7 lessons |
| exec-flash-attention-memory-hierarchy | tiles resident in SRAM; HBM writes avoided | llm_par | `FlashAttention` L1849–2026 | layered-stack | memory-hierarchy | A |  |
| serve-paged-block-table-map | logical→physical block table (OS page table for KV) | llm_par | `PagedAttention` L2090–2105 | address-stack | paged-attention | A | #10: 7 lessons |
| serve-paged-scatter-vs-contiguous | coalesced burst vs random-hop gather | llm_par | `PagedAttention` L2110–2117 | comparison | paged-attention | A |  |
| serve-paged-coarse-blocks | 16-token blocks keep reads coalesced | llm_par | `PagedAttention` L2125–2133 | grid-tiling | paged-attention | A |  |
| serve-paged-fused-kernel | block-at-a-time online-softmax folds each block | llm_par | `PagedAttention` L2143–2164 | address/state | paged-attention | A |  |
| serve-paged-bandwidth-hiding | table lookup hidden behind the byte transfer | llm_par | `PagedAttention` L2170–2176 | timeline | paged-attention | A |  |
| serve-prefix-caching-radix-tree | shared-prefix KV blocks via radix tree | llm_par | `PrefixCaching` L2665–2708 | hierarchy | prefix-caching | A | #6: 4 lessons (+1 deferred) |
| serve-kv-quantization-bitwidth | bit-width bars: memory savings vs quality | llm_par | `KVQuantization` L2762–2791 | math-shape | kv-quantization | B |  |
| serve-chunked-prefill-roofline-timeline | weight-stream vs compute race per layer vs N | llm_par | `ChunkedPrefill` L2926–2961 | timeline | roofline-model | A |  |
| serve-chunked-prefill-throughput-curve | throughput rises then falls with N (peak marker) | llm_par | `ChunkedPrefill` L2986–3001 | math-shape | roofline-model | A | #24: 7 lessons (spike — curve genre) |
| serve-chunked-prefill-scheduler-steps | mixed prefill-chunk + decode tokens per batch | llm_par | `ChunkedPrefill` L3036–3053 | state/grid | chunked-prefill | A | #19: 5 lessons |
| serve-chunked-prefill-attention-tails | chunking adds no quadratic cost (same Σ positions) | llm_par | `ChunkedPrefill` L3091–3109 | comparison | chunked-prefill | A |  |
| serve-chunked-prefill-wallclock | naive stalls decode; chunked never does | llm_par | `ChunkedPrefill` L3126–3159 | timeline | chunked-prefill | A |  |
| dec-speculative-decoding-loop | draft K, verify in one pass, accept/reject/bonus | llm_par | `SpeculativeDecode` L1022–1146 | timeline/state | speculative-decoding | A | #20: 4 lessons |
| dec-structured-output-dfa | schema→DFA masks logits per step | llm_par | `StructuredOutput` L1300–1430 | state-machine | structured-output | A | #5: 6 lessons |
| dec-test-time-compute-budgets | direct → CoT → self-correct → best-of-N tradeoff | llm_par | `TestTimeCompute` L3203–3290 | dataflow/comparison | test-time-compute | A |  |
| notes-mle-vs-map-chips | MLE vs MAP = same argmax, ± prior factor | notes | §2, L175–178 | comparison | maximum-a-posteriori | C |  |
| linux-arch-overview-stack | user→syscall gate→kernel→hardware layering | linux | L1040–1091 | layered-stack | kernel | B |  |
| linux-gpu-stack-overview | Python→CUDA→ioctl→nvidia.ko→silicon layering | linux | L1093–1127 | layered-stack | gpu-data-flow | B |  |
| linux-kernel-vs-pid1 | kernel is not a process; PID 1 is | linux | L1405–1420 | comparison | kernel | C |  |
| linux-boot-to-pid1 | kernel handoff to PID 1 | linux | L1424–1437 | timeline | init-process | B |  |
| linux-boot-complete-chain | power-on → firmware → GRUB → kernel → PID1 → shell | linux | L1443–1462 | timeline | boot-process | B |  |
| linux-install-one-picture | OS installation end-to-end | linux | L1570–1593 | timeline | boot-process | B |  |
| linux-kernel-one-vs-many | one binary, many subsystems | linux | L1622–1626 | comparison | kernel | C |  |
| linux-kernel-building-analogy | kernel-as-building mapped rows | linux | L1634–1641 | comparison | kernel | C |  |
| linux-kernel-contiguous-memory | kernel occupies one continuous region | linux | L1648–1657 | address-stack | kernel | B |  |
| linux-kernel-module-loading | module loaded into a separate region later | linux | L1663–1665 | address-stack | kernel-module | B |  |
| linux-function-vs-handler | called explicitly vs triggered by event | linux | L1693–1705 | comparison | interrupt | C |  |
| linux-driver-interface-pattern | function-pointer interface; drivers fill it in | linux | L1806–1824 | dataflow | device-driver | B |  |
| linux-kernel-entry-points | syscall / interrupt / timer tick entries | linux | L1891–1913 | state-machine | interrupt | B |  |
| linux-keypress-walkthrough | keystroke → interrupt → buffer → read() → echo | linux | L2041–2056 | timeline | interrupt | B |  |
| linux-mov-instruction-dataflow | MOV moves data over the bus | linux | L2097–2103 | dataflow | mmu | C |  |
| linux-dma-before-after | CPU-copy loop vs DMA delegate + interrupt | linux | L2141–2154 | comparison | dma | B |  |
| linux-scatter-gather-dma | controller walks a (block→addr) list | linux | L2177–2194 | dataflow | dma | B |  |
| linux-boot-stage-dma-evolution | data-movement capability grows per boot stage | linux | L2205–2219 | timeline | boot-process | C |  |
| linux-kernel-complete-picture | userspace / syscall gate / kernel / hardware | linux | L2227–2244 | layered-stack | kernel | B |  |
| linux-syscall-register-form | rax/rdi/rsi/rdx as the syscall "form" | linux | L2323–2328 | address-stack | system-call | B |  |
| linux-syscall-three-layers | glibc wrapper / syscall instr / kernel handler | linux | L2486–2500 | layered-stack | system-call | B |  |
| linux-ring-4floor-building | privilege rings as building floors | linux | L2512–2524 | hierarchy | user-mode-vs-kernel-mode | B |  |
| linux-ring-diagram-svg | concentric Ring3/Ring0 with syscall-gate arrows | linux | `<svg>` L2526–2554 | address-stack | user-mode-vs-kernel-mode | A | #27: 4 lessons (radial genre) |
| linux-ring3-vs-ring0-capabilities | per-ring can/cannot checklists | linux | L2558–2577 | comparison | user-mode-vs-kernel-mode | C |  |
| linux-container-syscall-filtering | same syscall, namespace-filtered result | linux | L2631–2637 | comparison | namespace | C |  |
| linux-clone-fork-thread-container | clone() flags ⇒ fork / thread / container | linux | L2904–2921 | comparison | clone | B |  |
| linux-fork-exec-ls-tmp | fork + waitpid + execve two-column trace | linux | L2938–2960 | dataflow | fork-exec | B |  |
| linux-fork-vs-fork-alone | fork+exec vs fork-alone use cases | linux | L2973–2978 | comparison | fork-exec | C |  |
| linux-spawn-vs-fork-exec | spawn as fork+exec wrapper across OSes | linux | L2998–3023 | comparison | fork-exec | C |  |
| linux-python-multiprocessing-methods | fork/spawn/forkserver per platform | linux | L3012–3024 | comparison | fork-exec | C |  |
| linux-cow-copy-on-read-problem | refcounting defeats COW sharing | linux | L3038–3059 | dataflow | copy-on-write | B |  |
| linux-cow-spawn-wins-little-data | spawn wins when child needs little | linux | L3065–3075 | comparison | copy-on-write | C |  |
| linux-cow-fork-wins-most-data | fork wins when child needs most | linux | L3077–3089 | comparison | copy-on-write | C |  |
| linux-cow-decision-summary | little/most/some-data decision branches | linux | L3092–3103 | comparison | copy-on-write | C |  |
| linux-process-states | R/S/D/Z/T states | linux | L3124–3130 | state-machine | process | C |  |
| linux-process-tree | PID hierarchy from PID 1 | linux | L3145–3155 | hierarchy | process | B |  |
| linux-clone-flags-thread-container-2 | share-vs-own-copy per clone() flags (repeat) | linux | L3304–3321 | comparison | thread | C |  |
| linux-gil-shared-code-svg | GIL mutex; shared bytecode, private PCs | linux | `<svg>` L3335–3367 | address-stack | gil | A |  |
| linux-virtual-vs-physical-addr | same virtual addr → different physical per process | linux | L3501–3513 | address-stack | virtual-memory | B |  |
| linux-page-number-offset-split | address = page number + offset; MMU swaps the page | linux | L3539–3550 | address-stack | page-table | B |  |
| linux-page-table-entry-bits | PTE fields (present/RW/user/dirty/accessed) | linux | L3577–3585 | address-stack | page-table | C |  |
| linux-demand-paging-malloc | malloc maps lazily; first touch faults a page in | linux | L3612–3628 | dataflow | demand-paging | B |  |
| linux-cow-fork-instant | shared read-only frame splits on first write | linux | L3670–3683 | address-stack | copy-on-write | B |  |
| linux-process-memory-layout-svg | canonical VA layout: text→heap↑ / mmap / stack↓ / kernel | linux | `<svg>` L3731–3768 | address-stack | address-space-layout | A | #2: 4 lessons |
| linux-two-process-isolation-svg | two page tables → distinct physical frames | linux | `<svg>` L3776–3810 | address-stack | virtual-memory | A |  |
| linux-mm-bookkeeping-svg | task_struct → mm_struct → VMAs + page table → frames | linux | `<svg>` L3823–3860 | hierarchy | page-table | A |  |
| linux-vfs-function-pointers | VFS interface; ext4/NFS/procfs fill it in | linux | L3978–3990 | dataflow | vfs | B |  |
| linux-inode-path-resolution | path walk: dentry→inode per component | linux | L4016–4024 | dataflow | inode | B |  |
| linux-disk-layout-superblock-inode-data | superblock / inode table / data blocks | linux | L4047–4058 | address-stack | inode | B |  |
| linux-inode-256-byte-fields | fields inside one on-disk inode | linux | L4066–4080 | address-stack | inode | C |  |
| linux-filename-to-data-chain | filename→dentry→inode→blocks→data | linux | L4083–4088 | dataflow | inode | B |  |
| linux-page-cache-hit-miss | read(): cache hit vs DMA-miss branch | linux | L4121–4137 | dataflow | page-cache | B | #12: 2 lessons (0 ref-grounded) |
| linux-write-dirty-page-writeback | write→dirty→async writeback (or fsync) | linux | L4164–4179 | timeline | writeback | B |  |
| linux-io-complete-chain | full I/O chain for `cat /etc/hostname` | linux | L4188–4210 | dataflow | vfs | B |  |
| linux-everything-is-a-file | one read()/write() API, many resources | linux | L4217–4225 | comparison | vfs | C |  |
| linux-overlayfs-layers | writable layer over read-only layers | linux | L4233–4249 | layered-stack | overlayfs | B |  |
| linux-namespace-8-types | the 8 namespace types | linux | L4386–4407 | comparison | namespace | C |  |
| linux-namespace-filters-not-changes | namespaces filter results, not code | linux | L4429–4437 | comparison | namespace | C |  |
| linux-task-struct-nsproxy | task_struct → nsproxy pointer | linux | L4461–4467 | address-stack | namespace | C |  |
| linux-nsproxy-namespace-objects | nsproxy → per-type namespace objects | linux | L4469–4476 | hierarchy | namespace | B |  |
| linux-namespace-creation-steps | clone(CLONE_NEW*) creates namespace objects | linux | L4479–4494 | dataflow | namespace | B |  |
| linux-cgroup-limit-enforcement | limits checked at brk()/schedule time | linux | L4529–4545 | dataflow | cgroup | B |  |
| linux-defense-in-depth-4-layers | namespaces+cgroups+capabilities+seccomp | linux | L4578–4587 | layered-stack | capabilities | B |  |
| linux-container-combination-timeline | 2002→2013 milestones to Docker | linux | L4597–4604 | timeline | container | C |  |
| linux-docker-run-full-sequence | docker run: CLI→dockerd→containerd→shim→clone→pivot_root | linux | L4612–4639 | dataflow | container-runtime | B |  |
| linux-container-vs-vm | container vs VM properties | linux | L4735–4749 | comparison | container | C |  |
| linux-socket-tcp-lifecycle | socket/connect/send/recv/close sequence | linux | L4799–4818 | dataflow | socket | B |  |
| linux-send-packet-5-layers | send path: headers added layer by layer | linux | L4838–4861 | layered-stack | network-stack | B | #7: 1 lesson |
| linux-recv-packet-reverse | receive path: headers stripped in reverse | linux | L4890–4907 | layered-stack | network-stack | B |  |
| linux-hub-vs-switch-vs-wifi | broadcast vs targeted delivery | linux | L4951–4970 | comparison | mac-vs-ip | C |  |
| linux-packet-hop-by-hop | NIC→switch→routers→destination | linux | L4987–5004 | timeline | ip-routing | B |  |
| linux-container-networking-primitives | veth / bridge / iptables NAT roles | linux | L5060–5073 | comparison | container-networking | C |  |
| linux-container-http-request-path | container netns→veth→bridge→NAT→NIC | linux | L5080–5096 | dataflow | container-networking | B |  |
| linux-tcp-responsibilities | 5 things TCP handles invisibly | linux | L5114–5123 | comparison | tcp | C |  |
| linux-hypervisor-type1-vs-type2 | bare-metal vs hosted hypervisor stacks | linux | L5225–5248 | layered-stack | hypervisor | B |  |
| linux-container-vs-vm-revisited | container vs VM (repeat) | linux | L5271–5284 | comparison | container | C |  |
| linux-rtos-blackout-causes | what breaks Linux's predictability | linux | L5310–5323 | comparison | real-time-os | C |  |
| linux-rtos-vs-linux-priority | strict preemption vs fair scheduling | linux | L5345–5356 | comparison | real-time-os | C |  |
| linux-rtos-interrupt-latency-bound | bounded vs unbounded critical sections | linux | L5378–5391 | comparison | real-time-os | C |  |
| linux-rtos-kernel-size-comparison | kernel LOC across 5 kernels | linux | L5413–5418 | comparison | real-time-os | C |  |
| linux-rtos-usecases | where hard real-time matters | linux | L5427–5435 | comparison | real-time-os | C |  |
| linux-rtos-full-comparison-table | full Linux-vs-RTOS attribute table | linux | L5442–5452 | comparison | real-time-os | C |  |
| gpu-torch-add-journey | torch.add descends 8 layers to silicon | linux | L5489–5506 | dataflow | gpu-data-flow | B |  |
| gpu-every-layer-glance | 12-layer stack overview | linux | L5511–5528 | layered-stack | gpu-data-flow | C |  |
| gpu-5-level-optimization-stack | 5 levels of GPU perf optimization | linux | L5548–5567 | hierarchy | roofline-model | C |  |
| gpu-two-parallel-hierarchies | hardware tree mirrors job-unit tree | linux | L5595–5613 | hierarchy | cuda-thread-hierarchy | B |  |
| gpu-chip-and-sm-svg | full chip zoomed into one SM's sub-cores | linux | `<svg>` L5695–5780 | dataflow | streaming-multiprocessor | A | #28: 2 lessons (zoom link) |
| gpu-resource-scope-table | resource sharing scope thread→GPU | linux | L5812–5825 | hierarchy | gpu-memory-spaces | C |  |
| gpu-warp-scheduler-cycle-trace | cycle-by-cycle warp pick/stall trace | linux | L5870–5881 | timeline | warp | B |  |
| gpu-simt-level-rules-table | fixed vs free per grid/block/warp/thread | linux | L5888–5895 | hierarchy | simt | C |  |
| gpu-warp-specialization-code | warps taking different roles for free | linux | L5908–5921 | dataflow | warp | C |  |
| gpu-warp-divergence-serialization | divergent branch serialized, lanes masked | linux | L5929–5934 | dataflow | simt | C |  |
| gpu-occupancy-limit-calc | occupancy = MIN over 4 resource caps | linux | L5960–5976 | math-shape | occupancy | B |  |
| gpu-two-processes-two-computers | CPU and GPU as two computers | linux | L6007–6014 | comparison | cpu-vs-gpu | C |  |
| gpu-dma-copy-pcie-path | cudaMemcpy H2D via PCIe TLPs | linux | L6047–6061 | dataflow | gpudirect | B |  |
| gpu-grid-block-array-mapping | 3907 blocks cover the array in slices | linux | L6107–6114 | hierarchy | cuda-thread-hierarchy | B |  |
| gpu-warp-block-subcore-mapping | 8 warps spread over 4 sub-cores | linux | L6134–6144 | hierarchy | warp | B |  |
| gpu-warp-lockstep-4-instructions | ld/ld/add/st in lockstep with coalescing | linux | L6154–6175 | timeline | memory-coalescing | B |  |
| gpu-4level-distribution-tables | job-unit counts × hardware concurrency | linux | L6193–6216 | hierarchy | cuda-thread-hierarchy | C |  |
| gpu-dataflow-u-shape-svg | full round trip host→HBM→core→host | linux | `<svg>` L6267–6362 | address-stack | gpu-memory-spaces | A |  |
| gpu-coordination-layers-table | what each of 10 layers contributed | linux | L6369–6382 | hierarchy | gpu-data-flow | C |  |
| gpu-multigpu-3-mechanisms | staged copy vs P2P vs NVLink | linux | L6401–6407 | comparison | nvlink | C |  |
| gpu-nccl-transport-selection | NCCL transport by topology | linux | L6462–6467 | comparison | nccl | C |  |
| gpu-rdma-cross-node-path | GPUDirect RDMA bypasses both CPUs | linux | L6512–6513 | dataflow | gpudirect | C |  |
| gpu-persistent-comm-kernel-split | SMs split compute vs comm | linux | L6562–6573 | dataflow | streaming-multiprocessor | B |  |
| gpu-gh200-nvlink-c2c-svg | Grace↔Hopper bonded by NVLink-C2C | linux | `<svg>` L6584–6619 | dataflow | nvlink | A |  |
| gpu-nvl72-rack-svg | 72 GPUs as one logical accelerator | linux | `<svg>` L6625–6709 | grid-tiling | nvlink | A | #25: 3 lessons |
| gpu-coherent-domain-growth-svg | coherent domain widening 1→288 GPUs | linux | `<svg>` L6715–6749 | grid-tiling | nvlink | A |  |
| gpu-culaunchkernel-signature | cubin vs runtime schedule/data params | linux | L6789–6799 | address-stack | cuda-kernel | C |  |
| gpu-cubin-compute-vs-schedule-split | cubin=compute, launch params=distribution | linux | L6805–6811 | comparison | cuda-kernel | C |  |
| gpu-triton-constexpr-baking | tl.constexpr baked at compile time | linux | L6817–6829 | comparison | jit-vs-aot-compilation | C |  |
| gpu-4-variation-pipeline-table | eager/cuBLAS/torch.compile/TensorRT stage-by-stage | linux | L6850–6982 | comparison | jit-vs-aot-compilation | C |  |
| gpu-function-qualifiers | __global__/__device__/__host__ | linux | L6995–7003 | comparison | cuda-kernel | C |  |
| gpu-thread-indexing-builtins | threadIdx/blockIdx/blockDim/gridDim | linux | L7010–7014 | address-stack | cuda-thread-hierarchy | C |  |
| gpu-loop-vanishes | CPU for-loop becomes the grid | linux | L7034–7048 | comparison | cuda-kernel | B |  |
| gpu-memory-space-table | 7 memory spaces by location/scope/latency | linux | L7067–7076 | grid-tiling | gpu-memory-spaces | C |  |
| gpu-coalescing-patterns | coalesced vs strided vs random transactions | linux | L7135–7143 | comparison | memory-coalescing | B |  |
| gpu-dual-natured-so-file | one .so holds CPU code + GPU cubins | linux | L7262–7273 | address-stack | cubin | B |  |
| gpu-cutlass-vs-cublas-buildtime-svg | build-time vs runtime compilation timeline | linux | `<svg>` L7332–7363 | timeline | jit-vs-aot-compilation | A |  |
| gpu-compilation-full-pipeline-svg | .cu→PTX→cubin→fatbin→.so→wheel + nesting | linux | `<svg>` L7451–7611 | dataflow | cubin | A | #29: 2 lessons (nesting anatomy) |
| gpu-kernel-launch-syscall-path | kernel<<<>>> down to ioctl and SMs | linux | L7622–7639 | dataflow | system-call | B |  |
| gpu-triton-compilation-pipeline | @triton.jit→IR→LLVM→PTX→SASS | linux | L7663–7679 | dataflow | jit-vs-aot-compilation | B |  |
| gpu-tl-constexpr-code | runtime args vs constexpr in signature | linux | L7687–7693 | address-stack | jit-vs-aot-compilation | C |  |
| gpu-cubin-lifecycle-5cases-svg | 5 compile-when cases × 6 pipeline stages grid | linux | `<svg>` L7757–7884 | grid-tiling | jit-vs-aot-compilation | A | #30: 4 lessons (case-matrix) |
| gpu-wheel-anatomy-tree | contents of an installed wheel | linux | L8085–8094 | hierarchy | cubin | B |  |
| gpu-so-elf-sections | ELF sections incl. .nv_fatbin | linux | L8104–8111 | hierarchy | cubin | B |  |
| gpu-fatbin-per-arch-entries | per-arch cubins + PTX fallback | linux | L8121–8129 | hierarchy | cubin | B |  |
| gpu-cubin-symbol-table | symbol table → .text offsets | linux | L8140–8156 | address-stack | cubin | B |  |
| gpu-sass-instruction-fragment | raw SASS listing annotated | linux | L8166–8178 | address-stack | sass | C |  |
| gpu-cublas-cuobjdump-walkthrough | 5-level inspection shell session | linux | L8187–8223 | dataflow | cubin | C |  |
| gpu-dtype-pattern-a-matched-svg | matched-dtype matmul, no casts | linux | `<svg>` L8301–8342 | dataflow | numeric-precision-formats | A |  |
| gpu-dtype-pattern-b-inline-dequant-svg | packed 4-bit weights dequantized inline | linux | `<svg>` L8356–8400 | dataflow | kv-quantization | A |  |
| gpu-dtype-pattern-c-low-precision-svg | both operands quantized; quant/dequant boxes | linux | `<svg>` L8414–8458 | dataflow | quantization | A |  |
| gpu-tensor-core-dtype-menu | supported dtypes per GPU generation | linux | L8475–8480 | comparison | tensor-core | C |  |
| gpu-kernel-hub-portability-layers | 3 nested portability layers | linux | L8573–8584 | layered-stack | jit-vs-aot-compilation | C |  |
| gpu-optimization-framework-levels-map | frameworks mapped to 5 levels | linux | L8607–8616 | grid-tiling | roofline-model | C |  |
| gpu-production-stack-box | vLLM/TRT-LLM/torch.compile/cuBLAS stack | linux | L8640–8650 | layered-stack | roofline-model | B |  |
| gpu-serialization-format-abstraction | model file→weights→universal launch tail | linux | L8663–8669 | dataflow | jit-vs-aot-compilation | C |  |
| gpu-profiling-tool-layers | nvidia-smi→nsys→ncu scope table | linux | L8773–8783 | comparison | roofline-model | C |  |
| gpu-ncu-sol-metrics | Speed-of-Light % readout → memory-bound verdict | linux | L8879–8883 | math-shape | roofline-model | C |  |
| gpu-bottleneck-symptom-table | symptom → likely cause reference | linux | L8973–8987 | comparison | roofline-model | C |  |
| gpu-driver-toolkit-app-compat | driver ≤ toolkit ≤ app chain | linux | L9029–9034 | dataflow | jit-vs-aot-compilation | C |  |
| gpu-gke-node-vs-container-split | node vs container image components | linux | L9046–9078 | layered-stack | container-runtime | B |  |
| gpu-uv-installable-layers | what uv/pip can vs cannot install | linux | L9108–9119 | comparison | jit-vs-aot-compilation | C |  |
| cpugpu-latency-vs-throughput-bet | CPU latency bet vs GPU throughput bet | linux | L9184–9203 | comparison | cpu-vs-gpu | C |  |
| cpugpu-core-granularity-svg | CPU core ≈ SM; AVX lane ≈ CUDA core | linux | `<svg>` L9216–9251 | comparison | cpu-vs-gpu | A |  |
| cpugpu-lane-anatomy-svg | CPU lane = register slice (no PC) vs GPU lane = regs+PC | linux | `<svg>` L9294–9403 | address-stack | cuda-thread-hierarchy | A |  |
| cpugpu-memory-strategy-table | avoid latency vs tolerate latency | linux | L9430–9436 | comparison | memory-hierarchy | C |  |
| cpugpu-simd-simt-cycle-trace-svg | converged vs diverged warp, cycle grid | linux | `<svg>` L9447–9511 | timeline | simt | A | #26: 4 lessons |
| cpugpu-branch-simd-vs-simt-svg | one branch traced SIMD vs SIMT | linux | `<svg>` L9515–9630 | timeline | simt | A |  |
| cpugpu-transistor-budget-floorplan-svg | CPU vs GPU core floorplans | linux | `<svg>` L9653–9730 | grid-tiling | cpu-vs-gpu | A | #23: 7 lessons (spike — comparison spine) |
| cpugpu-where-each-wins-table | workload → winner reference | linux | L9756–9762 | comparison | cpu-vs-gpu | C |  |
| cpp-pointer-reference-triad | object, pointer, and reference of one variable | cpp | "Three relatives of x" L117–135 | address-stack | none (pointer/reference nodes don't exist yet) | B |  |
| cpp-alias-vs-copy | reference aliases storage; a copy diverges | cpp | "Reference vs copy" L169–193 | comparison | none | B |  |
| cpp-address-vs-reference-binding | the two faces of & (address-of vs reference-binding) | cpp | "The two faces of &" L203–219 | comparison | none | B |  |
| cpp-bit-pattern-type-lens | same bits, different pointer type → different value | cpp | "Why pointer types differ" L230–246 | dataflow | none | B |  |
| cpp-address-dereference-inverse | & and * as inverse operations between two worlds | cpp | "& and * are inverses" L274–292 | dataflow | none | B |  |
| gcp-gpu-decision-flowchart | GPU SKU selection by walking spec gates in order | gcp | §02 "Decision map" L327–372 (mermaid) | state-machine (decision tree) | none | A |  |
| gcp-gpu-criteria-gates | per-gate criteria/rationale cards | gcp | §03 L374–491 | comparison | none | C |  |

## Source notes

- **mpi** (`mpi_collective_operations.html`): JS-animated (setTimeout + CSS transition, no SMIL). One shared canvas + palette: purple/teal/coral/pink = data identity A–D per rank; amber = computed result. Fixed rank columns at x=[110,270,430,590].
- **diffop** (`differential-operators-summary.html`): Static (no animation). Shared type-color legend: blue=scalar, teal=vector, amber=matrix, coral=operator/derivative-cell.
- **llm_par** (`llm_parallelism_strategies.jsx`): React tab app; per-figure interactivity noted (interaction-dependent figures are the hardest ports to static SMIL — good late-curriculum examples).
- **notes** (`study-notes.html`): Nearly figure-free (prose + plain tables only; confirmed no `<svg>` anywhere).
- **linux** (`linux-internals-complete.html`): Static (CSS fade on tab switch only). True `<svg>` figures = tier A; styled-div box/arrow/chain/tree diagrams = tier B; styled lists/tables = tier C.
- **cpp** (`cpp-pointers-references-study-guide.html`): Static inline SVGs, shared legend: teal = object/value world, purple = address/pointer world, coral = alternate-type world, amber = frozen copy; green/red pills = compiles/error verdicts.
- **gcp** (`gcp-gpu-guide-final.html`): NOTE: contains NO GPU-microarchitecture diagram — its one true diagram is a Mermaid **decision flowchart** for picking a GCP GPU SKU (fabric → precision → link → VRAM → BW gates), tier-colored (Blackwell-Ultra/Blackwell/Hopper/Ampere/legacy).

## Dataset stats

- **213 figures total** (measured from the flat table): 10 (mpi) + 14 (diffop) + 29 (llm_par) + 1 (notes) + 152 (linux) + 5 (cpp) + 2 (gcp)
- **Tier A: 72** · Tier B: 69 · Tier C: 72 (measured). Train on A first; B as second epoch; C skipped by default.
- Consumed by training: 30/213 (14%) — 28 tier-A, 2 tier-B controls; 115 lessons total.
- Genre coverage across A-tier: dataflow, timeline, grid-tiling, hierarchy, address-stack, layered-stack, state-machine, comparison, math-shape — all nine genres represented.
